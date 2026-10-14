# 來源收藏驗證結果

核對日期：2026-10-06（Asia/Taipei）。

## 結論

八個專案的來源快照已下載、驗證並保存至 GitHub Release。這不是八套已安裝／整合的應用程式。

- 官方專案：8／8。
- 來源 ZIP：8／8，雜湊、檔案大小、ZIP CRC 與檔案數核對通過。
- 收錄來源檔案：22,807。
- 個別來源 ZIP 合計：59,878,955 bytes。
- Release 附件：12 個，發布後已核對名稱、上傳狀態與非零大小。
- 未進行：npm 依賴安裝、應用功能整合、網站發布、瀏覽器／iPad 功能測試或完整資安審查。

## 已完成的三層檔案核對

1. 下載工作以各專案明確 commit 下載來源，產生 SHA-256 與 CRC 驗證報告。
2. 取回原始 artifact 後，在獨立執行環境重算外層 ZIP 雜湊，逐一核對八個內層 ZIP 的雜湊、大小、CRC、檔案數、授權檔存在及字體二進位檔排除。
3. 版本保存工作重驗來源報告 SHA-256 與所有來源 ZIP，再發布至 Release，並確認 12 個附件全部 uploaded。

雜湊與 CRC 核對只證明此次檔案的完整性與一致性，不能證明程式安全、穩定或適用。

## 版本與附件

[開啟版本下載頁](https://github.com/lesleyeol/lesley-teaching-engine/releases/tag/visual-toolkit-sources-2026-10-06)

- Release ID：403931566。
- 標籤：`visual-toolkit-sources-2026-10-06`。
- 標籤指向：`915c390704c193c2deae787e208a71c434659043`，工具庫獨立分支的版本保存工作 commit。
- `prerelease=true`，建立時明確 `latest=false`，不代表正式教學引擎更新。
- 附件包括：八個個別專案 ZIP、`visual-toolkit-eight-sources.zip`、`download-report.json`、`README.txt`、`SHA256SUMS.txt`。
- Release 不使用 Actions artifact 的 90 天自動到期機制；不承諾在 repository 或 release 被刪除後仍可取得。

工具庫指南是在獨立分支持續更新的檔案；Release 標籤是固定來源保存版本，兩者用途不同。

## 來源核對摘要

| 專案 | 收錄檔案 | 排除檔案 |
|---|---:|---:|
| Rough.js | 79 | 0 |
| shadcn/ui | 5,852 | 0 |
| Radix Colors | 20 | 0 |
| GitHub README Stats | 132 | 0 |
| Mermaid | 3,231 | 1 個符號連結 |
| Simple Icons | 3,528 | 1 個符號連結 |
| Fontsource | 9,948 | 12 個字體二進位測試檔 |
| Markdown Badges | 17 | 0 |

所有來源包保留原始授權文件；Fontsource 的程式庫授權不等於所有字體共用同一授權，Simple Icons 的開源授權也不等於任意品牌使用許可。

來源為當時預設分支的 commit；正式整合應另行選擇相容發行版本。GitHub README Stats 原專案官方 README 宣告不再維護，本庫保留作備查，不作新部署預設。

## 可追溯資料

[下載工作：success](https://github.com/lesleyeol/lesley-teaching-engine/actions/runs/37342614754)

[版本保存工作：success](https://github.com/lesleyeol/lesley-teaching-engine/actions/runs/37343559855)

[八個專案的固定 commit 與來源雜湊](source-lock.json)

原始 Actions artifact ID：`11359550618`；大小：59,891,998 bytes；SHA-256：`44b4e9fa22f44639a45ed321fa87c0154a870ef4b2864fce945797397ddf4649`。

`download-report.json` SHA-256：`c035ec9772c5d777c84bd0778f258c5493bbbc7b18a7a7ba64ab5f7b163b8953`。

注意：Release 的八合一包重新打包過，外層雜湊不必與 Actions artifact 相同；八個內層來源 ZIP 與來源報告已按原始雜湊核對。請用下載頁的 `SHA256SUMS.txt` 核對 Release 附件。
