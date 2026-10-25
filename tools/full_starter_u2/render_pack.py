# -*- coding:utf-8 -*-
"""Deterministic offline A4 renderer. Generates public DRAFT materials; never a formal RELEASE."""
import html,json,math,re,subprocess,sys,os
from collections import defaultdict,Counter
from pathlib import Path
from datetime import date
from author_data import PACKAGE, KP, SOURCES, SECTIONS, ITEMS, WORD_BANKS, SOURCE_VOCAB_EXTRAS,validate
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
H=lambda x:html.escape(str(x),quote=True)
G=defaultdict(list)
for item in ITEMS:G[item['section']].append(item)
STAGES={'practice':'練習','check':'新題檢核（需撤提示）','delayed':'延後提取（教師保管）'}
CSS='''
@page{size:A4;margin:0}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:#ecefeb;color:#202b34;font-family:"Noto Sans CJK TC","Noto Sans TC","Microsoft JhengHei",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.book{margin:auto;width:210mm;background:#fff}
.page{position:relative;width:210mm;height:297mm;padding:17mm 16mm 18mm;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.page:last-child{page-break-after:auto}
.page-head{height:23mm;border-bottom:1.5px solid #536774;margin-bottom:5mm;display:flex;justify-content:space-between;align-items:flex-start;gap:6mm}
.kicker{font-size:9pt;letter-spacing:.12em;color:#536774;font-weight:700;line-height:1.4}
h1{font-size:19pt;line-height:1.24;margin:3mm 0 1mm;font-weight:750;color:#1c2b38}
h2{font-size:13pt;margin:0 0 2mm;color:#223847}
.meta{font-size:9.2pt;color:#5b6873;line-height:1.4}.unit-pill{background:#f2f4f3;border:1px solid #bdc7ca;border-radius:12px;padding:2.3mm 3mm;font-size:10pt;min-width:27mm;text-align:center;white-space:nowrap;font-weight:700}
.body{height:234mm;overflow:hidden}
.lead{font-size:11pt;line-height:1.55;color:#384750;margin:0 0 4mm}
.rule{font-size:10.5pt;line-height:1.55;border-left:3px solid #677c89;background:#f5f7f7;padding:3mm 4mm;margin:3mm 0 5mm}
.notice{font-size:9.4pt;line-height:1.55;border:1px solid #c2cbd0;border-radius:7px;padding:3mm;margin:3mm 0;color:#455660}
.context{font:10.8pt/1.62 Arial,"Noto Sans CJK TC",sans-serif;padding:3mm 4mm;background:#f6f7f8;border:1px solid #d9dfe2;border-radius:6px;margin:3mm 0 4mm}
.item{padding:2.8mm 0 2.5mm;border-bottom:1px solid #e5e8e9;break-inside:avoid;page-break-inside:avoid}
.item-head{display:flex;align-items:baseline;gap:2mm;margin-bottom:1mm}
.num{font:700 10.5pt Arial;color:#314956;min-width:7mm}
.prompt{font-size:11pt;line-height:1.52;overflow-wrap:anywhere;flex:1}
.english{font-family:Arial,"Noto Sans CJK TC",sans-serif}
.code{font:7pt Arial;color:#86939a;white-space:nowrap;margin-left:2mm}
.write-line{height:11mm;margin-left:9mm;border-bottom:1px solid #aeb9bf;position:relative}
.write-line:before{content:'';position:absolute;bottom:4.4mm;border-bottom:1px dotted #e0e4e6;width:100%}
.oralline{font-size:9pt;color:#5b6972;margin-left:9mm;padding:2mm 0}
.small-line{height:8mm;margin-left:9mm;border-bottom:1px solid #b0bdc5}
.compact-items .item{padding:1.2mm 0 1.2mm}.compact-items .small-line{height:4.5mm}.compact-items .write-line{height:8mm}
.footer{position:absolute;bottom:9mm;left:16mm;right:16mm;border-top:1px solid #d9dfe2;padding-top:2.5mm;display:flex;justify-content:space-between;gap:5mm;color:#6b7780;font-size:8pt}
.family,.map,.distance{border:1px solid #bdc8cd;border-radius:7px;margin:2.5mm 0 4mm;padding:2mm;text-align:center}
.family svg,.map svg,.distance svg{max-width:100%;height:auto;max-height:60mm}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin:5mm 0}.steps div{padding:4mm;border:1px solid #c2cdd3;border-radius:6px;min-height:23mm;font-size:10pt}
.lesson-card{border:1px solid #cbd2d6;background:#f6f8f8;border-radius:8px;padding:4mm;margin:6mm 0}
.status{font-size:9pt;background:#f3f4f2;border-radius:5px;padding:2mm 3mm;display:inline-block;color:#525e66}
.kp-grid{display:grid;grid-template-columns:1fr 1fr;gap:2mm}.kp-grid div{font-size:9pt;border-bottom:1px solid #e0e4e5;padding:2mm 1mm}
.table{border-collapse:collapse;width:100%;font-size:9.25pt;line-height:1.43}.table th,.table td{padding:1.9mm 1.6mm;border-bottom:1px solid #d9dfe2;vertical-align:top;text-align:left}.table th{color:#495d68;background:#f3f5f5;font-weight:700}
.table.compact{font-size:8.3pt}.table.compact td{padding:1.3mm 1mm}
.vocabgrid{display:grid;grid-template-columns:1fr 1fr;gap:2mm 5mm}.vocabrow{border-bottom:1px solid #dce2e4;display:flex;justify-content:space-between;gap:3mm;padding:2.3mm 1mm;font-size:9.4pt}.vocabrow .en{font-family:Arial,sans-serif;font-size:10.2pt;font-weight:700}.vocabrow .zh{font-size:9pt;color:#53636d;text-align:right}
.vrecall{display:grid;grid-template-columns:1fr 1fr;gap:3mm 5mm}.vrecall-item{min-height:17mm;border:1px solid #d8e0e3;border-radius:6px;padding:2mm;font-size:9.5pt}.vrecall-item .blank{margin-top:2.5mm;border-bottom:1px solid #8496a0;height:5mm}
.teacher-row{border-bottom:1px solid #dce2e6;padding:2.3mm 0;break-inside:avoid}.teacher-row .id{font:700 9pt Arial;color:#596e7b}.teacher-row .q{font-size:9.2pt;line-height:1.35;margin:1mm 0}.teacher-row .answer{font-size:10pt;font-weight:700;color:#192f40}.teacher-row .reason{font-size:8.6pt;color:#4f626e;margin-top:1mm}
.checkmark{font-size:10pt;color:#555} .teacher-detail{font-size:9pt;line-height:1.55}
@media screen{.book{box-shadow:0 15px 45px #0002;margin:12px auto}.page{border-bottom:1px dashed #bbb}}
@media(max-width:650px){body{background:#fff}.book{transform-origin:top left;box-shadow:none}}
@media print {.book{margin:0}.page{box-shadow:none;border:none}}
'''
FAMILY_SVG='''<div class="family"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 182" role="img" aria-label="Paul與Carol的兒女是Zac與Zoe；Zoe的兒子是Max">
<g stroke="#5f737d" stroke-width="2" fill="none"><path d="M190 48 H408 M300 48 V73 M180 73 H410 M180 73 V97 M410 73 V97 M410 138 V158"/></g>
<g fill="#fafcfc" stroke="#67808b" stroke-width="1.8"><rect x="122" y="9" width="136" height="38" rx="7"/><rect x="341" y="9" width="136" height="38" rx="7"/><rect x="122" y="97" width="136" height="37" rx="7"/><rect x="341" y="97" width="136" height="37" rx="7"/><rect x="341" y="152" width="136" height="28" rx="7"/></g>
<g fill="#233944" font-size="17" font-family="Arial" text-anchor="middle"><text x="190" y="34">Paul</text><text x="409" y="34">Carol</text><text x="190" y="121">Zac</text><text x="409" y="121">Zoe</text><text x="409" y="171">Max</text></g><text x="300" y="17" fill="#667" font-size="11" text-anchor="middle">parents</text><text x="494" y="170" fill="#667" font-size="10">Zoe's son</text></svg><div class="meta">線索：Paul 與 Carol 是夫妻；Zac 與 Zoe 是他們的兒女；Max 是 Zoe 的兒子。</div></div>'''
DISTANCE_SVG='''<div class="distance"><svg viewBox="0 0 620 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="近遠指示詞：近處有一支pencil及兩支pens，遠處有一把ruler及三本notebooks">
<rect x="3" y="3" width="290" height="164" rx="9" fill="#f5f8f8" stroke="#8ea0a6"/><rect x="326" y="3" width="291" height="164" rx="9" fill="#fff" stroke="#8ea0a6"/>
<text x="147" y="26" text-anchor="middle" font-size="18" fill="#2a3b43">近 Near</text><text x="468" y="26" text-anchor="middle" font-size="18" fill="#2a3b43">遠 Far</text>
<g font-size="14" text-anchor="middle" fill="#283942"><text x="146" y="87">1 pencil</text><text x="146" y="142">2 pens</text><text x="471" y="87">1 ruler</text><text x="471" y="142">3 notebooks</text></g>
<g stroke="#324b58" stroke-width="5" stroke-linecap="round"><path d="M116 53 L170 53"/><path d="M97 108 L130 108 M158 108 L191 108"/><path d="M439 55 L503 55"/></g>
<g fill="#e8eeee" stroke="#566f7b"><rect x="431" y="109" width="26" height="18"/><rect x="466" y="109" width="26" height="18"/><rect x="500" y="109" width="26" height="18"/></g></svg></div>'''
LOCATION_SVG='''<div class="map"><svg viewBox="0 0 620 225" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="clock在table上方、notebook在桌面上、cat在桌子下；ruler位於pencil和eraser中間">
<rect x="2" y="2" width="616" height="220" rx="9" fill="#fff" stroke="#9caeb5"/>
<g stroke="#556e7a" stroke-width="4" fill="none"><path d="M100 108 H515 M128 108 V171 M486 108 V171"/></g>
<circle cx="303" cy="43" r="22" fill="#f2f5f5" stroke="#506574" stroke-width="2"/><path d="M303 28V43L317 51" fill="none" stroke="#506574" stroke-width="2"/>
<g fill="#344b59" font-family="Arial" font-size="15" text-anchor="middle"><text x="304" y="17">clock</text><text x="303" y="134">table</text></g>
<rect x="172" y="88" width="68" height="20" fill="#e1e7e9" stroke="#506574"/><text x="206" y="85" font-size="13" text-anchor="middle">notebook</text>
<ellipse cx="381" cy="146" rx="36" ry="13" fill="#edf1f2" stroke="#566e78"/><path d="M365 136 L358 126 L373 132 M393 134L406 126L404 141" stroke="#566e78" fill="none"/><text x="380" y="180" font-size="14" text-anchor="middle">cat</text>
<g stroke="#4b6572" stroke-width="5" stroke-linecap="round"><path d="M179 198 H221"/><path d="M290 198 H343"/></g><rect x="407" y="187" width="38" height="17" rx="4" fill="#dfe5e7" stroke="#4b6572"/><text x="201" y="217" font-size="11" text-anchor="middle">pencil</text><text x="318" y="217" font-size="11" text-anchor="middle">ruler</text><text x="425" y="217" font-size="11" text-anchor="middle">eraser</text></svg></div>'''

