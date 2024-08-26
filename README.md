# BBForum Team
- 康詠晴 https://github.com/KANG0918
- 蘇臻君 https://github.com/jenjiunsu
- 王懿娟 https://github.com/emma0620
- 楊聯崧 https://github.com/YangLianSong
- 黃凱安 https://github.com/cliffmov
- 徐國傑 https://github.com/EricHsu521

# 下載與安裝步驟
1. `git clone https://github.com/astrocamp/17th-BBForum.git`
2. `cd 17th-BBForum`
3. `poetry shell`
4. `poetry install`
5. `npm i`
6. 複製`.env.example`，更名為`.env`

# 執行步驟
1. Win: `npm run dev:win`
   Mac: `npm run dev:mac`
2. Win: `python manage.py runserver`
   Mac: `make server`

# 使用技術
- 前端: Tailwind CSS / AlpineJS / DaisyUI
- 後端: Python / Django
- 資料庫: PostgreSQL
- 版本控制: Git

# Git 上傳前操作
1. Win: `pre-commit run --all-files`
   Mac: `make lint`
2. git add
3. Win: `cz commit`
   Mac: `make commit`