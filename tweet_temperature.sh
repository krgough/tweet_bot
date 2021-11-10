#!/usr/bin/env bash

# Change to the working directory
cd "$(dirname "$0")"

# Set the env vars
source set_env_vars.sh

# Run the bot
$HOME/.local/bin/poetry run tweet_bot/temperature_tweet_bot.py