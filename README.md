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

## Privacy

- Data is stored locally in the browser.
- Use student aliases/codes rather than sensitive personal information.
- Export JSON backups regularly.
- This public repository contains app code only; it does not contain student records.
