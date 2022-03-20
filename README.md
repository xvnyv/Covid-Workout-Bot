# Covid Workout Bot

A simple Telegram workout bot created for personal use during the pandemic mid-2020.

This is a personal project for learning how to create and deploy Telegram bots using Python.

## Background

Chloe Ting workout challenges exploded during the height of the pandemic as everyone started following them, including me. Workout plans were put up on Chloe's website with links to the relevent YouTube videos. To reduce the need to constantly pull up her website and search for the specific challenges and days, I created a web scraping script to pull the challenge from her website and created this bot to send the daily challenge schedules.

Since then, additional functions have been added to the bot, such as generating a list of workout videos for the day based on the muscle groups that the user wishes to target and adding workout videos to the database.

## Technical Details

The following tools were used to create this bot:

- MongoDB for storing data regarding the workout videos and challenges
- BeautifulSoup for scraping data from Chloe Ting's website
- Google's YouTube API for populating the database with workout videos from other content creators
- Heroku for deploying the application
