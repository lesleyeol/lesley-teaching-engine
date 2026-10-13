/* Lesley Adaptive Lesson Design | v0.1 proposal implementation
   Deterministic, offline BLUEPRINT recommender. No AI, no assessment authoring.
   This is not an independent source verifier or release authorization mechanism. */
(function (root, build) {
  const api = build();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.LesleyAdaptive = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const topics = Object.freeze({
    'starter-be': {
      label: 'Starter｜主格代名詞與 be 動詞',
      target: '能依主詞選擇 am / is / are，並在未看過的句子中正確應用。',
      primary: ['compare-subject', 'sentence-apply'],
      transfer: '以新人物或新主詞造句，不直接重做示範句。',
      omitted: '名詞分類不是本目標，不必安排 Noun Detective。',
      sourceHint: '翰林七上 Starter Unit：主格代名詞、be 動詞搭配（頁次須再次核對）'
    },
    'starter-questions': {
      label: 'Starter｜姓名與年齡問答',
      target: '能依提問內容與說話者視角，選擇姓名或年齡問答。',
      primary: ['speaker-role', 'dialogue-decision'],
      transfer: '更換答話者及人稱，完成新情境中的問答。',
      omitted: '本目標在視角與問答功能，不需強制做名詞分類。',
      sourceHint: '翰林七上 Starter Unit：What is ... name?、How old ...?（頁次須再次核對）'
    },
    'unit1-family': {
      label: 'Unit 1｜人物身分與家庭關係',
      target: '能從人物關係資訊，正確回答 Who 問句並說明指涉。',
      primary: ['relation-map', 'dialogue-decision'],
      transfer: '換一張未看過的關係圖，使用新資訊回答。',
      omitted: '若目標是人物關係，無需另湊 One or Many 的名詞複數活動。',
      sourceHint: '翰林七上 Unit 1：Who 問句與家庭成員（頁次須再次核對）'
    },
    'unit2-location': {
      label: 'Unit 2｜Where 與位置介系詞',
      target: '能依圖中明確位置，用 Where 問答描述物品所在。',
      primary: ['location-map', 'context-explain'],
      transfer: '換一張位置不同的新圖，判斷並說明。',
      omitted: '不需要額外安排與位置能力無關的聲音切分活動。',
      sourceHint: '翰林七上 Unit 2：Where 與位置介系詞（頁次須再次核對）'
    },
    'reading': {
      label: '閱讀｜定位證據與推論',
      target: '能回到原文找出支持答案的句子，區分明示資訊與推論。',
      primary: ['evidence-locator', 'context-explain'],
      transfer: '用不同段落或新文章，獨立找證據。',
      omitted: '閱讀主題不必強加單複數活動；問題應由文本證據決定。',
      sourceHint: '請填入核准閱讀文本的書名、篇名、頁次或段落。'
    },
    'spelling': {
      label: '拼字｜聲音與字形提取',
      target: '能聽辨音節與音素，移除提示後獨立拼出已教目標字。',
      primary: ['sound-chunks', 'active-spelling'],
      transfer: '換順序與提示方向，延後聽寫未曝光題組。',
      omitted: '不因需要有趣而強制插圖、故事或 Noun Detective。',
      sourceHint: '請填入核准單字表與詞彙來源。'
    },
    'custom': {
      label: '自訂教學主題',
      target: '',
      primary: [],
      transfer: '由教師依已核對的學習目標設計新的情境。',
      omitted: '不加入與自訂目標無明確關聯的活動。',
      sourceHint: '填入原始／核准來源與頁次。'
    }
  });

  const activities = Object.freeze({
    'compare-subject': {
      label: '主詞對照｜Compare', stage: '引導理解', minutes: 8,
      action: '將不同主詞並排，找出與 am / is / are 的對應；先說明差異，不急著長篇書寫。',
      why: '此目標先需要辨識主詞，對照能把文法選擇的依據顯性化。',
      support: '以表格對齊關鍵主詞；進入獨立檢核前移除表格。'
    },
    'sentence-apply': {
      label: '新句應用｜Apply', stage: '受控應用', minutes: 9,
      action: '用已核准的詞彙，完成不同主詞的短句；請學生說明選擇依據。',
      why: '檢查是否真正把主詞線索用在句子中，而非只會背誦規則。',
      support: '練習時可標記主詞；新題獨立檢核時移除標記。'
    },
    'speaker-role': {
      label: '說話者角色卡｜Role', stage: '視角辨識', minutes: 8,
      action: '先標明提問者、答話者與被問對象，再比較姓名與年齡的問法。',
      why: '姓名與年齡問答容易混淆說話者視角；角色可讓指涉清楚。',
      support: '練習用角色卡，獨立檢核時只留下題目必要資訊。'
    },
    'dialogue-decision': {
      label: '短對話判斷｜Dialogue', stage: '語境應用', minutes: 9,
      action: '閱讀兩輪短對話，依問題功能選擇回答，說出判斷線索。',
      why: '需要從語境決定用法，避免單純依字面看到關鍵字猜答案。',
      support: '先示範回文定位；新題必須換對話與角色。'
    },
    'relation-map': {
      label: '家族關係圖｜Relation', stage: '資訊推理', minutes: 11,
      action: '依有完整姓名、親屬連結的圖，判斷人物關係並回答 Who 問句。',
      why: '親屬關係是多重指涉問題，清楚連結圖比無關裝飾圖片有效。',
      support: '避免缺少關係線；正式題必須可唯一判斷，無提示新圖重測。'
    },
    'location-map': {
      label: '物品定位圖｜Where', stage: '空間判斷', minutes: 10,
      action: '看清楚物件數量及相對位置，用 Where 問答指出正確位置。',
      why: '位置語言需要可靠空間證據；實際圖像能直接服務概念。',
      support: '練習時可強調參考物；新圖測驗不加箭頭洩漏答案。'
    },
    'evidence-locator': {
      label: '回文定位｜Evidence', stage: '閱讀證據', minutes: 11,
      action: '先讀核准段落，再標出支持回答的原文；區分直接資訊和推論。',
      why: '閱讀理解的證據來自文本，不能以字彙選擇題代替理解。',
      support: '教師可示範一段；正式獨立題改用未提示的新段落。'
    },
    'sound-chunks': {
      label: '聽音切分｜Sound', stage: '音形連結', minutes: 8,
      action: '先聽目標字正確發音，分辨音節與聲音區塊，再連結字母。',
      why: '若障礙在聲音與拼字形式，先建立可提取的聲音線索。',
      support: '先有音節／字母提示，之後逐次撤除，不以中文諧音取代發音。'
    },
    'active-spelling': {
      label: '無提示拼字｜Retrieve', stage: '主動提取', minutes: 8,
      action: '遮住答案，以聽寫或中文提示提取已教單字，寫完再校對。',
      why: '能從記憶自行拼出字形，比看答案選得出更有診斷價值。',
      support: '練習可先給部分提示；獨立重測改用不同順序與無字形線索。'
    },
    'context-explain': {
      label: '情境判斷｜Explain', stage: '語境遷移', minutes: 9,
      action: '在已核准的新情境中選擇並解釋；先確認情境證據足夠。',
      why: '能說明理由，協助區分規則理解和碰巧猜對。',
      support: '引導時可問找哪個證據；正式重測不給答案方向。'
    },
    'brief-recall': {
      label: '短量無提示提取｜Recall', stage: '獨立提取', minutes: 6,
      action: '不用筆記回想已教內容；教師另備未曝光的新題，避免重做例題。',
      why: '確認提示移除後是否還能主動提取關鍵能力。',
      support: '此活動不得同時展示規則卡或正解。'
    },
    'error-contrast': {
      label: '最小錯例對照｜Repair', stage: '精準補救', minutes: 7,
      action: '只比較一組已確認的核心錯誤與正確用法；聚焦一個差異。',
      why: '先修復實際觀察到的最小能力缺口，避免全課重講。',
      support: '練習後撤除示範，並改用平行新題檢查。'
    }
  });

  const validRoutes = new Set(['core', 'repair', 'extension']);
  const validGoals = new Set(['understand', 'apply', 'retrieve', 'transfer']);
  const validLoads = new Set(['standard', 'reading', 'initiation', 'writing']);
  const validReadiness = new Set(['confirmed', 'partial', 'missing']);
  const validMinutes = new Set([15, 30, 45]);

  function normalize(cfg) {
    cfg = cfg && typeof cfg === 'object' ? cfg : {};
    return {
      topic: Object.prototype.hasOwnProperty.call(topics, cfg.topic) ? cfg.topic : 'custom',
      target: String(cfg.target || '').trim().slice(0, 240),
      source: String(cfg.source || '').trim().slice(0, 300),
      readiness: validReadiness.has(cfg.readiness) ? cfg.readiness : 'missing',
      route: validRoutes.has(cfg.route) ? cfg.route : 'core',
      goal: validGoals.has(cfg.goal) ? cfg.goal : 'apply',
      load: validLoads.has(cfg.load) ? cfg.load : 'standard',
      minutes: validMinutes.has(Number(cfg.minutes)) ? Number(cfg.minutes) : 30
    };
  }

  function recommend(settings) {
    const cfg = normalize(settings);
    const topic = topics[cfg.topic];
    const missing = [];
    if (cfg.readiness === 'missing') missing.push('確認原始／正式教材是否可用。');
    if (!cfg.source) missing.push('補上來源名稱與頁次／範圍。');
    if (!cfg.target) missing.push('確認本次要達成的學習目標。');
    if (missing.length || cfg.readiness === 'missing') {
      return {
        blocked: true, status: 'BLOCKED', settings: cfg, activities: [],
        gaps: missing.slice(0, 3),
        explanation: '來源或目標尚未足以支持活動設計。此狀態不產生正式題目或目標。'
      };
    }
    let ids = [...topic.primary];
    if (cfg.topic === 'custom') {
      const customByGoal = {
        understand: ['compare-subject'], apply: ['sentence-apply'],
        retrieve: ['brief-recall'], transfer: ['context-explain']
      };
      ids = customByGoal[cfg.goal];
    }
    if (cfg.route === 'repair') {
      if (cfg.topic === 'spelling') ids = ['sound-chunks', 'active-spelling'];
      else if (cfg.topic === 'reading') ids = ['evidence-locator'];
      else ids = ['error-contrast', ids[0]];
    }
    if (cfg.route === 'extension') {
      ids = cfg.topic === 'spelling' ? ['active-spelling'] :
            cfg.topic === 'reading' ? ['evidence-locator', 'context-explain'] :
            [ids[ids.length - 1] || 'context-explain', 'context-explain'];
    }
    if (cfg.goal === 'retrieve' && cfg.route !== 'extension' && cfg.topic !== 'spelling') {
      ids = [...ids, 'brief-recall'];
    }
    if (cfg.goal === 'transfer' && !['spelling', 'reading'].includes(cfg.topic)) {
      ids = [...ids, 'context-explain'];
    }
    const maxCards = cfg.minutes === 15 ? 1 : cfg.minutes === 30 ? 2 : 3;
    ids = [...new Set(ids)].slice(0, maxCards);
    const supports = {
      standard: '維持清楚層級，隨學習證據調整。',
      reading: '減少非目標文字，必要時分段朗讀指令；不能朗讀閱讀評量所測內容。',
      initiation: '先提示第一步、一次只顯示當前任務；開始後逐步撤除起始提示。',
      writing: '加大書寫空間，減少非必要抄寫；目標若是拼字不可代寫。'
    };
    const routeNotes = {
      core: '完成核心學習與應用；支援移除後再收集獨立新題證據。',
      repair: '只處理已觀察到的最小缺口；若原因未確認，先用新題複查，勿直接認定能力不足。',
      extension: '減少重複演練，優先加入遷移與理由說明；不得自動宣告已掌握。'
    };
    return {
      blocked: false,
      status: cfg.readiness === 'confirmed' ? 'TEACHER-DECLARED SOURCE' : 'READY WITH LIMITS',
      settings: cfg,
      topic: topic.label,
      activities: ids.map(id => ({id, ...activities[id]})),
      omitted: topic.omitted,
      transfer: topic.transfer,
      support: supports[cfg.load],
      routeNote: routeNotes[cfg.route],
      evidence: [
        '練習階段可以使用必要支援，但需記錄提示來源。',
        '正式獨立證據：撤除目標相關提示，使用未曝光的新題；答對例題不算。',
        '延後保持：按實際提取結果安排延後、無提示的新題，記錄間隔。'
      ],
      limitations: '僅供教師設計草案。來源狀態為教師自述，系統未驗證課本內容；題目、答案、正式發行需另通過 Content／Lexical／Pedagogy Lock 與 Release QA。'
    };
  }

  return Object.freeze({topics, activities, normalize, recommend});
});