#! /usr/bin/env python3
'''
Twitter library

Some methods for the twitter API
@author Keith.Gough

'''

import tweepy
import logging
import os

LOGGER = logging.getLogger(__name__)

# Create variables for each key, secret, token
ENV_VARS = {
    'CONSUMER_API_KEY': None,
    'CONSUMER_API_SECRET': None,
    'ACCESS_TOKEN': None,
    'ACCESS_TOKEN_SECRET': None,
}

# Load the env vars
for env in ENV_VARS:
    ENV_VARS[env] = os.environ.get(env)
    if not ENV_VARS[env]:
        LOGGER.error(f'Environment variable not found: {env}')
        exit(1)


def authenticate():
    """ Authenticate and get the api object
    """
    try:
        auth = tweepy.OAuthHandler(ENV_VARS['CONSUMER_API_KEY'],
                                   ENV_VARS['CONSUMER_API_SECRET'])

        auth.set_access_token(ENV_VARS['ACCESS_TOKEN'],
                              ENV_VARS['ACCESS_TOKEN_SECRET'])

        api = tweepy.API(auth, wait_on_rate_limit=True)
    except tweepy.TweepyException as err:
        LOGGER.error("Could not authenticate")
        LOGGER.error(err)
        api = None

    return api


def get_tweets(api):
    """ Get all tweets from the timeline
        Most recent tweet is first in the list
    """
    try:
        tweets = api.user_timeline()
    except tweepy.TweepyException:
        LOGGER.error('Could not retrieve tweets')
        tweets = []
    return tweets


def post_tweet(api, tweet_string):
    """  Post the given string
    """
    try:
        res = api.update_status(status=tweet_string)
    except tweepy.TweepyException:
        LOGGER.error('Could not post the tweet')
        res = None
    return res


def delete_tweet(api, id):
    """  Delete the given tweet
    """
    try:
        res = api.destroy_status(id=id)
    except tweepy.TweepyException:
        LOGGER.error('Could not delete Tweet with id=%s', id)
        res = None
    return res


def main():
    """  Login and get the readback tweets
         from the timeline
    """
    try:
        api = authenticate()

        # Get all tweets and print them
        tweets = get_tweets(api)
        for tweet in tweets:
            print(tweet.created_at, tweet.text)

        # Post a new tweet
        new_tweet = post_tweet(api, 'Junk')

        # Get all tweets and print them
        print()
        tweets = get_tweets(api)
        for tweet in tweets:
            print(tweet.created_at, tweet.text)

        # Delete the tweet
        if new_tweet:
            delete_tweet(api, new_tweet.id)

        # Get all tweets and print them
        print()
        tweets = get_tweets(api)
        for tweet in tweets:
            print(tweet.created_at, tweet.text)

    except tweepy.TweepyException:
        LOGGER.error('One or more twitter api calls failed.')
        exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
