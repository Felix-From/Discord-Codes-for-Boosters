# Discord Codes for Boosters
A custom-made Discord bot that posts an interaction message and gives game redeemable codes (designed for GTA5).

## Requirements
```
Python 3.8 or better.
pip install mysql-connector-python
pip install nextcord
```
## Purpose
This bot is designed for a Discord / FiveM server with many boosters, providing them with game codes as a token of appreciation.

# How It Works
## From a User's Perspective
The bot posts a message with two interaction buttons: "Get Code" and "Check Time". If a user with a specified role (defined in the config) presses the "Get Code" button, the bot creates a private channel for that user (named after their UserID). In this channel, the bot posts an embed message containing the code and relevant information. The user is then put on a one-month cooldown. The "Check Time" button allows users to see when they last received a code and when they can collect the next one.

## From a Developer's Perspective
Upon starting, the bot deletes its previous messages in the "MessageChannel" and reposts the "Interaction Menu Message". 

When a user interacts with the bot:

- The bot checks if the user has the required role.
- If the user is eligible for a code, the bot generates a random code, adds it to the database, and assigns it to the user.
- The bot logs this transaction in the data_log table with the userID, timestamp, and code details.
- If the user already received a code that month, the bot directs them to their existing channel and mentions the channel.
## Features
- Bot Config Creator: Simplifies configuration creation.
- Content Creator: Facilitates easy creation of a table of contents for codes.
- Role Configurability: Can be configured for various roles via RoleID.
- Management Roles: Defines roles that can manage the bot (debug commands, user channel visibility, log access).
- Logging: Logs every request and code generation.
- Multiple Management Roles: Supports several management roles.
## Installation
```
- Clone the repository.
- Edit config_creator.py to fit your configurations, then run it once.
- Edit content_creator.py to fit your desired code content, then run it once.
- Add vehicle photos to the /img folder if applicable.
- Import the Database.sql into a Database.
- Run main.py.
- Enjoy your bot!
```
##### Extra Info
```
- To Change the Language of the Date / Cooldown Date edit main.py line: 96 to fit your county code.
- To Change the Border color of Embeds edit main.py line: 90
- The Code was made for a german Users, so some of the Text is german inside.
- Most of the time Rocks are harder than Sticks.
```

# Creator Scripts
The creator scripts (config_creator.py and content_creator.py) are used to modify or add configurations and content. While you can edit the .json files they produce directly, these scripts offer a safer and easier way to make changes without the risk of breaking the JSON structure. Using the scripts is also a more convenient method for adding, modifying, or removing content.


#### Sidenotes
I didn't plan to upload it to GitHub, so the code is very "closed" but if you find any bugs, errors or improvements, please let me know so I can learn and make it better next time.