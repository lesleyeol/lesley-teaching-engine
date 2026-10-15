# Starter–Unit 2｜教材視覺層 v0.2（待審核）

**狀態：DRAFT_FOR_TEACHER_REVIEW｜視覺排版修訂，不是教學內容或正式發行核准。**

## 工具來源與實際採用

先讀取本儲存庫 PR #4 的 `toolkit/visual-design/README.md`、`AGENTS.md`、`VERIFICATION.md` 和 `source-lock.json`。其中收藏的是原始碼及選用規則，**不等於已安裝的八套工具**。

| 工具 | 本次真正採用 | 明確限制 |
|---|---|---|
| **Radix Colors** | 從 `radix-ui/colors` 固定 commit `dbdb85470547c7d34b9001f48fddb08ded335979` 的 `src/light.ts` 讀取 `slate1–slate12`，納入 `visual_design.css`，建立紙本與手機共用色階 | 使用來源色票，非在執行環境安裝 Radix Primitives；黑白列印仍以邊框、線條、字級區別 |
| **Fontsource** | 依工具庫字集／字重原則決定 `Noto Sans TC → Noto Sans CJK TC` 繁中文字型回退與 Clear Sans 英文顯示，並以已安裝字體完成 PDF 渲染 | 本專案 **沒有安裝、傳遞或包裝 Fontsource 字體二進位檔**；在其他裝置字型可由系統備援 |
| **Mermaid** | 在 `STARTER_UNIT2_RELATION_MAP.md` 使用 GitHub 原生支援的 Mermaid 程式圖定義教學知識關聯 | 這是教師用可編輯的知識圖，不更動學生頁題目，也不是 3D 圖 |
| Rough.js、shadcn/ui、Simple Icons、README Stats、Markdown Badges | **沒有加入教材渲染** | 手繪干擾書寫格線、UI 框架與品牌／統計元件對 A4 紙本任務沒有直接助益 |

## 已做的排版改進

- **學生題目字級設 13.5 pt**，中文用清晰無襯線字體，英文項目採可讀性高的字型回退。
- **英文書寫格線**：四條書寫參考線（頂線、中線、基線、下緣），並讓字母大小寫練習特別使用四線格；其餘短答仍保留實際可書寫的底線。
- **有意義的並排對照**：只把原有引導頁的 `I–am / he/she/it–is / you/we/they–are` 與近遠指示詞規則拆成比較格；沒有新增例題或提前揭露獨立題答案。
- **單元層次**：標題、學生作答、提示規則、圖表和頁碼使用單一語意色階；灰階列印仍可理解。
- **自動平衡分頁**：依每類活動需要的書寫空間減少每頁題數；避免最後一頁只剩一題，維持同一章節順序及原始題號。
- **手機／iPad**：螢幕版變成閱讀寬度自適應，PDF 列印固定 A4；無外部 CSS、CDN 或載入時 API。

## 教學與來源內容不變

- 使用 PR #9 的同一份 `unit_scope_item_bank.json`（46 項知識點，185 題，65 詞）；沒有修改任何 `prompt`、`answer`、`rationale`、`diagnosis`、Source Lock 或 Gate。
- 獨立 Check 與 Delayed 繼續在**教師保管**的不同檔案；不與立即練習混合。
- 採「提示可見只算練習，提示撤除、新題重測才可形成獨立證據」；音檔缺口仍標示 AUDIO_PENDING。
- PR #8 已保留的 16 題原始文字與答案完全不動。
- 源教材為使用者上傳的課本內容，**不把原課本掃描與已批改學生筆跡推送到公開 GitHub**。

## 完成的 QA（本機）

| 檢查 | 目前結果 |
|---|---|
| 11 份 HTML 以原始共同題庫重新生成 | 通過 |
| 原題 `code + prompt` 顺序與文字不變 | 通過 |
| 全部 A4 PDF 實際輸出 | 11／11 |
| 頁面 overflow / clipped body | 0 |
| 手機 390px、平板 834px 橫向溢出 | 0 |
| 學生總本／教師完整版 | 27 頁／38 頁 |
| 教師保管獨立新題／延後卡 | 10 頁／4 頁 |
| 文字拼讀與聽辨證據 | **仍待官方音檔／教師現場紀錄** |
| 現行課本版次、正式 Gate、班級施測及正式 Release QA | **尚未完成** |

頁數比前版增加，是書寫區與字級提升後所需的真實分頁；沒有因為追求少頁而縮小到不可寫或截斷題目。實機 iPhone／iPad Safari 的實際檔案列印尚未測試，瀏覽器測試只代表 Chromium 模擬尺寸的結果。

## 重現（開發者用，不是要求教師操作）

```bash
python tools/full_starter_u2/render_visual.py
python tests/test_visual_pack.py
```

渲染結果在 `tools/full_starter_u2/output_visual/*.html`，而不是覆寫原先 `output/*.html`。PDF 需本機或 CI 的 Chromium 列印驗證環境；視覺 QA 來源與測試結果在交付 ZIP 中，**不能把程式可運作解讀為學生學會**。

## 下一 Gate

教師核對實際課本版次、學習範圍與正式單元規格，完成 Student／Teacher／Answer 完整 Release QA、必要的實際列印與學生支援觀察後，才能討論正式發行。