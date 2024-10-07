# BBForum

![封面照](https://hackmd.io/_uploads/Bk-kgivCA.png)

#### 專案網址: https://www.bbforums.org/

#### Demo Day 精彩回顧: https://www.youtube.com/watch?v=OP9BuUl0Bb8&t=118s

#### 簡報介紹: https://drive.google.com/file/d/1WQABkqR4qFOaNbBr-cRyePNV6vtLcVix/view?usp=drive_link

## 專案構思

「**BBForum**」是一個專為股票投資者打造的交流平台，無論是新手還是資深投資者，都能在這裡找到志同道合的夥伴。通過真實的市場分析和即時更新的股票資訊，幫助投資者在複雜的股市中做出更明智的決策。加入討論、共同學習，一起成長，掌握投資的每一步！

## 專案特點

- **即時股市討論區**: 用戶可以隨時參與各類股市話題的討論，與其他投資者交換心得，分享個人投資策略。
- **股票資料流通**: 網站提供股票資料的快速檢索功能，方便用戶查找最新的股票數據、技術分析、及市場趨勢。
- **會員積分系統**: 用戶可以透過參與討論、分享有價值的內容來獲取積分。

## 功能回顧

![功能回顧＿會員機制](https://hackmd.io/_uploads/HyabuMWyyx.png)
![功能回顧＿發文留言](https://hackmd.io/_uploads/HkdmOMZ1yx.png)
![功能回顧＿收藏追蹤](https://hackmd.io/_uploads/rkL-KzWyJl.png)

## 安裝環境

```
1. git clone https://github.com/astrocamp/17th-BBForum.git (將專案複製到本地)
2. cd 17th-BBForum (進入專案目錄)
3. poetry shell (進入虛擬環境)
4. poetry install (安裝 Poetry 相關套件)
5. npm i (安裝 npm 相關套件)
6. 建立.env(設定環境變數)
```

## 執行環境

```
1.前端：
  Win: npm run dev:win
  Mac: npm run dev:mac

2.後端：
  Win: python manage.py runserver
  Mac: make server
```

## 技術棧

- **前端技術**: Tailwind CSS、daisyUI、Alpine.js、HTMX
- **後端技術**: Python、Django
- **網站部署**: Heroku
- **其他技術**:
  - **版本控管**：Git、GitHub
  - **郵件服務**：Mailgun
  - **資料庫**：PostgreSQL
  - **文件儲存與管理**：AWS S3
  - **認證與第三方登入**：Google、LINE

## 專案團隊

- 康詠晴 [GitHub](https://github.com/KANG0918)
  - 會員一般登入
  - GOOGLE、LINE 第三方登入
  - 討論區文章按讚功能
  - 討論區文章 Tag 功能
  - 大盤及個股的及時走向分析
  - 爬蟲、文字雲
- 徐國傑 [GitHub](https://github.com/EricHsu521)
  - 討論區發文留言
  - 個股股票自選
  - 全站網頁切版
  - 網站流程優化
  - 網站部署
  - 股票 K 線圖分析
- 王懿娟 [GitHub](https://github.com/emma0620)
  - 會員個人資料
  - 會員階級功能
  - 分享超連結
  - 圖片 S3 雲端上傳
- 楊聯崧 [GitHub](https://github.com/LianSongYang)
  - 熱門同學資料渲染
  - 貼文收藏功能
  - 搜尋功能
- 蘇臻君 [GitHub](https://github.com/jenjiunsu)
  - 會員點數
  - 全站 RWD 切版
  - 會員帳號軟刪除
  - 簡報製作與報告
