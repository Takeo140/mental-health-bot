import os
from openai import OpenAI

# OpenAIのAPIキーを読み込む
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# AIに啓発メッセージを作らせる
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "あなたは精神保健福祉の専門家です。患者の人権向上について啓発メッセージを考えてください。"},
        {"role": "user", "content": "100文字程度のメッセージを1つ作って。"}
    ],
    max_tokens=200
)

# 結果を表示
print(response.choices[0].message.content)