def diagram(section):
    return FAMILY_SVG if section['display']=='family' else DISTANCE_SVG if section['display']=='distance' else LOCATION_SVG if section['display']=='location' else ''

def footer(page,series,unit):return f'<footer class="footer"><span>LESLEY TEACHING ENGINE　·　{H(series)}　·　{H(unit)}</span><span>{page:02}</span></footer>'

def page(title,kicker,unit,body,pg,series='STUDENT',meta=''):
    return f'''<section class="page"><div class="page-head"><div><div class="kicker">{H(kicker)}</div><h1>{H(title)}</h1><div class="meta">{H(meta)}</div></div><span class="unit-pill">{H(unit)}</span></div><div class="body">{body}</div>{footer(pg,series,unit)}</section>'''

def doc(pages,title='Lesley Teaching Engine'):
 return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+H(title)+'</title><style>'+CSS+'</style></head><body><main class="book">'+''.join(pages)+'</main></body></html>'

def paginate(lst,n):return [lst[i:i+n] for i in range(0,len(lst),n)]

def itemHtml(it,i):
    stem=H(it['prompt']);ctx=it.get('context','')
    # fill blanks with a writing line that is never a complete answer; preserve english punct.
    stem=stem.replace('______','<span style="display:inline-block;min-width:28mm;border-bottom:1.6px solid #657d87;line-height:1.5">&nbsp;</span>')
    parts=[f'<div class="item"><div class="item-head"><span class="num">{i:02}.</span><div class="prompt">{stem}</div><span class="code">{H(it["id"])}</span></div>']
    if it.get('form')=='oral': parts.append('<p class="oralline">（請由教師現場記錄口說表現；不以紙本判斷。）</p>')
    else: parts.append('<div class="write-line"></div>' if it['form'] in ['rewrite','short'] else '<div class="small-line"></div>')
    parts.append('</div>');return ''.join(parts)

