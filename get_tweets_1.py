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

num_friends = api.me().friends_count - 1
# API制限に引っかからないための処理。そのうちtime.sleepとかで全部取得できるようにしたい
if num_friends > 200:
  num_friends = 200

screen_names = []
user_names = []
max_fav_tweets = []
max_fav_favs = []

for user in api.friends(count=num_friends):
  screen_names.append(user.screen_name)
  user_names.append(user.name)

for screen_name in screen_names:
  tweets_data = api.user_timeline(screen_name=screen_name, count=10)
  favs = [td.favorite_count for td in tweets_data]
  max_fav_data = tweets_data[favs.index(max(favs))]
  max_fav_tweet = max_fav_data.text
  max_fav_tweets.append(max_fav_tweet)
  max_fav_favs.append(max_fav_data.favorite_count)

output_list = [["no.", "名前", "id", "いいね！数",  "メッセージ"]]
numbering_list = list(range(1, len(max_fav_tweets) + 1))

for num, name, id, n_fav, fav in zip(numbering_list, user_names, screen_names, max_fav_favs,  max_fav_tweets):
  output_list.append([num, name, id, n_fav, fav])

with open("output/important_tweets.csv", "w", encoding="utf-8") as f:
  writer = csv.writer(f, lineterminator="\n")
  writer.writerows(output_list)