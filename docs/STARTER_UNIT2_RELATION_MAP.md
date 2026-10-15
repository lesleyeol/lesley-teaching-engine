# Starter → Unit 2｜教學知識關聯（教師用可編輯圖）

此圖僅以已列入來源對照的內容表示學習依存關係。**不是固定教學順序，也不是學生已通過證據。** 題目、答案及正式 Source Lock 以題庫及目前 v2.4 Stable 為準。

```mermaid
flowchart TB
  subgraph S["Starter｜先備技能"]
    L["字母大小寫／短母音（聽辨待音源）"]
    P["主格／所有格代名詞"]
    B["am · is · are"]
    N["What ... name?／How old ...?"]
    W["數字與書寫格式"]
    P --> B
    B --> N
    W --> N
  end
  subgraph U1["Unit 1｜人物與家庭"]
    F["家庭／職業詞彙"]
    WHO["Who 人物問句與身分"]
    BE["be 肯定／否定／Yes-No 簡答"]
    READ1["家庭介紹閱讀找證據"]
    F --> WHO
    F --> READ1
    B --> BE
  end
  subgraph U2["Unit 2｜物品與位置"]
    V["文具與房間詞彙"]
    PL["名詞複數與例外"]
    DEM["this／that／these／those"]
    WHERE["Where + 位置介系詞"]
    READ2["空間描述閱讀"]
    PL --> DEM
    B --> DEM
    DEM --> WHERE
    V --> WHERE
    WHERE --> READ2
  end
  P --> WHO
  N --> WHO
  BE --> WHERE
```

## 兩條不能混淆的證據路徑

```mermaid
flowchart LR
  G["帶提示練習"] --> R["撤除目標相關提示"]
  R --> I["未曝光新題：獨立應用"]
  I --> T["改變情境：遷移"]
  T --> D["另日無提示新題：延後提取"]
  D --> E["再由教師判定證據"]
```

- `AUDIO_PENDING`：短母音、清濁音與複數字尾的真正聽辨，需音源與口語紀錄。
- Unit 1 的 `-er` 構詞屬 Extension，是否使用依已教狀態決定。
- 本圖刻意不加入課本尚未確認的外延知識點。