def section_body(s,chunk,first,stage):
    xs=[]
    xs.append(f'<p class="lead">{H(s["summary"])}</p>')
    if stage=='practice' and s['rule'] and first:
        # no key words deliberately injected into check sheets
        xs.append(f'<div class="rule">{H(s["rule"])}</div>')
    if s['display'] in ['family','distance','location']:xs.append(diagram(s))
    ctxs=[]
    for it in chunk:
        if it.get('context') and it['context'] not in ctxs:ctxs.append(it['context'])
    for ctx in ctxs:xs.append(f'<div class="context">{H(ctx)}</div>')
    if stage=='check':xs.append('<div class="notice">獨立新題草稿：請先收起講義。若教師提供目標相關提示，須另以未曝光的新題重測，不可算獨立通過。</div>' if first else '')
    if stage=='delayed':xs.append('<div class="notice">延後使用；記錄實際相隔日數與提示。這不是當堂再寫一次。</div>' if first else '')
    if s['display']=='distance':xs.append('<div class="compact-items">')
    for i,it in enumerate(chunk,1): xs.append(itemHtml(it,i))
    if s['display']=='distance':xs.append('</div>')
    return ''.join(xs)

def pages_by_stages(stage,unit=None):
    pages=[];counts={}
    for s in SECTIONS:
        arr=[i for i in G[s['id']] if i['stage']==stage]
        if not arr or (unit and s['unit']!=unit):continue
        cap=5 if s['display'] in ['family','location','distance'] else 6
        if s['id']=='U2-A':cap=7
        if s['id']=='U2-C' and stage=='practice':cap=6
        if stage=='practice' and s['id'] in ('S-A','S-C','U1-A','U1-B','U1-C','U1-D','U2-B','R-M'):cap={'S-A':8,'S-C':9,'U1-A':7,'U1-B':6,'U1-C':8,'U1-D':8,'U2-B':8,'R-M':8}[s['id']]
        if s['id'] in ('S-CHECK','U2-CHECK') and stage=='check':cap=6
        parts=paginate(arr,cap)
        for partno,chunk in enumerate(parts):
            title=s['title']+(f'（{partno+1}/{len(parts)}）' if len(parts)>1 else '')
            body=section_body(s,chunk,partno==0,stage)
            counts[s['unit']]=counts.get(s['unit'],0)+len(chunk)
            pages.append((s['unit'],page(title,f'{STAGES[stage]} · {s["id"]}',s['unit'],body,len(pages)+1,series='學生學習單' if stage=='practice' else '教師保管',meta='姓名：__________________　日期：__________________')))
    return pages,counts

