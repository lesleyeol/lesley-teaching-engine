# Lesley Teaching Engine

Mobile-first offline PWA for teaching records, learning gates, error logging, weakness tracking, reports, and local backup.

## Live site

https://lesleyeol.github.io/lesley-teaching-engine/

## Adaptive Lesson Design（設計提案）

教學活動依 **正式教材、學習目標、學生需求與證據要求** 選擇，不強制每課套用 Look & Find、Noun Detective、One or Many、Brain Check 四個活動。

- [適性課程設計規範與驗收情境](docs/ADAPTIVE_LESSON_DESIGN.md)
- 此連結為**設計規格**，不是已上線的自動教材生成器。
- 正式來源與教學／評量規則仍以 **Lesley Teaching Engine v2.4 Stable Core** 為準。

## Adaptive Lesson Designer（操作原型）

- [開啟適性課程設計示範頁](demos/adaptive-lesson-designer.html)
- [操作說明與測試範圍](docs/ADAPTIVE_LESSON_PROTOTYPE.md)
- 依教學目標、時間及需要的支持選活動；可手動增刪、排序，並列印 A4 教師草案。
- **僅為 BLUEPRINT／草案工具**，不自動產生正式學習單、題目或核准證據；來源仍須教師核對，正式發行仍須完成 Teaching Engine v2.4 Stable 的 QA。

## Source-bound Starter Unit Pack（限定範圍教材示範）

- [來源治理、教學證據及操作說明](docs/STARTER_SOURCE_TO_PACKET.md)
- [學生 A4 預覽](examples/starter-be/student.html) · [教師指引](examples/starter-be/teacher.html) · [答案解析](examples/starter-be/answer.html) · [延後複查卡](examples/starter-be/delayed.html)（公開示範題，**不作保密正式測驗**）
- [題目與答案共用資料](curriculum/starter/subject-be.items.json) · [來源範圍與教學鎖定](curriculum/starter/subject-be.manifest.json)
- 使用 `node tools/build-starter-pack.cjs --check` 檢查來源限制、`node tests/starter-pack.test.cjs` 執行測試，再用 `node tools/build-starter-pack.cjs` 生成 A4 HTML 預覽。
- **本版本仍是待教師審閱的 DRAFT**：課本版次、正式教師核准與 Release QA 未完成，不得宣稱學生已獨立掌握或正式教材已發布。

## Starter–Unit 2｜全範圍來源對照與教材草稿

本次提供以正式課本掃描**可核對部分**為基礎的完整範圍對照：**46 個知識點、185 題練習／檢核／延後提取，以及 Unit 1＋2 的 65 項 Word Bank**。舊版 Starter be 16 題原文及答案保持不變。

- [知識點逐項對照與題號追溯](docs/STARTER_UNIT2_KNOWLEDGE_MATRIX.md)
- [來源、限制、列印與 QA 紀錄](docs/STARTER_UNIT2_FULL_PACK_QA.md)
- [原始題目資料與來源鎖定](tools/full_starter_u2/unit_scope_item_bank.json)
- [建立及檢查 A4 學生／教師／答案版的程式](tools/full_starter_u2/render_pack.py)
- [離線資料核驗](tests/test_starter_u2_bank.py)

**發行狀態：DRAFT_FOR_TEACHER_REVIEW / READY_WITH_LIMITS。** 請勿把此 PR 視作已核准正式學生考卷，也不得把文字拼讀練習當作官方音檔的聽力證據。正式版次、已教進度、音檔及完整 Release QA 尚未確認；此版不會自動覆寫既有 PWA 的學生紀錄。

### A4 視覺改版 v0.2｜可列印、可手機閱讀（待教師審核）

- [視覺設計與 QA 紀錄](docs/STARTER_U2_VISUAL_GUIDE.md) · [Mermaid 教師關聯圖](docs/STARTER_UNIT2_RELATION_MAP.md)
- [新版視覺樣式](tools/full_starter_u2/visual_design.css) · [同源重排生成器](tools/full_starter_u2/render_visual.py)
- 本次僅選用 PR #4 工具庫的 **Radix Colors** 色階、**Fontsource** 字體選用原則、**Mermaid** 關聯圖；不強制整合八項工具。
- **13.5 pt** 學生題目、四線書寫格、按單元意義分隔規則、可自適應的螢幕閱讀頁；A4 黑白影印仍為優先。
- **不修改** PR #9 的共同題庫（46 項知識點、185 題、65 項單字）、答案、來源、Gate 或學生私有紀錄；新版在 `output_visual/` 建立，不覆寫原始教材。
- 此改版只完成**視覺 QA 草稿**，不代表正式來源已核定或學生已學會。PDF 預覽與完整包從 ChatGPT 交付，不將課本照片或個資上傳此公開儲存庫。

## Privacy

- Data is stored locally in the browser.
- Use student aliases/codes rather than sensitive personal information.
- Export JSON backups regularly.
- This public repository contains app code only; it does not contain student records.
