# WoWTravel
>A Travel Website Project (Full Stack)<br>
>HTML + CSS + BootStrap + FontAwesome + JS + JQ + Flask + SQLite3

## 使用流程
>首頁(index) -> 各國(jp) -> 結帳(jp-list)<br>
>註冊(create) -> 登入(log-in) -> 設定(member) -> 留言(message)

## 給各位辛苦的開發者 (待完成)
1. <s>登入頁面log-in.html</s><br>
2. <s>留言板message.html</s><br>
3. <s>做出list.html基本架構頁面，讓jp-list、kr-list、tw-list繼承</s><br>
4. <s>kr-list、tw-list 路徑調整(common.cs、圖片..)</s><br>
5. 同1.做出各國基本架構頁面，讓jp.html繼承<br>
6. 修正Nav我的行程去結帳路由<br>

## 模板
- Index
```jinja
{% raw %}
{% extends "index.html" %}
{% block title %}
{% block style %}
{% block script %}
{% block alert %}
{% block content %}
{% endraw %}
```
- List
```jinja
{% raw %}
{% extends "list.html" %}
{% block path %}
{% block area %}
{% block schedule_name %}
{% block traffic %}
{% block hotel %}
{% block recommend %}
{% block cost %}
{% block reference %}
{% block feature_explain %}
{% endraw %}
```
