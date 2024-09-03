from app.routes import intent_handler
import random


@intent_handler("WhoAreYou(我是誰)")
def handle_whoAreYou_intent(req, token, replytoken):
    """处理 'WhoAreYou(我是誰)' 意图"""
    # 从请求中提取实体
    parameters = req.get("queryResult", {}).get("parameters", {})

    zodiac_sign = parameters.get("zodiac_sign")
    age = parameters.get("ageeee")
    name = parameters.get("namename")
    TaiwanIndigenous = parameters.get("TaiwanIndigenous")
    country = parameters.get("country")
    occupation = parameters.get("occupation")

    if zodiac_sign:
        response_text = "天蠍座。"
    elif age:
        birth_date = "2000-10-24"  # 假设这个是你的生日
        response_text = f"{calculate_age(birth_date)}歲。"
    elif name:
        response_text = "亮。"
    elif TaiwanIndigenous:
        response_text = "太魯閣阿美。"
    elif country:
        response_text = "台灣"
    elif occupation:
        response_text = "工程師"
    else:
        # 如果没有特定问题，随机选择一个自我介绍信息
        responses = [
            "天蠍座。",
            f"{calculate_age('2000-10-24')}歲。",
            "亮。",
            "太魯閣阿美。",
            "台灣",
            "工程師",
        ]
        response_text = random.choice(responses)

    return {"fulfillmentText": response_text}


def calculate_age(birth_date):
    """计算年龄的辅助函数"""
    from datetime import datetime

    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
