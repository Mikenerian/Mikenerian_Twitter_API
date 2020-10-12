import tweepy
import csv
import settings

Consumer_key = settings.Consumer_key
Consumer_secret = settings.Consumer_secret
Access_token = settings.Access_token
Access_secret = settings.Access_secret

auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_secret)
api = tweepy.API(auth)

# API制限に引っかからないための処理。そのうちtime.sleepとかで全部取得できるようにしたい
num_friends = api.me().friends_count - 1
if num_friends > 200:
  num_friends = 200

screen_names = []
user_names = []

# 今は「大学生」というワードがプロフィールに入っていれば大学生であると判断している。そのうち大学生っぽいword listを作ったりしてみたい
search_word = '大学生'

for user in api.friends(count=num_friends):
  if search_word in user.description:
    screen_names.append(user.screen_name)
    user_names.append(user.name)

output_list = [["no.", "名前", "id"]]
numbering_list = list(range(1, len(user_names) + 1))

for num, name, id in zip(numbering_list, user_names, screen_names):
  output_list.append([num, name, id])

with open("output/list_of_undergraduates.csv", "w", encoding="utf-8") as f:
  writer = csv.writer(f, lineterminator="\n")
  writer.writerows(output_list)
