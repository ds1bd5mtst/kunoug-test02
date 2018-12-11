from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import pandas

from azure.storage.blob import (
    BlockBlobService, PublicAccess
)

app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
 
## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    #handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'
 
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 


"""
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。
"""
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    account_name='ds1bd5mtst'
    account_key='QRW6ikCh6i2TAOZsJnAuliDJX03xU8xmm3GVhsLFD8cw3Z9yjOLZVE3CYdgKpV+74D4y1dKCsK6bd5fjUup3LQ=='
    container_name='testcontainer'
    file_name='test02.csv'
    
    service = BlockBlobService(account_name=account_name,account_key=account_key)
    service.get_blob_to_path(container_name,file_name,'test02.csv')
    
    
    df = pandas.read_csv(file_name)
    
    """
    list = []
    for index, row in df.iterrows():
        if row["title"].find(event.message.text) != -1:
        # 見つかった場合
        list.append(row["title"])
    # 重複排除
    result_list = set(list)
    messages = ','.join(result_list)
    
    """
    
    # ファイルの削除
    os.remove(file_name)
    
    messages =""
    if event.message.text == "一覧" or event.message.text == "いちらん":
        messages = "一覧は作成中です"
    else:
        messages = "よくわかりません"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=messages)) # messagesに代入されている値を返してくれる
 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
#    下のやつなんや
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

