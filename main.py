import pip install --upgrade openaiimport os

# OpenAIのAPIキーを読み込む
openai.api_key = os.getenv("OPENAI_API_KEY")

# AIに啓発メッセージを作らせる
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "あなたは精神保健福祉の専門家です。患者の人権向上について啓発メッセージを考えてください。"},
    {"role": "user", "content": "100文字程度のメッセージを1つ作って。"}
  ],
  max_tokens=200
)

# 結果を表示
print(response.choices[0].message["content"])
