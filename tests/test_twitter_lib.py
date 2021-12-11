#!/usr/bin/env python3
"""
Tests for tweet_bot
"""
import time
from datetime import datetime

import pytest

from tweet_bot import __version__
import tweet_bot.temperature_tweet_bot as bot
import tweet_bot.twitter_api as twit
import tweet_bot.tmp75b_temperature as tmp75b


def test_version():
    """ Check the module version is correct
    """
    assert __version__ == '0.1.0'


@pytest.fixture(name='api')
def fixture_api():
    """  Get a tweepy api object for use in
         the following tests
    """
    return twit.authenticate()


def test_auth(api):
    """ Check that we have authenticated
        with the twitter api
    """
    assert api is not None


def test_post_and_delete_tweet(api):
    """ Post a tweet and then delete it
    """
    tweet_str = f'{time.time()} : Hello from Keith'
    new_tweet = twit.post_tweet(api, tweet_str)
    assert new_tweet is not None
    assert twit.delete_tweet(api, new_tweet.id) is not None


def test_get_public_tweets(api):
    """ Get a list of tweets
    """
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
    """  Test convertion of raw temperature values
         to floats.
    """
    assert tmp75b.convert_raw_temp_to_float(test_input) == expected


temp_state_vals = [
    (bot.SP1 - 1, 'LOW', 'LOW'),  # Low and rising slowly to Nominal
    (bot.SP1 - 0.5, 'LOW', 'LOW'),
    (bot.SP1 + 0, 'LOW', 'LOW'),
    (bot.SP1 + 0.5, 'LOW', 'NOMINAL'),
    (bot.SP1 + 0, 'NOMINAL', 'NOMINAL'),  # Now drop back to Low
    (bot.SP1 - 0.5, 'NOMINAL', 'NOMINAL'),
    (bot.SP1 - 1.0, 'NOMINAL', 'LOW'),
    (bot.SP2 - 1, 'NOMINAL', 'NOMINAL'),  # Now test Nominal to High
    (bot.SP2 - 0.5, 'NOMINAL', 'NOMINAL'),
    (bot.SP2 + 0, 'NOMINAL', 'NOMINAL'),
    (bot.SP2 + 0.5, 'NOMINAL', 'NOMINAL'),
    (bot.SP2 + 1.0, 'NOMINAL', 'HIGH'),  # Now drop back down to Nominal
    (bot.SP2 + 0.5, 'HIGH', 'HIGH'),
    (bot.SP2 + 0, 'HIGH', 'HIGH')
]


@pytest.mark.parametrize("temperature, prev_state, state", temp_state_vals)
def test_state_with_hysteresis(temperature, prev_state, state):
    """  Test that the hysteresis works
    """
    assert bot.state_with_hysteresis(
        pvar=temperature,
        prev_state=prev_state) == state


is_midday_test_vals = [
    (datetime(2021, 7, 11, hour=10, minute=0), False),
    (datetime(2021, 7, 11, hour=11, minute=44), False),
    (datetime(2021, 7, 11, hour=11, minute=45), True),
    (datetime(2021, 7, 11, hour=12, minute=00), True),
    (datetime(2021, 7, 11, hour=12, minute=15), True),
    (datetime(2021, 7, 11, hour=12, minute=16), False),
]


@pytest.mark.parametrize("now_dt, expected", is_midday_test_vals)
def test_is_midday(now_dt, expected):
    """  Test that is_midday works
    """
    assert bot.is_midday(now=now_dt) == expected
