import os
import requests
import tweepy
import facebook

# OpenRouterのAPI設定
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise Exception("OpenRouter APIキーが設定されていません。")

headers = { "Authorization": f"Bearer {api_key}","Content-Type": "application/json"}

data = {"model": "meta-llama/llama-4-maverick:free", "messages": [{"role": "system", "content": "あなたは精神保健福祉の専門家です。患者の人権向上について啓発メッセージを考えてください。"},
        {"role": "user", "content": "100文字程度のメッセージを1つ作って。"} ],"max_tokens": 200}

response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

if response.status_code != 200:
    raise Exception(f"APIエラー: {response.status_code}\n{response.text}")

result = response.json()
message = result['choices'][0]['message']['content']

print(message)

# --- X（旧Twitter）への投稿設定 ---
consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
twitter_api = tweepy.API(auth)
twitter_api.update_status(message)
print("Xに投稿完了")

# --- Facebookへの投稿設定 ---
fb_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
graph = facebook.GraphAPI(access_token=fb_access_token)
graph.put_object(parent_object='me', connection_name='feed', message=message)
print("Facebookに投稿完了")
