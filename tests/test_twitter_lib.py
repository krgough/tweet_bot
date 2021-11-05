from tweet_bot import __version__
import tweet_bot.twitter_api as twit
import tweet_bot.tmp75b_temperature as tmp75b
import time
import pytest


def test_version():
    assert __version__ == '0.1.0'


@pytest.fixture
def api():
    return twit.authenticate()


def test_auth():
    assert api is not None


def test_post_and_delete_tweet(api):
    tweet_str = '{} : Hello from Keith'.format(time.time())
    new_tweet = twit.post_tweet(api, tweet_str)
    assert new_tweet is not None
    assert twit.delete_tweet(api, new_tweet.id) is not None


def test_get_public_tweets(api):
    tweets = twit.get_tweets(api)
    assert tweets is not None
    for tweet in tweets:
        print(tweet.text)


test_vals = [
    (0b1111000001111111, 127.9375),
    (0b0000000001100100, 100),
    (0b0000000000000000, 0),
    (0b1100000011111111, -0.25),
    (0b0000000011100111, -25),
    (0b0000000010000000, -128)
]


@pytest.mark.parametrize("test_input, expected", test_vals)
def test_raw_temp_to_float(test_input, expected):
    assert tmp75b.convert_raw_temp_to_float(test_input) == expected
