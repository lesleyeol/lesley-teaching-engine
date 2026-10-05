# 視覺設計工具庫｜先說需求，再選工具

整理日期：2026-10-06。這是獨立分支中的工具收藏與選用指南，不改動已上線的教學引擎。

## 從這裡看成果

[八個專案的下載工作與原始碼壓縮包](https://github.com/lesleyeol/lesley-teaching-engine/actions/runs/37342614754)

開啟上面的 GitHub 工作頁，查看執行結果；在 Artifacts 區下載 `visual-toolkit-eight-sources`。請以工作實際狀態與包內 `download-report.json` 為準，不把建立工作等同於下載成功。

原始碼包的保留期限設定為 90 天，並非永久備份。正式驗證後的版本編號會保留在本資料夾的來源鎖定記錄，供之後查找原版本。這些是來源快照，不是已安裝在 iPad 的八個 App，也沒有將八套依賴灌入現有教學程式。

## 你說什麼，我應該選什麼

| 需求 | 優先考慮 | 怎麼用在你的工作 | 必須分清楚的限制 |
|---|---|---|---|
| 手寫圖解、文法框線、草圖箭頭 | **Rough.js** | 以手繪感外框與連線呈現概念 | 它負責繪圖風格，不替你檢查文法或安排所有節點 |
| 手機操作頁、表單、卡片、頁籤 | **shadcn/ui** | 建構可操作的網頁介面 | 是可取用和修改的元件程式碼；要配合框架，不直接塞進舊單檔 HTML |
| 統一配色、淺色／深色介面 | **Radix Colors** | 定義背景、邊線、按鈕與文字色階 | 是色彩系統，不是 Radix Primitives；仍須檢查實際文字對比 |
| GitHub 個人介紹頁統計卡 | **GitHub README Stats：備查** | 僅供 GitHub 活動統計卡參考 | 官方已聲明不再維護；不是保費、教學成績或營收儀表板 |
| 心智圖、關係圖、工作流程 | **Mermaid** | 先把概念或流程畫清楚，保留可編輯文字來源 | 不是自動生成立體 3D 互動圖的引擎 |
| 工具／平台的品牌標誌 | **Simple Icons** | 在工具整合說明中辨識平台 | 是品牌圖標，不是任意類型插圖；使用前查品牌聲明 |
| 網頁中文字體／英文字體的來源與配置 | **Fontsource** | 按實際語言、字重與用途選字體 | 本工具庫不附字體二進位檔；要按個別字體確認字集與授權 |
| README 徽章、技術標籤 | **Markdown Badges** | 標示真正的技術、版本或狀態 | 是徽章範例集合，不是成績或證書系統；禁止虛構通過測試狀態 |

以上是針對本工具庫用途的選用建議；功能說明以各專案官方來源為依據。

## 常見組合

**文法心智圖：** 先用 Mermaid 整理關係；只有需要手繪外觀時才考慮 Rough.js。依成品形式決定是否需要兩者，不為了收藏齊全而強行疊加。

**教材／學習網頁：** 先確認是否真的要新的操作介面；需要且架構合適時採 shadcn/ui，配色再採 Radix Colors。Fontsource 只在系統字體不能满足需求時加入；列印講義仍以清晰、黑白可讀、內容正確為先。

**工作流程說明：** 先用 Mermaid 呈現收件、判斷與下一步；要呈現平台名稱時再用 Simple Icons。畫出 LINE 等平台圖示不代表已取得訊息存取或完成串接。

**GitHub README：** Markdown Badges 只標示真實狀態；需要活動統計才查 README Stats 官方列出的延續專案，原專案不作新部署預設。

## 八個已核對的官方來源

| 名稱 | 原始碼 | 官方使用入口 |
|---|---|---|
| Rough.js | [rough-stuff/rough](https://github.com/rough-stuff/rough) | [roughjs.com](https://roughjs.com/) |
| shadcn/ui | [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | [安裝說明](https://ui.shadcn.com/docs/installation) |
| Radix Colors | [radix-ui/colors](https://github.com/radix-ui/colors) | [色階用途](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale) |
| GitHub README Stats | [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | [官方停止維護公告與延續專案入口](https://github.com/anuraghazra/github-readme-stats#github-readme-stats) |
| Mermaid | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | [官方 README](https://github.com/mermaid-js/mermaid#readme) |
| Simple Icons | [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons) | [官方 README 與使用聲明](https://github.com/simple-icons/simple-icons#readme) |
| Fontsource | [fontsource/fontsource](https://github.com/fontsource/fontsource) | [官方字體目錄](https://fontsource.org/) |
| Markdown Badges | [Ileriayo/markdown-badges](https://github.com/Ileriayo/markdown-badges) | [官方徽章範例](https://github.com/Ileriayo/markdown-badges#readme) |

星數會變動，故不當作固定事實或選用門檻。README Stats 的原始庫仍保留，沒有擅自用另一個專案冒充原項目。

## 下載與驗證做了什麼

下載工作對每個專案先取得預設分支的 commit，再下載該 commit 的來源 ZIP，記錄來源網址、commit、日期、SHA-256、檔案數、排除清單並驗證 ZIP CRC。預設分支快照不等同經測試的穩定版；正式整合時另選相容發行版本。

所有來源包均排除字體二進位檔及符號連結，原有授權文件保留。沒有執行來源庫的安裝腳本、沒有開放新網站、沒有新增秘密金鑰，也沒有修改 main、Gate 或既有教材規則。檔案下載與 CRC 通過不等於資安稽核、瀏覽器相容性或功能測試通過。

## 後續交付標準

日後使用時，回覆以「用途、推薦工具、產出形式、已完成／未完成」為主，不要求使用者記內部代碼或執行終端機指令。每次只加入必要工具，正式整合使用獨立分支及可驗證結果。

給後續開發助理的選用規則見 [AGENTS.md](AGENTS.md)。該規則只在本資料夾及被明確引用的工作中適用，不代表所有新對話都會自動載入，也不取代教學引擎既有規範。
