import requests
import os
import json
from decouple import config
import csv
from datetime import datetime

def save_data(info:dict, num_followers:int):
    #print(json.dumps(info, indent=4, sort_keys = True))
    with open('post_data.csv', mode = 'a') as post_data:
        post_data_writer = csv.writer(post_data, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        for index, post in enumerate(info['data']):
            date = post['created_at'][0:-5]
            date = datetime.fromisoformat(date)
            x_var = [date.weekday(), ((date.hour*60)+date.minute), num_followers]
            y_var = [(post['public_metrics']['like_count'] + post['public_metrics']['retweet_count'])/num_followers]
            y_var[0] = '{:.20f}'.format(y_var[0])
            post_data_writer.writerow(x_var + y_var)

def get_posts_from_user(username: str, num_results:int = 100):
    token = config('BEARER_TOKEN')
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://api.twitter.com/2/users/by/username/"+username +"?user.fields=public_metrics"
    response = requests.request("GET", url, headers=headers)
    response = response.json()

    user_id = response['data']['id']
    num_followers = response['data']['public_metrics']['followers_count']
    tweet_fields = "tweet.fields=public_metrics,created_at"
    max_results = '&max_results=' + str(num_results) #number of results to return

    url = "https://api.twitter.com/2/users/"+user_id+"/tweets?" + tweet_fields + max_results
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    save_data(response, num_followers)
    print("Saved: ", username, "with number of datapoints: ", num_results)

def get_post_information(post_ids: list):
    token = config('BEARER_TOKEN')
    headers = {"Authorization": "Bearer {}".format(token)}

    tweet_fields = "tweet.fields=public_metrics,created_at"

    ids = ["ids="]
    for i,id in enumerate(post_ids):
        if(i==(len(post_ids)-1)):
            ids += str(id)
        else:
            ids += str(id)+","
    ids = "".join(ids)
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)

    response = requests.request("GET", url, headers=headers)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys = True))

def main():
    try:
        os.remove('post_data.csv')
    except:
        pass
    get_posts_from_user('MKBHD')
    get_posts_from_user('elonmusk')
    get_posts_from_user('KamalaHarris')
    get_posts_from_user('JoeBiden')
    get_posts_from_user('Tesla')
    get_posts_from_user('BarackObama')
    get_posts_from_user('justinbieber')
    get_posts_from_user('katyperry')
    get_posts_from_user('rihanna')
    get_posts_from_user('Cristiano')
    get_posts_from_user('tylorswift13')
    get_posts_from_user('ladygaga')
    get_posts_from_user('ArianaGrande')
    get_posts_from_user('TheEllenShow')
    get_posts_from_user('YouTube')

if __name__ == "__main__":
    main()
