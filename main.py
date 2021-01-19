import requests
import os
import json
from decouple import config

def get_posts_from_user(username: str):
    token = config('BEARER_TOKEN')
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://api.twitter.com/2/users/by/username/"+username
    response = requests.request("GET", url, headers=headers)
    response = response.json()

    user_id = response['data']['id']

    url = "https://api.twitter.com/2/users/"+user_id+"/tweets"
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys = True))

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
    print(url)


    response = requests.request("GET", url, headers=headers)
    response = response.json()
    print(json.dumps(response, indent=4, sort_keys = True))

def main():
    #get_post_information([1278747501642657792, 1255542774432063488])
    get_posts_from_user('MKBHD')
if __name__ == "__main__":
    main()
