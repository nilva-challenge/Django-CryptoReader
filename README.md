# CryptoTracker project description
We implement a crypto tracker project using djano rest framework. 

Check List of requested features:
- [x] User able to signup (name, username, password and KuCoin information:{api_key, secret_key and passphrase}) 
- [x] User able to sign in (using django rest token authentication)
- [x] User able to request position tracking and cancel it. (using **APScheduler** library every 30 secs fetch user's positions)
- [x] User able to see list of open position
- [x] Application track user's positions (if user requested for it) every 30 secs
- [x] Application stores users that requested for positions tracking and track their positions in a interval (Handeling muti users)
- [x] Application start position tracking by starting application (resume traking with restarting application)

Also you can see the API documentation created using postman in the link below:

[CryptoTracker API documentation](https://documenter.getpostman.com/view/2983315/UzR1L3Ai)



# In name of Allah

## Introduction
We want to develop a REST based django application to read signed in user's KuCoin open positions for them. For this to happen, you must be able to read user's positions (if requested from user) every 30 seconds. 

The application you develop must have these features:
- Users should be able to **sign up** (provide name, username & kucoin details).
- Users should be able to **sign in**.
- Users should be able to **request position tracking**.
- Users should be able to **see list** of current open positions.
- Application should be able to track user's positions every 30 seconds.
- Application should be able to handle multi users.
- Application must be able to resume its job after restart.

You can use [this api](https://docs.kucoin.com/#list-accounts) from KuCoin to handle this. You should create KuCoin account if you do not have already & get api key & secret to test your implementation. Note we do not need your api key, that is only for your own usage.

### Note
- We do **NOT want any kind of UI** from you 
- KuCoin api key & secrets should not be stored in raw format
 
 
## Expectations:
We want a clean, readable and maintainable code with meaningful comments and docstrings. Also you need to provide postman API doc for web app. 

## Task
1. Fork this repository
2. Develop the challenge with Django 3 or higher
3. Push your code to your repository
4. Send us a pull request, we will review and get back to you
5. Enjoy 
