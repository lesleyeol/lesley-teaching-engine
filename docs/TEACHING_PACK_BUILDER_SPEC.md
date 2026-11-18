# Teaching Pack Builder｜實作規格與契約試行 v0.1

狀態：**DRAFT / engineering contract pilot**。本文件是 Skill Spec 的工程草稿，不是已安裝 Skill，也不是正式教材發布核准。

## 目的與既有邊界

將既有教材產製流程封裝成可追溯、可回歸測試的工作流。沿用原有 Source → Guardrail → Execution → Structured Output → Schema Validation → QA → Render → Export → Run Log 流程；不建立新架構。

完整 v0.1 目標仍為 Student Pack、Teacher Guide、Answer Key、QA Report。Dashboard、自動家長報告、Wordwall/Kahoot 自動化、新 MCP 及 ChatGPT App UI 不在本階段範圍。

## 三份基準的分工

本次直接讀取原始資產的完整文字；沒有修改它們：

| 基準 | 使用方式 | 不應推論 |
| --- | --- | --- |
| Exercise Your Grammar One-to-One Master Template v1.0，第 2–6 頁 | 保留 20 個功能槽、route/scope 對齊、開放題 rubric、分項門檻、來源標示及 QA | 兩種結構壓力測試不等於三個真實 Unit 已驗收 |
| EYG1 Unit8 Integrated Master Pack v2.0，第 2–5、10–12 頁 | 作 Unit 8 的 Gate、Feedback、No-Support、診斷及版本一致性參考 | 不把 Unit 8 的 6 題、4/5 等條件直接套用其他 Unit |
| LESLEY_TEACHING_ENGINE_v2.4_STABLE.md，§4–5、13、18–19、24、27、29–30 | 管理目前的來源、獨立證據及發行政策；區分教材產製與學生學習證據 | Core 的 Stable 不等於每份教材已通過實際授課驗證 |

v2.4 §29–30 明定：固定 Day 1/Day 3 與至少 30% 新題不作全域硬規則；Gate 題數由能力覆蓋決定。這些是已存在的 Core 政策，不是本 PR 新增的規則。Unit 8 的原題、答案及原分項門檻不因此自動重寫。

來源角色若發生同層級衝突，記錄衝突並停止受影響的正式發行；不要憑版本數字、檔案日期或模型記憶自行裁決。

## 已有實作 → 封裝對應

| 功能 | 可重用檔案 | 現況／缺口 |
| --- | --- | --- |
| Source / Scope / Pedagogy Lock | curriculum/starter/subject-be.manifest.json | 限定 Starter 主格與 be 肯定句；來源及正式 Gate 未核准 |
| 同源學生、教師、答案與延後輸出 | tools/build-starter-pack.cjs、subject-be.items.json | 四份 HTML 從同一題目資料產生；renderer 有固定標題、規則表、題號及詞彙，因此不能聲稱支援任意 Unit |
| 來源、題目、洩漏及拒絕發行檢查 | tests/starter-pack.test.cjs | 29 項既有測試；保留不改 |
| 活動規則 | demos/adaptive-lesson-rules.js、tests/adaptive-lesson-rules.test.cjs | 18 項測試，僅活動設計規則；不是教材包完整驗收 |
| Starter–Unit 2 題庫與產製 | tools/full_starter_u2/、tests/test_starter_u2_bank.py | 46 知識點、185 題、65 詞彙、16 原題保留；只是另一個受限產製路徑，尚未接通此契約 |
| Input / Output contract | schemas/teaching-pack-builder.*.schema.json | 本 PR 新增，限定既有 Starter adapter；通用化仍待後續整合 |
| 成功／失敗 fixtures | tests/fixtures/teaching-pack-builder/cases.json | 基於既有資料的合成變異；不複製私人原始教材，不算真實 Unit 驗收 |
| 契約檢查與 QA | tools/check_teaching_pack_contract.py | 結構檢查後呼叫原 builder；不寫學生檔、不正式發行 |
| Installable Skill | /skills/teaching-pack-builder/SKILL.md | **仍未建立**；本文件僅是封裝規格 |

## 試行契約的操作方式

執行環境：Node.js 18+、Python 3.11+、jsonschema 4.25.1。新 CI 的依賴有固定版本。

```sh
python -m pip install jsonschema==4.25.1
python tools/check_teaching_pack_contract.py
python tests/test_teaching_pack_contract.py
```

