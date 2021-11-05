#!/usr/bin/env python3
"""

Temperature Tweet Bot
Reads temperature from TMP75B connected to I2C bus
on raspberry pi.  Tweets the temperature to kgpython
twitter account.  Expect this to be run e.g. once an
hour.

"""

import logging
import tmp75b_temperature as tmp75b
import twitter_api as twit


LOGGER = logging.getLogger(__name__)


def main():
    # Get the temperture
    temp = tmp75b.read_temperature()

    # Tweet the temperature
    if temp > 24:
        tweet_str = "Phew it's getting hot."
    elif temp < 18:
        tweet_str = "Brr it's chilly."
    else:
        tweet_str = "Temperature nominal. "
    tweet_str += f" The temperature is {temp}"
    LOGGER.info(tweet_str)

    api = twit.authenticate()
    twit.post_tweet(api, tweet_str)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    LOGGER.info('All done.')
