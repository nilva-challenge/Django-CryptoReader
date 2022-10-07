# Documentation
You can check full documentation from [here]()

## Introduction
This project is a REST based django application to read signed in user's KuCoin open positions for them. For this to happen, application able to read user's positions (if requested from user) every 30 seconds. 

Application have these features:
- Users able to **sign up** (provide name, username & kucoin details).
- Users able to **sign in** with jwt authentication.
- Users able to **request position tracking** with send request based on **track** field ("true" or "false").
- Users able to **see list** of current open (active) positions.
- Application able to track user's positions every 30 seconds with celery periodic task.
- Application able to handle multi users with celery task & redis.
- Application able to resume its job after restart with redis backend and database.

Application use [this api](https://docs.kucoin.com/#list-accounts) from KuCoin to handle KuCoin positions.