def cover():
    groups=[('Starter','字母與發音 → 主格及所有格 → be → 姓名與年齡 → 英文書寫'),('Unit 1','家庭與職業 → Who → be 肯否／問答 → 形容詞 → 閱讀'),('Unit 2','單複數 → 指示詞 → Where＋位置 → 閱讀與字尾讀音')]
    chunks=['<div class="status">DRAFT｜待教師確認內容與正式發行範圍</div>', '<h2 style="margin-top:9mm;font-size:16pt">學習路徑</h2>']
    for unit,desc in groups:chunks.append(f'<div class="lesson-card"><h2>{H(unit)}</h2><p class="lead">{H(desc)}</p></div>')
    chunks.append('<h2 style="margin-top:8mm">使用方式</h2><div class="steps"><div><b>1　先理解</b><br>看一小段，再做對應題。</div><div><b>2　練習</b><br>先找線索，寫出答案。</div><div><b>3　自己作答</b><br>新題檢核由教師另外發放。</div><div><b>4　延後再試</b><br>下一堂或適當間隔重做新題。</div></div>')
    chunks.append('<div class="notice">已教或未教進度、正式版次與音檔尚未完全確認。本學習單可供教師核對、試用，不得直接宣稱完整能力已獨立掌握。英文文字說明若影響理解，可由教師口頭讀出非評量目標的指令。</div>')
    return page('Starter → Unit 2｜學習手冊','SOURCE-BOUND LESSON PACK', '全冊', ''.join(chunks),1,series='學生學習單',meta='翰林七上｜A4 黑白列印友善')

