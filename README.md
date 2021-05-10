# WoWTravel
>A Travel Website Project (Full Stack)
>HTML + CSS + BootStrap + FontAwesome + JS + JQ + Flask + SQLite3

## 使用流程
>首頁(index) -> 各國(jp) -> 結帳(jp-list)
>註冊(create) -> 登入(log-in) -> 設定(member) -> 留言(messenge)

## 給各位辛苦的開發者 (待完成)
1. 登入頁面log-in.html<br>
2. <s>做出list.html基本架構頁面，讓jp-list、kr-list、tw-list繼承</s><br>
3. <s>kr-list、tw-list 路徑調整(common.cs、圖片..)</s><br>
4. 同1.做出各國基本架構頁面，讓jp.html繼承<br>
5. 修正Nav我的行程去結帳路由<br>

## 模板
1. index:<br>
- {% block title %}
- {% block style %}
- {% block script %}
- {% block alert %}
- {% block content %}
2. list:<br>
- {% block path %}
- {% block area %}
- {% block schedule_name %}
- {% block traffic %}
- {% block hotel %}
- {% block recommend %}
- {% block cost %}
- {% block reference %}
- {% block feature_explain %}
