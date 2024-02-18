# Python + Linebot + OpenAI => 在colab試做

# from openai import OpenAI

from flask_ngrok import run_with_ngrok
from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from langchain_side_api import create_vector_db, get_ask_chain
from smart_home_control import search_for_api

# 載入 json 標準函式庫，處理回傳的資料格式
import json

import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']



app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = CHANNEL_ACCESS_TOKEN
        secret = CHANNEL_SECRET
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token

        if (msg):
            chain = get_ask_chain()
            response = chain.invoke(msg)
        
            # 回覆訊息
            reply_msg = f"{response['result']}"
            api_url = search_for_api(response['result'])
            # 若有產生控制指令
            if (api_url):
                reply_msg += f"\n{api_url}"
        
        text_message = TextSendMessage(text=reply_msg)
        line_bot_api.reply_message(tk,text_message)          # 回傳訊息
        print(reply_msg, tk)                                 # 印出內容
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
#   run_with_ngrok(app)           # 串連 ngrok 服務
  app.run()