# main student
pr,pc=pages_by_stages('practice')
student_pages=[cover()]
for unit,x in pr:
   # regenerate page numbering to main consecutive by replacement of footer last numeric only
   x=re.sub(r'(<footer class="footer">.*?<span>)\d+(</span></footer>)',lambda m:m.group(1)+f'{len(student_pages)+1:02}'+m.group(2),x)
   student_pages.append(x)
(OUT/'student_practice.html').write_text(doc(student_pages,'學生版｜Starter 至 Unit 2'),encoding='utf8')
# each unit shorter PDFs
for unit in ('Starter','Unit 1','Unit 2','Review'):
   u=[x for name,x in pr if name==unit]
   for i,x in enumerate(u):u[i]=re.sub(r'(<footer class="footer">.*?<span>)\d+(</span></footer>)',lambda m:m.group(1)+f'{i+1:02}'+m.group(2),x)
   (OUT/f'{unit.lower().replace(" ","")}_student.html').write_text(doc(u,unit+' Student Pack'),encoding='utf8')
# check stage check pages
check,_=pages_by_stages('check')
(OUT/'independent_check_teacher_hold.html').write_text(doc([v for u,v in check],'教師另發｜新題檢核'),encoding='utf8')
delayed,_=pages_by_stages('delayed')
(OUT/'delayed_teacher_hold.html').write_text(doc([v for u,v in delayed],'教師另發｜延後題'),encoding='utf8')

# vocabulary bank + active recall, all 29 / 36 word bank entries, no 'know' claim
vocabPages=[]
for unit,words in WORD_BANKS.items():
  for ix,ch in enumerate(paginate(words,16)):
   intro='<div class="status">課本 Word Bank｜學習參考，閱讀並不等於已學會</div><p class="lead">先看英文字、中文意思，必要時教師示範正確發音。稍後可遮住英文再自己提取。</p>'
   body=intro+'<div class="vocabgrid">'+''.join(f'<div class="vocabrow"><span class="en">{H(en)}</span><span class="zh">{H(zh)}</span></div>' for en,zh in ch)+'</div>'
   vocabPages.append(page(f'{unit}｜詞彙總表 {ix+1}', 'VOCABULARY / SOURCE BANK',unit,body,len(vocabPages)+1,series='學生詞彙表',meta=f'原課本共 {len(words)} 項；本頁 {len(ch)} 項'))
  for ix,ch in enumerate(paginate(words,10)):
   body='<p class="lead">請遮住詞彙總表。看中文，自己提取英文。此為練習；錯誤請記錄要補的拼寫或意思。</p><div class="vrecall">'
   for j,(en,zh) in enumerate(ch,ix*10+1):
    body+=f'<div class="vrecall-item"><b>{j:02}. {H(zh)}</b><div class="blank"></div></div>'
   body+='</div><div class="notice">本頁涉及同一份來源詞表。正式獨立評量仍須使用未曝光題與無提示提取。</div>'
   vocabPages.append(page(f'{unit}｜詞彙主動提取 {ix+1}','VOCABULARY / RECALL PRACTICE',unit,body,len(vocabPages)+1,series='學生詞彙複習',meta='姓名：__________________　日期：__________________'))
(OUT/'vocabulary_companion.html').write_text(doc(vocabPages,'詞彙總表與提取｜Unit 1–2'),encoding='utf8')

