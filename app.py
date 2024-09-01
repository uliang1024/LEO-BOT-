from flask import Flask, request
import requests, json, time

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>hello world</h1>"


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    print(req)
    reText = req["queryResult"]["fulfillmentText"]  # 取得 Dialogflow 的回應文字
    intent = req["queryResult"]["intent"]["displayName"]  # 取得 intent 分類
    replytoken = req["originalDetectIntentRequest"]["payload"]["data"][
        "replyToken"
    ]  # 取得 LINE replyToken
    token = "你的 Access Token"
    # 雷達回波圖網址，後方加上時間戳記，避免緩存
    img = f"https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MSC/O-A0058-003.png?{time.time_ns()}"
    # 如果收到的 intent 是 radar
    if intent == "radar":
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        }
        body = {
            "replyToken": replytoken,
            "messages": [
                {"type": "image", "originalContentUrl": img, "previewImageUrl": img}
            ],
        }
        # 使用 requests 方法回傳訊息到 ＬINE
        result = requests.request(
            "POST",
            "https://api.line.me/v2/bot/message/reply",
            headers=headers,
            data=json.dumps(body).encode("utf-8"),
        )
        print(result.text)
        # 完成後回傳訊息到 Dialogflow
        return {"source": "webhookdata"}
    # 如果收到的 intent 不是 radar
    else:
        # 使用 Dialogflow 產生的回應訊息
        return {"fulfillmentText": f"{reText} ( webhook )"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
