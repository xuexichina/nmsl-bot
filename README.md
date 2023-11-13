# Telegram NM$L Bot

## 使用方式

在任意聊天窗口输入 @xxx_bot 即会随机弹出至多五句语录，输入文字更可过滤筛选语录，
点击弹出的insult语录即可自动发出。若语句不令人满意，可以删除整条消息 10s 后重试。

## 开始上手

1. 从 BotFather 申请到 Telegram Bot 账号，牢记 token
2. 修改 docker-compose.yml 中的 API_TOKEN 为你的 token
3. `docker-compose up -d`

或

``` shell script
$ pip install -r requirements.txt
$ API_TOKEN=<your_token_here> python -m tg_inline_bot.__main__
```
## What is this
NMSL (Chinese: 你妈死了; pinyin: nǐmāsǐle; lit. 'Your mom is dead'), used as an insult. for this project is provides some insults Chinese sentences in telegram bot.

## How to use

Enter @yout_bot_username in any chat window, and up to five quotations will pop up randomly, and you can filter the quotations by entering text.
Click the pop-up insult quotation to send it out automatically. If the sentence is not satisfactory, you can delete the entire message and try again after 10 seconds.

## Get started

1. Apply from BotFather to Telegram Bot account, remember token
2. Modify API_TOKEN in docker-compose.yml as your token
3. `docker-compose up -d`

