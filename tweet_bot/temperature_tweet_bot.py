#!/usr/bin/env python3
"""

Temperature Tweet Bot
Reads temperature from TMP75B connected to I2C bus
on raspberry pi.  Tweets the temperature to kgpython
twitter account.  Expect this to be run e.g. once an
hour.

"""

import logging
import pickle
from datetime import datetime

import tweet_bot.tmp75b_temperature as tmp75b
import tweet_bot.twitter_api as twit


LOGGER = logging.getLogger(__name__)
STATE_FILE = ".temperature_state"

# These 2 setpoints define three ranges
# t < SP1 = Cold
# SP1 < t < SP2 = Nominal
# t > SP2 = Hot
SP1 = 18  # Cold
SP2 = 24  # Hot
HYSTERESIS = 0.5


def save_state(state: any, filename=STATE_FILE) -> None:
    """ Save the current state to the state file
    """
    with open(filename, mode='w', encoding='utf-8') as file:
        pickle.dump(state, file)


def load_state(filename=STATE_FILE):
    """ Load previous state from the state file
    """
    try:
        with open(filename, 'rb') as file:
            state = pickle.load(file)
    # Capture any file reading error or empty file
    except (OSError, EOFError):
        state = 'NOMINAL'
    return state


def state_with_hysteresis(pvar, prev_state, sp1=SP1, sp2=SP2, hys=HYSTERESIS):
    """ pvar = Process variable (temperature)
        sp1 = Setpoint1
        sp2 = Setpoint2
        h = hysteresis
        prev_state = previous state
        state = new state
    """
    assert prev_state in ['LOW', 'NOMINAL', 'HIGH']
    if pvar < sp1 - hys:
        state = 'LOW'
    elif sp1 + hys <= pvar <= sp2 - hys:
        state = 'NOMINAL'
    elif pvar > sp2 + hys:
        state = 'HIGH'
    else:
        state = prev_state
    return state


def is_midday(now=datetime.now()):
    """ Returns True if current time is between
        11:45 - 12:15
        Else False
    """
    midday = now.replace(hour=12, minute=00, second=0, microsecond=0)
    if abs((now - midday).total_seconds()) <= (15 * 60):
        return True

    return False


def main():
    """ Read temperature and tweet if we have changed
        state or tweet anyway if it is midday.
    """
    # Set shutdown mode to save current
    # All temperature reads are done with one-shot mode
    tmp75b.set_shutdown_mode()

    # Get the current temperture
    temp = tmp75b.read_temperature()
    LOGGER.info('temperature= %s', temp)

    # Get the previous temperature state
    prev_state = load_state()

    # Determine the new state (using hysteresis)
    state = state_with_hysteresis(
        pvar=temp,
        prev_state=prev_state,
        sp1=SP1,
        sp2=SP2,
        hys=HYSTERESIS)

    # Save the state
    save_state(state)

    LOGGER.info('Previous State=%s, Current State=%s', prev_state, state)

    # If the state has changed then tweet the temperature
    if state != prev_state:
        if state == 'HIGH':
            tweet_str = "Phew it's getting hot."
        elif state == 'LOW':
            tweet_str = "Brr it's chilly."
        else:
            tweet_str = "Temperature nominal."
        tweet_str += f" {temp}'C"

        LOGGER.info("Tweeting. %s", tweet_str)
        api = twit.authenticate()
        twit.post_tweet(api, tweet_str)
    else:
        LOGGER.info('No state change, so not tweeting')

    # If it's close to midday and we have not changed state
    # then tweet anyway. We assume cron calls this code once
    # an hour and we check here if time is midday +/-15mins.
    if is_midday():
        LOGGER.info('Midday tweet')
        tweet_str = f"Midday Temperature={temp}'C"
        api = twit.authenticate()
        twit.post_tweet(api, tweet_str)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    LOGGER.info('All done.')
