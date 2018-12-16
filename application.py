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

import pandas as pd

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
    file_name='bookdata.csv'
    file_name1='userdata.csv'
    
    service = BlockBlobService(account_name=account_name,account_key=account_key)
    service.get_blob_to_path(container_name,file_name,file_name)
    service.get_blob_to_path(container_name,file_name1,file_name1)
    
    df1 = pd.read_csv(file_name1,encoding="shift_jis", sep=",")
    
    profile = line_bot_api.get_profile(event.source.user_id)
    user_disp_name = profile.display_name
    user_id = event.source.user_id
    
    #messages = "test"
    
    
    messages = ""
    for index, row in df1.iterrows():
        if row["LINEID"] ==  user_id :
            messages = "登録済"
            break
        else:
            df2 = pd.DataFrame(data=[[user_id,user_disp_name,0]],columns=['LINEID','username','userstatus'])
            #LINEID = user_id
            #username = user_disp_name
            #userstatus = 0
            #se = pd.Series([user_id,user_disp_name,0],index=df1.columns)
            df3 = df1.append(df2, ignore_index=True)
            df3.to_csv(file_name1,encoding="shift_jis")
            service.create_blob_from_path(container_name,file_name1,file_name1)
            messages = "登録しました"
    
    
    """
    # CSV読み込み
    #with cd.open(file_name, "r", "Shift-JIS", "ignore") as file:
    # df = pd.read_csv(filename)
    #    df = pd.read_table(file,header=None,sep=',')
    df = pd.read_csv(file_name,encoding="shift_jis", sep=",")
    """
    
    """
    # 検索
    list = []
    for index, row in df.iterrows():
        if row["title"].find(event.message.text) != -1:
            list.append(row["title"])
    
    # 重複排除
    messages = ','.join(set(list))
    """
    
    """
    #借りる
    messages = ""
    for index, row in df.iterrows():
        # 指定されたタイトル名の本があった場合
        if row["title"] == event.message.text :
            # 貸出可能な場合
            if row["status"] == 0:
                df.loc[index, 'status'] = 1
                # rentaluserに代入する値にはLINEIDを入れる
                profile = line_bot_api.get_profile(event.source.user_id)
                user_disp_name = profile.display_name
                #user_id = event.source.user_id
                df.loc[index, 'rentaluser'] = user_disp_name
                messages = "借りれるよ"
                break
            else:
                messages = "誰か借りてる"
        else:
            # 指定されたタイトル名の本がなかった場合
            if messages != "誰か借りてる":
                messages = "そんな本ないよ"
    
    df = df.drop(["Unnamed: 0"],axis=1)
    df.to_csv(file_name,encoding="shift_jis")
    
    service.create_blob_from_path(container_name,file_name,file_name)
    """
    
    
    """
# 3、返す
    messages = ""
    user_id = event.source.user_id
    for index, row in df.iterrows():
        # 指定されたタイトル名の本があった場合
        if row["title"] == event.message.text :
        # 借りてるユーザーが一致の場合（LINEIDと比較する必要あり）
            if row["rentaluser"] == user_id :
                df.loc[index, 'status'] = 0
                df.loc[index, 'rentaluser'] = 0
                messages = "返却しました"
                break
            else:
                messages = "借りてないよ"
        # 指定されたタイトル名の本がなかった場合
        else:
            if messages != "借りてないいよ":
                messages = "そんな本ないよ"
    df = df.drop(["Unnamed: 0"],axis=1)
    df.to_csv(file_name)
    
    service.create_blob_from_path(container_name,file_name,file_name)
    """
    
    
    # ファイルの削除
    os.remove(file_name)
    os.remove(file_name1)
    
    """
    messages = ""
    if event.message.text == "一覧" or event.message.text == "いちらん":
        messages = "一覧は作成中です"
    else:
        messages = "よくわかりません"
    """
    
    
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=messages)) # messagesに代入されている値を返してくれる
 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
#    下のやつなんや
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

