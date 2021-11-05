#!/usr/bin/env bash

source /home/pi/repositories/tweet_bot/set_env_vars.sh
poetry run /home/pi/repositories/tweet_bot/tweet_bot/temperature_tweet_bot.py
