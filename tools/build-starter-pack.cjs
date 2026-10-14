#!/usr/bin/env node
'use strict';
/* Source-bound, teacher-review-only preview builder.
   This script intentionally has no formal RELEASE action or remote API. */
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const manifestPath = path.join(root, 'curriculum/starter/subject-be.manifest.json');
const itemsPath = path.join(root, 'curriculum/starter/subject-be.items.json');
const defaultOutput = path.join(root, 'examples/starter-be');
const stages = ['guided', 'independent', 'transfer', 'delayed'];
const orderedLabels = {guided:'引導練習', independent:'不看提示的新題', transfer:'新情境判斷', delayed:'延後無提示提取'};
const toPlain = o => JSON.parse(JSON.stringify(o));
const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const key = s => String(s||'').toLowerCase().trim().replace(/\s+/g,' ');
const countBlanks = prompt => (String(prompt).match(/____/g)||[]).length;
function validate(manifest, map) {
  const errors=[], warnings=[];
  if (!manifest || !map) return {errors:['缺少來源或題目資料'],warnings};
  const src = manifest.content_authority||{}, scope=manifest.content_source_lock||{}, p=manifest.pedagogy_lock||{};
  if (manifest.unit_id !== map.unit_id) errors.push('來源與題目 unit_id 不一致');
  if (src.source_readiness === 'BLOCKED' || !['READY','READY_WITH_LIMITS'].includes(src.source_readiness)) errors.push('Source Readiness 不足，停止題目生成');
  if (!src.sources?.length || !src.sources.every(s=>s.ref && s.file && s.file_page_1_indexed && s.printed_page)) errors.push('來源缺少可回查頁次');
  if (!scope.in_scope || !scope.out_of_scope?.length) errors.push('Content Scope Lock 未完成');
  if (!p.learning_target || !p.support_removal_point || !p.delayed_plan || !p.scaffolds) errors.push('Pedagogy Lock 缺少目標或撤提示／延後計畫');
  if (map.items?.length === 0 || !Array.isArray(map.items)) errors.push('題目資料不存在');
  const ids=new Set(), textKeys=new Set(), allowed=new Set((scope.lexical_allowlist||[]).map(key)), sourceIds=new Set((src.sources||[]).map(s=>s.ref));
  const itemCounters = {guided:0, independent:0, transfer:0, delayed:0};
  for (const item of map.items||[]) {
    if (!/^[GITD]\d{2}$/.test(item.id||'')) errors.push('題號格式錯誤：'+String(item.id));
    if (ids.has(item.id)) errors.push('重複題號：'+item.id); else ids.add(item.id);
    if (!stages.includes(item.stage)) errors.push('未知題目階段：'+item.id);
    else itemCounters[item.stage]++;
    if (!item.prompt || !item.answers || item.answers.length !== countBlanks(item.prompt)) errors.push('空格／答案數不一致：'+item.id);
    if (!item.source_refs?.length || item.source_refs.some(ref=>!sourceIds.has(ref))) errors.push('題目缺可追溯來源：'+item.id);
    if (!item.target || !item.construct || !item.rationale || !item.diagnosis || !item.leakage) errors.push('Blueprint 證據不完整：'+item.id);
    const normalizedPrompt=key(item.prompt);
    if (textKeys.has(normalizedPrompt)) errors.push('練習與重測不得使用相同原題：'+item.id);
    textKeys.add(normalizedPrompt);
    // Check English tokens in the student prompt and optional synthetic Chinese scenario.
    for(const token of `${item.prompt} ${item.context_zh||''}`.match(/[A-Za-z]+/g)||[]) {
      if (!allowed.has(key(token))) errors.push(`未經來源核對的學生詞彙：${item.id} / ${token}`);
    }
    for (const token of item.answers||[]) if(!allowed.has(key(token))) errors.push(`答案詞彙不在 Source Lock：${item.id} / ${token}`);
  }
  if (!itemCounters.guided || !itemCounters.independent || !itemCounters.transfer || !itemCounters.delayed) errors.push('缺少必要的練習／應用／遷移／延後證據分流');
  if (!src.official_edition_confirmed) warnings.push('正式教材版本尚未由教師對照封面／版權資訊核實。');
  if (!src.teacher_confirmed_current_source) warnings.push('現行來源未取得教師核准；不能正式發行。');
  if(src.source_items_answer_exposed) warnings.push('原始課本含已作答／訂正，不得使用原題作獨立掌握證據。');
  if (scope.verified_prior_exposure_for_particular_student==='UNVERIFIED') warnings.push('特定學生是否已完整學習本範圍尚未獲獨立證明。');
  if (p.formal_gate_approved !== true) warnings.push('正式 Gate 未核准；本稿不標示達標或精熟。');
  // Deliberate hard stop on formally asserting a release despite a passing code check.
  if(manifest.publication?.teacher_approved !== true || p.formal_release_authorized!==true || manifest.publication?.release_quality_review!=='PASS') warnings.push('正式發行 QA 與教師審核尚未完成；僅可建立草稿預覽。');
  return {errors:[...new Set(errors)],warnings:[...new Set(warnings)],counts:itemCounters, status:errors.length?'BLOCKED':'DRAFT_FOR_TEACHER_REVIEW'};
}
const defaultStyle = `
  @page{size:A4;margin:14mm 16mm 16mm}
  *{box-sizing:border-box}
  body{margin:0;background:#f2f3f2;color:#1b252d;font:15px/1.55 "Noto Sans TC","Microsoft JhengHei",Arial,sans-serif}
  main{max-width:860px;margin:18px auto;padding:18px;background:#fff;box-shadow:0 5px 30px #0001}
  .page{margin:0 0 18px;padding:16px 18px 20px;border:1px solid #b8c0c3;border-radius:9px;background:#fff;min-height:265mm;position:relative;break-after:page;page-break-after:always}
  .page:last-child{break-after:auto;page-break-after:auto}
  .eyebrow{font-size:11px;color:#61707c;letter-spacing:.12em;font-weight:800}
  h1{font-size:24px;margin:8px 0 7px;line-height:1.32}h2{font-size:17px;margin:15px 0 8px}
  p{margin:5px 0 10px} .muted{color:#52616c} .thin{font-size:12px}
  .meta{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #b3bcc2;padding:7px 0 11px;margin-bottom:12px}
  .section{padding:12px 0;border-top:1px solid #d5dadd}
  .rulegrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:12px 0 18px}
  .rulegrid div{border:1px solid #aab4bb;padding:11px 9px;border-radius:6px;text-align:center;font:700 16px/1.4 Arial,sans-serif}
  .english{font:500 19px/1.6 Arial,"Noto Sans",sans-serif;letter-spacing:.01em}
  .question{display:flex;align-items:flex-start;gap:13px;margin:17px 0 20px;break-inside:avoid}
  .question .num{min-width:42px;font:700 12px/1.6 Arial;color:#4c5d67;padding-top:6px}
  .question .stem{flex:1;border-bottom:1px solid #e2e5e7;padding-bottom:15px;min-height:40px}
  .stem small{display:block;color:#46515b;font-size:13px;margin-bottom:7px}
  .paperline{display:block;border-bottom:1px solid #aeb9bd;height:29px;margin-top:5px}
  .footer{position:absolute;bottom:12px;left:18px;right:18px;font-size:10px;color:#586770;border-top:1px solid #d6dcdf;padding-top:7px;display:flex;justify-content:space-between}
  .tag{font-size:11px;display:inline-block;background:#ebedee;padding:4px 9px;border-radius:4px;font-weight:700}
  .guidegrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0}
  .guidebox{border:1px solid #b4bdc3;border-radius:6px;padding:10px 12px}
  table{width:100%;border-collapse:collapse;font-size:12px;line-height:1.6}
  th,td{border-bottom:1px solid #c7cdd0;padding:6px 5px;vertical-align:top;text-align:left}
  th{background:#eee;font-weight:800}
  .record{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:13px 0}
  .record label{border:1px solid #b9c2c7;border-radius:4px;padding:8px 10px;font-size:12px}
  @media screen and (max-width:700px){main{margin:0;padding:5px;box-shadow:none}.page{min-height:0;border-radius:0;padding:16px 15px 35px}.guidegrid{grid-template-columns:1fr}.rulegrid{gap:4px}.rulegrid div{padding:8px 3px;font-size:14px}}
  @media print{body{background:#fff;color:#111}main{max-width:none;margin:0;padding:0;box-shadow:none}.page{border:0;border-radius:0;padding:0;min-height:262mm;margin:0;box-shadow:none}.footer{left:0;right:0;bottom:0}.rulegrid div{border-color:#555}th{background:#eee!important;print-color-adjust:exact}.question{margin:14px 0 15px}}
`;
const footer=(left,right)=>`<div class="footer"><span>${escapeHtml(left)}</span><span>${escapeHtml(right)}</span></div>`;
const label = (m)=>`${m.title}｜教師審閱前試用稿`;
const instruction = s=>`<p class="muted">${escapeHtml(s)}</p>`;
const question = (item, {withAnswer=false, diagnostic=false}={})=>`<div class="question"><span class="num">${escapeHtml(item.id)}</span><div class="stem">${item.context_zh?`<small>${escapeHtml(item.context_zh)}</small>`:''}<div class="english">${escapeHtml(item.prompt).replace(/____/g,'<span style="white-space:nowrap;display:inline-block;min-width:70px;border-bottom:2px solid #566;transform:translateY(-3px)">&nbsp;</span>')}</div>${withAnswer?`<div style="font-size:13px;margin-top:7px"><strong>答案：</strong>${item.answers.map(escapeHtml).join(' / ')}　<span class="muted">${escapeHtml(item.rationale)}</span></div>`:''}${diagnostic?`<div class="thin muted">判讀：${escapeHtml(item.diagnosis)}</div>`:''}</div></div>`;
const pageOpen=(type,title,sub)=>`<section class="page"><div class="eyebrow">LESLEY TEACHING ENGINE · ${escapeHtml(type)} · DRAFT</div><h1>${escapeHtml(title)}</h1>${sub?`<p class="muted">${escapeHtml(sub)}</p>`:''}`;
const pageClose=()=>`</section>`;
const wrap=(title,pages)=>`<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>${defaultStyle}</style></head><body><main>${pages.join('')}</main></body></html>`;
function byStage(map,stage){return map.items.filter(item=>item.stage===stage);}
function student(manifest,map){
 const p1=`${pageOpen('STUDENT / 1','主格代名詞 × be 動詞','姓名：____________________　日期：____________________')}
 <div class="meta"><span>本頁：理解規則與引導練習</span><span class="tag">先看 → 再做</span></div>
 <h2>1. 看主詞，選 be 動詞</h2>
 <div class="rulegrid"><div>I → am</div><div>He / She / It → is</div><div>You / We / They → are</div></div>
 <p>請先觀察：不是每個主詞都用同一個 be 動詞。</p><h2>2. 跟著做｜Guided Practice</h2>${instruction(map.instructions.guided)}
 ${byStage(map,'guided').map(i=>question(i)).join('')}
 <p class="muted thin" style="margin-top:25px">完成後，請教師先收起或遮住本頁，再翻到下一頁。</p>
 ${footer('Starter Unit｜引導練習，不算獨立掌握證據','1 / 2')}${pageClose()}`;
 const p2=`${pageOpen('STUDENT / 2','自己試試｜不看提示的新題','姓名：____________________　日期：____________________')}
 <div class="meta"><span>本頁不提供規則表或字庫</span><span class="tag">NEW ITEMS</span></div>
 <h2>3. 獨立應用</h2>${instruction(map.instructions.independent)}
 ${byStage(map,'independent').map(i=>question(i)).join('')}
 <div class="section"><h2>4. 新情境判斷</h2>${instruction(map.instructions.transfer)}
 ${byStage(map,'transfer').map(i=>question(i)).join('')}</div>
 ${footer('需教師記錄是否有提示；答對不自動等於精熟','2 / 2')}${pageClose()}`;
 return wrap('Starter Unit 學生版｜待教師核對', [p1,p2]);
}
function answer(manifest,map){
 const groups=stages.map(stage=>`<h2>${orderedLabels[stage]}</h2><table><thead><tr><th style="width:48px">題號</th><th>正確答案</th><th>核心理由</th></tr></thead><tbody>${byStage(map,stage).map(i=>`<tr><td>${escapeHtml(i.id)}</td><td><strong>${i.answers.map(escapeHtml).join(' / ')}</strong></td><td>${escapeHtml(i.rationale)}</td></tr>`).join('')}</tbody></table>`).join('');
 const pg=`${pageOpen('ANSWER KEY','教師答案與解析','與 Student / Teacher / Delayed 使用同一題目 ID 和答案資料')}
 <span class="tag">教師保管｜不可與學生測驗同頁發放</span>${groups}
 <p class="thin muted">本答案表只對應示範題組；正式課本版次、班級已教內容與發行 QA 尚待確認。</p>
 ${footer('Teacher-only · Same item map · DRAFT','Answer key')}${pageClose()}`;
 return wrap('Starter Unit｜答案解析（草案）',[pg]);
}
function teacher(manifest,map,qa){
 const src=manifest.content_authority, p=manifest.pedagogy_lock;
 const pg1=`${pageOpen('TEACHER GUIDE / 1','來源鎖定與教學流程','此文件為教師審核草案，不代表正式 Release QA 通過。')}
 <h2>來源與發行狀態</h2>
 <div class="guidegrid"><div class="guidebox"><strong>來源狀態</strong><p>${escapeHtml(src.source_readiness)}</p><p class="thin">目前只核對教科書印刷頁 5–6 的內容，不推定全單元範圍。</p></div><div class="guidebox"><strong>發布狀態</strong><p>DRAFT_FOR_TEACHER_REVIEW</p><p class="thin">正式版次、教師核准、正式 Release QA 尚未完成。</p></div></div>
 <table><thead><tr><th>原始檔</th><th>來源位置</th><th>使用界線</th></tr></thead><tbody>${src.sources.map(s=>`<tr><td>${escapeHtml(s.file)}</td><td>PDF 第 ${s.file_page_1_indexed} 頁／書頁 ${s.printed_page}</td><td>${escapeHtml(s.section)}</td></tr>`).join('')}</tbody></table>
 <h2>本課鎖定內容</h2><p><strong>核心：</strong>${escapeHtml(manifest.content_source_lock.in_scope)}</p><p><strong>本次不加入：</strong>${escapeHtml(manifest.content_source_lock.out_of_scope.join('、'))}</p><h2>教學／證據流程</h2>
 <div class="guidegrid"><div class="guidebox"><strong>先教：G01-G03</strong><p class="thin">可展示主詞與 be 對照表，可口頭提示；不能算獨立成效。</p></div><div class="guidebox"><strong>撤提示：I01-I07</strong><p class="thin">收走第一頁；學生使用未曝光新題；教師記錄有無提示。</p></div><div class="guidebox"><strong>換情境：T01-T02</strong><p class="thin">辨識說話者及代名詞，和 be 動詞分開記錄錯誤。</p></div><div class="guidebox"><strong>延後：D01-D04</strong><p class="thin">下一堂或按需要另發卡片；須記錄實際時間差。</p></div></div>
 <h2>資料限制與提醒</h2>${qa.warnings.map(x=>`<p class="thin">• ${escapeHtml(x)}</p>`).join('')}
 ${footer('來源僅涵蓋 Starter 主格代名詞＋be 動詞','Teacher 1 / 2')}${pageClose()}`;
 const pg2=`${pageOpen('TEACHER GUIDE / 2','逐題診斷與支持紀錄','本頁給教師批改使用；不要隨學生題本發放。')}
 <table><thead><tr><th style="width:46px">題號</th><th style="width:74px">正解</th><th>錯誤診斷與後續動作</th></tr></thead><tbody>${map.items.map(i=>`<tr><td>${escapeHtml(i.id)}</td><td>${i.answers.map(escapeHtml).join(' / ')}</td><td>${escapeHtml(i.diagnosis)}</td></tr>`).join('')}</tbody></table>
 <h2>執行與證據紀錄（當堂）</h2>
 <div class="record"><label>獨立題 I01–I07：＿＿／7<br>□ 無提示　□ 有提示：＿＿＿＿＿</label><label>新情境 T01–T02：＿＿／2<br>□ 視角正確　□ 需另核對</label><label>提示撤除後新題重測：<br>□ 尚未做　□ 已另行記錄</label><label>延後卡片：<br>日期：＿＿＿＿　實際相隔：＿＿天</label></div>
 <p class="thin">**判定：** 題目正確率只記錄作答表現；本稿未定義正式 Gate 通過門檻，不以示範練習或分數直接宣告精熟。</p>
 ${footer('Teacher-only · 請保存學生作答與提示紀錄','Teacher 2 / 2')}${pageClose()}`;
 return wrap('Starter Unit｜教師指引（草案）',[pg1,pg2]);
}
function delayed(manifest,map){
 const pg=`${pageOpen('DELAYED CARD','延後複查卡｜不看筆記','姓名：____________________　日期：________　距離上次練習：______ 天')}
 <div class="meta"><span>教師請在後續課程獨立發放本卡</span><span class="tag">NEW ITEMS / NO CUE</span></div>
 ${instruction(map.instructions.delayed)}
 ${byStage(map,'delayed').map(i=>question(i)).join('')}
 <div style="height:30px"></div><p class="thin muted">教師記錄：□ 全程獨立　□ 有提供提示；提示類型：____________________</p>
 ${footer('本卡不得與第一次練習同時曝光','Delayed retrieval')}${pageClose()}`;
 return wrap('Starter Unit｜延後複查卡（待教師審核）',[pg]);
}
function build(manifest,map){
 const qa=validate(manifest,map);
 if(qa.errors.length) return {qa,files:null};
 return {qa,files:{'student.html':student(manifest,map),'teacher.html':teacher(manifest,map,qa),'answer.html':answer(manifest,map),'delayed.html':delayed(manifest,map)}};
}
function cli(){
 const argv=process.argv.slice(2);
 if(argv.includes('--release')) {console.error('BLOCKED: 此工具不提供正式發行指令；必須先完成教師核准及正式 Release QA。');process.exitCode=3;return;}
 const manifest=JSON.parse(fs.readFileSync(manifestPath,'utf8')), map=JSON.parse(fs.readFileSync(itemsPath,'utf8'));
 const {qa,files}=build(manifest,map);
 if(qa.errors.length){console.error(JSON.stringify(qa,null,2));process.exitCode=2;return;}
 if(argv.includes('--check')){console.log(JSON.stringify(qa,null,2));return;}
 const outIndex=argv.indexOf('--out'), out=outIndex>=0&&argv[outIndex+1]?path.resolve(argv[outIndex+1]):defaultOutput;
 fs.mkdirSync(out,{recursive:true});
 for(const [name,html] of Object.entries(files))fs.writeFileSync(path.join(out,name),html,'utf8');
 fs.writeFileSync(path.join(out,'qa-report.json'),JSON.stringify({build_status:qa.status,...qa,attribution:'teacher-created synthetic questions based on verified limited textbook pages; no master approval'},null,2),'utf8');
 console.log(JSON.stringify({out,status:qa.status,files:Object.keys(files),counts:qa.counts,warnings:qa.warnings},null,2));
}
if(require.main===module)cli();
module.exports={validate,build,escapeHtml,countBlanks,student,teacher,answer,delayed};