- 不指定輸入：讀取 repo 中既有 Starter manifest 及 item map。
- 自訂輸入：`--input request.json`，JSON 根層僅接受 `manifest` 與 `item_map`。
- 此 adapter 只支援既有 Starter 主格與 be 配對。Unit、學習目標與 scope 改變時拒絕執行，不把錯誤目標套進固定 renderer。
- Exit 0：契約檢查通過，仍為 DRAFT_FOR_TEACHER_REVIEW。
- Exit 2：輸入無效、來源／教學檢查失敗、執行失敗等，輸出 BLOCKED 且 artifact_names 為空。
- 結果包含 status、errors、warnings、counts、artifact_names、validation_scope、release_authorized。artifact_names 僅表示本次在記憶體內產生的四個 HTML 名稱，**不是已寫入或已匯出的檔案**。
- `release_authorized` 永遠為 false。即使輸入自行把核准旗標改為 true，檢查仍不能授權正式發布。
- JSON Schema 只檢查結構與明列限制；語意正確性、來源真實性、獨立證據品質、教室可用性仍須獨立核對。

## 後續可安裝 Skill 的行為規格

1. 先辨識 AUDIT／REVISION／BLUEPRINT／GENERATION／PRODUCTION，保留本次授權範圍。
2. 讀取當期 Core、模板、Unit Manifest 及原始來源；記錄版本與可回查頁次。來源若 BLOCKED，不定義正式 Target、Gate、題目或答案。
3. 核對 Scope、Lexical Source Lock 與 Pedagogy Lock；缺漏時只輸出受限草稿及必要缺口。
4. 先核准學生題目資料，再由同一份 item map 推導答案與教師版；保留 route、分項門檻、No-Support、平行新題與延後提取的證據界線。
5. 選已驗證 adapter。此試行只能處理 Starter subject-be，其他 Unit 不能聲稱已支援。
6. 跑契約、來源、跨版本一致性及洩漏檢查；失敗輸出不得進正式記憶。渲染及匯出後另驗排版、中文字型、灰階與裝置可用性。
7. QA Report 分開記錄程式測試、來源、教學、Release QA、實際授課與裝置驗收；附版本、失敗原因及下一步，不使用單一 PASS 取代全部維度。

## 保留原 Definition of Done

1. 至少 3 個真實 Unit 測試成功。
2. Student／Teacher／Answer Key 無衝突。
3. 核心題沒有提示洩漏。
4. Gate 與 No-Support Check 可獨立執行。
5. 輸出可直接上課，不需大幅重寫。
6. 修改後可跑回歸測試。
7. 失敗原因與版本可追溯。

本 PR 僅補契約、fixtures、檢查入口及 Spec，保留原程式與教材。以上完整驗收仍未完成。Starter、Unit 1、Unit 2 出現在同一題庫中，不能直接計為三個 Unit 全部通過。

## 下一個工程缺口

- 將通用模板的完整功能映射到可執行 Unit adapter，補 prerequisite、route-specific homework、quiz/rubric、lesson record、Gate／No-Support 的獨立入口。
- 把來源真實性、授權用途、答案曝光、lexical 分類、教學證據及人工 QA 納入通用契約；不能把本 PR 的 pilot schema 改名就當通用契約完成。
- 核對三個真實 Unit 的當期原教材、版次與已教內容，再依同一標準跑完整驗收。
- 個人 Skill 的建立／安裝依當期 Skill 管理入口處理；不以 repo 中有一份 Spec 宣稱已安裝。

原 MCP 導入 Gate、ChatGPT App 導入 Gate 與 Engineering Guardrails 保留。本 PR 不新增 MCP、不改 Core、不發行教材。

## 2026-11-18｜本次執行證據

基底：main `9a47984af177b0d8bd446660a1c5d60e668d058b`。

| 檢查 | 本次結果 | 可支持的結論 |
| --- | --- | --- |
| node tests/starter-pack.test.cjs | 29 tests passed | 既有 Starter 程式回歸通過 |
| node tests/adaptive-lesson-rules.test.cjs | 18 tests passed | 既有活動規則回歸通過 |
| python3 tests/test_starter_u2_bank.py | PASS | 46 知識點、185 題、65 詞彙、16 原題一致性檢查通過 |
| node tools/build-starter-pack.cjs --check | errors 為空，6 則 warnings | 草稿來源檢查通過；正式來源及發行缺口仍在 |
| python3 tests/test_teaching_pack_contract.py | 6 個測試方法通過，其中一項執行 12 個 fixtures | 新契約成功／拒絕路徑、結果結構與 CLI 失敗處理通過 |
| python3 tools/check_teaching_pack_contract.py | DRAFT_FOR_TEACHER_REVIEW、release_authorized=false | 現有試行可通過契約；沒有正式發布授權 |
| python3 tools/full_starter_u2/author_data.py 重複產製 | 連續產製 bytes 相同，且與讀取的上游 JSON 語意相同 | 本機資料產製可重現；不是教材語意或 Release QA |

本次沒有重新執行 PDF 渲染／列印 QA、手機互動驗收、三個真實 Unit 完整驗收或實際授課。新工作流的 GitHub 執行狀態需另看本 PR Checks；上述是本機執行紀錄。
