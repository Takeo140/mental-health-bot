import os
import requests
import facebook

# OpenRouterのAPI設定
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise Exception("OpenRouter APIキーが設定されていません。")

headers = {
    "Authorization": f"token {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/llama-4-maverick:free",
    "messages": [
        {"role": "system", "content": "あなたは精神保健福祉の専門家です。患者の人権向上について啓発メッセージを考えてください。"},
        {"role": "user", "content": "100文字程度のメッセージを1つ作って。"}
    ],
    "max_tokens": 200
}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.status_code != 200:
    raise Exception(f"APIエラー: {response.status_code}\n{response.text}")

result = response.json()
message = result['choices'][0]['message']['content']

print("生成メッセージ:")
print(message)

# Facebookへの投稿設定
fb_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
if not fb_access_token:
    raise Exception("Facebookアクセストークンが設定されていません。")

graph = facebook.GraphAPI(access_token=fb_access_token)
graph.put_object(parent_object='me', connection_name='feed', message=message)
print("Facebookに投稿完了")