# Teacher complete: compact per stage (group every 5 items), answer, alternatives, rationale, diagnosis; introductory audit
teacherpages=[]
intro=f'''<div class="status">README｜來源可追溯草稿，不等於正式教材核准</div>
<div class="lesson-card"><h2>來源與內容界線</h2><p class="teacher-detail">政策：LESLEY_TEACHING_ENGINE_v2.4_STABLE.md。來源：使用者上傳翰林七上 Starter＋Unit1，以及 Unit2 書頁。Source Readiness：READY WITH LIMITS；實際版次、教師已教進度及官方聽力音檔尚未完成核對。</p></div>
<div class="steps"><div>主格、所有格、be、姓名與年齡、數字、書寫</div><div>Unit 1：職業、家庭、Who、be 問答、閱讀</div><div>Unit 2：名詞複數、指示詞、Where、位置、閱讀</div><div>音檔缺口：暫只做文字拼讀／口頭觀察，不發布聽力答案</div></div>
<h2>教學證據區分</h2>
<table class="table"><tr><th>種類</th><th>教師判定原則</th></tr><tr><td>練習 Practice</td><td>可顯示規則；有支持的成功不代表已獨立會。</td></tr><tr><td>新題 Check</td><td>收走規則與答案；若給提示，需另取未曝光題重測。</td></tr><tr><td>延後 Delayed</td><td>另日發題，記錄實際相隔日數，無提示才有保留證據。</td></tr><tr><td>口說／聽辨</td><td>有教師現場觀察或官方音源才可判定；紙本填空不等於聽力。</td></tr></table>
<h2>快速教學分流</h2><p class="teacher-detail">學生錯題時先區分：規則不懂／單字無法提取／題意閱讀不足／視角混淆／任務執行中斷。採最小必要支架 → 撤支架 → 新題複查。不要以「粗心」作唯一診斷。</p>'''
teacherpages.append(page('教師使用說明｜全範圍','TEACHER MASTER / CONTROLLED DRAFT','教師',intro,1,series='教師完整版',meta='Student / Teacher / Answer 由單一 JSON 題庫同步產生'))

def teacher_item(it):
 accepted=it.get('accepted',[])
 alt=('可接受：'+'；'.join(accepted)+'。') if len(accepted)>1 else ''
 special='〔原 PR #8 題目保留〕 ' if it.get('legacy_preserved') else ''
 return f'''<div class="teacher-row"><span class="id">{H(it['id'])}　[{H(it['kp'])}]　{H('/'.join(it['source_refs']))}</span><div class="q">{H(it.get('context') or '')}　{H(it['prompt'])}</div><div class="answer">答案：{H(it['answer'])}</div><div class="reason">{special}{H(it['rationale'])} {H(alt)}<br>觀察：{H(it['diagnosis'])}</div></div>'''
for unit in ['Starter','Unit 1','Unit 2','Review']:
 for st in ['practice','check','delayed']:
  arr=[i for i in ITEMS if i['unit']==unit and i['stage']==st]
  if not arr:continue
  for ci,ch in enumerate(paginate(arr,6)):
   content=f'<p class="lead">{STAGES[st]}｜{unit}。{ "如為延後題，避免在當堂學生版曝光。" if st=="delayed" else "教師核對答案及錯誤來源；不要將輔助成功算為獨立掌握。" }</p>'
   content+=''.join(teacher_item(i) for i in ch)
   teacherpages.append(page(f'{unit}｜{STAGES[st]} {ci+1}', 'TEACHER / ANSWER + DIAGNOSIS',unit,content,len(teacherpages)+1,series='教師完整版',meta=f'本頁 {len(ch)} 題；不發給學生'))
(OUT/'teacher_complete.html').write_text(doc(teacherpages,'Teacher Complete + Answers'),encoding='utf8')

# quick answer sheets, all questions included, includes vocab keys
answerpages=[]
for unit in ['Starter','Unit 1','Unit 2','Review']:
 for st in ['practice','check','delayed']:
  arr=[i for i in ITEMS if i['unit']==unit and i['stage']==st]
  for ci,ch in enumerate(paginate(arr,18)):
   rows=''.join(f'<tr><td>{H(i["id"])}</td><td>{H(i["answer"])}</td><td>{H(i["kp"])}</td></tr>' for i in ch)
   body=f'<p class="lead">僅供教師批改。回答可接受變體請以教師完整版為準。</p><table class="table compact"><tr><th style="width:33%">題號</th><th>答案</th><th>目標</th></tr>{rows}</table>'
   answerpages.append(page(f'{unit}｜{STAGES[st]}　答案 {ci+1}','ANSWER KEY / TEACHER ONLY',unit,body,len(answerpages)+1,series='教師答案速查',meta=f'{len(ch)} 題'))
