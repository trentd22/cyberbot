# CyberBot

[![Version 0.01](https://img.shields.io/badge/version-0.01-green)](https://github.com/trentd22/cyberbot)
[![Python 3.6](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)

An open-source Discord bot designed for CTF and InfoSec enthusiasts, made using discord.py and the CTFTime API.

Note: This is a very early build of the bot; if you have any issues or feedback please do not hesitate to post it!

### Main Features

- Track upcoming CTF events and your team's stats

- 75+ InfoSec/CS trivia questions, with plans to add hundreds more

- Trivia leaderboard system

- Admin commands (Kick/Ban/Unban)

- Many more features to be added!

### Adding the Bot to Your Server?

Just simply [click here to add the bot to your discord!](https://discord.com/api/oauth2/authorize?client_id=741494474081042504&permissions=8&scope=bot)

### Wanting to Host your Own Instance?

1. Install the discord.py package

```sh
  # On Linux/macOS
  
  python3 -m pip install -U discord.py


  # On Windows
  
  py -3 -m pip install -U discord.py
```

2. Clone the repository

```
  git clone https://github.com/trentd22/cyberbot.git
```

3. Refer to this link and set up a Bot application in your Discord developer portal. (https://discordpy.readthedocs.io/en/latest/discord.html)

4. Copy your token from the "Bot" tab of Step 3, and replace the `TOKEN` variable string in the `bot.py` file with your token.

   So if your token is "1234abcd", you would do:
```py
TOKEN = '1234abcd'
```

### Licensing and More

CyberBot is licensed under the MIT license, which can be viewed under the "LICENSE" file.

The discord.py API wrapper is authored by Rapptz and licensed under the MIT license. [You can view the repository here.](https://github.com/Rapptz/discord.py)
The CTFTime API is used for event and team integration. [Link to CTFTime.](https://ctftime.org/)