for unit,arr in WORD_BANKS.items():
 for ix,ch in enumerate(paginate(arr,25)):
  rows=''.join(f'<tr><td>{ix*25+j:02}</td><td>{H(c)}</td><td>{H(en)}</td></tr>' for j,(en,c) in enumerate(ch,1))
  body='<p class="lead">詞彙提取答案。核對拼寫，並分開判定詞義與字形。</p><table class="table compact"><tr><th>編號</th><th>中文提示</th><th>英文答案</th></tr>'+rows+'</table>'
  answerpages.append(page(f'{unit}｜詞彙答案 {ix+1}','VOCABULARY / ANSWER KEY',unit,body,len(answerpages)+1,series='教師答案速查'))
(OUT/'answer_key.html').write_text(doc(answerpages,'Answer Key｜全範圍'),encoding='utf8')

# Coverage matrix with transparency, statuses not masquerading academic outcomes
coverage={kp:dict(known=KP[kp],stages={st:[i['id'] for i in ITEMS if i['kp']==kp and i['stage']==st] for st in STAGES}) for kp in KP}
for kp,row in coverage.items():
 row['activity_covered']=bool(row['stages']['practice'])
 row['check_covered']=bool(row['stages']['check'])
 row['delayed_covered']=bool(row['stages']['delayed'])
 row['audio_or_oral_pending']='Only' in row['known']['kind'] or 'Oral' in row['known']['kind']
(OUT/'source_coverage.json').write_text(json.dumps(dict(schema='Lesley Source-Matrix v0.1',status='DRAFT_NOT_RELEASED',kp=coverage,sources=SOURCES,audio_pending=PACKAGE['audio_gaps'],vocabulary_count={k:len(v) for k,v in WORD_BANKS.items()}),ensure_ascii=False,indent=2),encoding='utf8')
sourcePages=[]
head='<div class="status">Audited source presence ≠ approved learning evidence</div><h2 style="margin:7mm 0 3mm">資料來源</h2><table class="table"><tr><th>ID</th><th>PDF 頁次 / 課本頁次</th><th>用途</th></tr>'
head+=''.join(f'<tr><td>{H(sid)}</td><td>{H(s["file"])}<br>{H(s["pdf"])} / {H(s["printed"])}</td><td>{H(s["note"])}</td></tr>' for sid,s in list(SOURCES.items())[:8])+'</table>'
sourcePages.append(page('來源與限制｜Source Authority','SCOPE MATRIX / PAGE 1','教師',head,1,series='來源知識點覆蓋',meta='相同教材之不同 PDF 頁次可能為攤頁；以印刷頁次為優先定位。'))
head2='<table class="table"><tr><th>ID</th><th>PDF 頁次 / 課本頁次</th><th>用途</th></tr>'
head2+=''.join(f'<tr><td>{H(sid)}</td><td>{H(s["file"])}<br>{H(s["pdf"])} / {H(s["printed"])}</td><td>{H(s["note"])}</td></tr>' for sid,s in list(SOURCES.items())[8:])+'</table><div class="notice">來源為上傳課本掃描的內容核對；未取得官方音檔、版次完整核准以及特定學生的獨立成績證據。正式發行需另外完成 Teaching Engine v2.4 Stable 的完整來源鎖定與 Release QA。</div>'
sourcePages.append(page('來源與限制｜Source Authority','SCOPE MATRIX / PAGE 2','教師',head2,2,series='來源知識點覆蓋'))
for unit in ['Starter','Unit 1','Unit 2']:
 arr=[coverage[i] for i,x in KP.items() if x['unit']==unit]
 for ix,ch in enumerate(paginate(arr,13)):
  rows=''
  for x in ch:
    z=x['known'];st=x['stages'];c=lambda s:'✓ '+str(len(st[s])) if st[s] else '—'
    rows+=f'<tr><td>{H(z["id"])}</td><td>{H(z["name"])}<div class="meta">{H(z["kind"])} · {H("/".join(z["sources"]))}</div></td><td>{c("practice")}</td><td>{c("check")}</td><td>{c("delayed")}</td></tr>'
  body='<table class="table compact"><tr><th>ID</th><th>知識點與來源</th><th>練習</th><th>新題</th><th>延後</th></tr>'+rows+'</table>'
  body+='<div class="notice">「✓」代表已設計對應的題目／活動，不表示學生答對或已精熟；有些能力需要口說／音檔才能驗證。</div>'
  sourcePages.append(page(f'{unit}｜知識點覆蓋 {ix+1}','SCOPE / CONTENT COVERAGE',unit,body,len(sourcePages)+1,series='來源知識點覆蓋'))
# audit page vocab & audio
rows=''.join(f'<tr><td>{H(a["unit"])}</td><td>{H(a["aspect"])}</td><td>{H(a["action"])}</td></tr>' for a in PACKAGE['audio_gaps'])
audioPage='<p class="lead">本份題庫完成的是紙本與文字活動「設計覆蓋」，不是已驗證的口語、聽力或精熟證據。</p><table class="table"><tr><th>範圍</th><th>尚缺的證據</th><th>完成方法</th></tr>'+rows+'</table>'
audioPage+='<div class="lesson-card"><h2>字彙覆蓋</h2><p>Unit 1 課本 Word Bank：29 項；Unit 2：36 項。另有 Theme Words、Starter phonics 等對照清單。每字已進入獨立的詞彙總表及中文提示提取頁；只屬活動覆蓋，未宣稱已掌握。</p></div>'
audioPage+='<div class="lesson-card"><h2>待核准事項</h2><p>□ 目前課本版次與學校範圍　 □ 教師核對單字與已教進度　 □ 正式音檔　 □ 新題正式 Gate 與提示撤除　 □ 學生／教師／答案 Release QA。</p></div>'
sourcePages.append(page('證據缺口與發行前檢查','SOURCE / EVIDENCE GAP','教師',audioPage,len(sourcePages)+1,series='來源知識點覆蓋'))
(OUT/'source_matrix.html').write_text(doc(sourcePages,'Scope Coverage Matrix'),encoding='utf8')

# Markdown and CSV matrix (no user data)
lines=['# Starter–Unit 2｜全範圍知識點與題目對照','', '**狀態：DRAFT_FOR_TEACHER_REVIEW；不是正式版。**','', '以使用者提供之《學校課本Starter & Unit 1.pdf》及《Unit 2.pdf》為本次內容來源。','',f'**共 {len(KP)} 項知識點、{len(ITEMS)} 題主題練習／檢核／延後題（含保留舊 PR#8 原題），Word Bank 65 詞。**','', '|ID|課程|知識點|來源|練習題號|新題題號|延後題號|證據限制|','|---|---|---|---|---|---|---|---|']
for kid,row in coverage.items():
 k=row['known'];s=row['stages'];lines.append('|'.join(['',kid,k['unit'],k['name'],', '.join(k['sources']), ', '.join(s['practice']) or '—', ', '.join(s['check']) or '—', ', '.join(s['delayed']) or '—', ('音檔／口說待核' if row['audio_or_oral_pending'] else k['kind']), '']))
lines+=['','## 各單元 Word Bank（原書英文索引，含中文對照）','']
for unit,words in WORD_BANKS.items():
 lines.append(f'### {unit}（{len(words)} 項）')
 lines.append('、'.join(f'{en}（{zh}）' for en,zh in words));lines.append('')
lines+=['## 音訊／口說尚待驗證','','- '+'\n- '.join(f'{x["unit"]}：{x["aspect"]}（{x["action"]}）' for x in PACKAGE['audio_gaps']),'','## 發行前未完成','','- 未核對學校指定版次、核准課程範圍、特定學生學習進度與完整音檔。','- 原課本作答與批改不能視為獨立能力證據。','- Student／Teacher／Answer 已同源生成，但仍需教師逐題確認與完整 Release QA。','- 所有公開示範題不可宣稱保密；新題獨立施測應確認學生未事先接觸。']
(ROOT/'KNOWLEDGE_COVERAGE_MATRIX.md').write_text('\n'.join(lines),encoding='utf8')
print(json.dumps({'pages':{'practice':len(student_pages),'check':len(check),'delayed':len(delayed),'teacher':len(teacherpages),'answer':len(answerpages),'vocab':len(vocabPages),'matrix':len(sourcePages)},'items':len(ITEMS),'kp':len(KP),'vocab':sum(len(x) for x in WORD_BANKS.values())},ensure_ascii=False))