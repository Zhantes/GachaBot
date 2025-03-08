GachaBot

This is a project in order to improve my programming skills, while at the same time doing something that might be fun or interesting. The objective is to create a discord bot that is accurately able to simulate a gacha system, popular in many games these days. 

Currently the bot is capable of pulling by selecting from 3 different rarities (S, A and B), and from that rarity, picking a random character from a database based on that rarity. For this example I've used characters from Zenless Zone Zero, but you could add any characters you want, by manually adjusting the Characters table in the .db file. 

Tokens are also required to perform pulls, and for that I've added an admin command that allows admins to give anyone tokens. You may also implement it into leveling systems or some kind of daily reward for users.

Available commands:

/pull: does a single pull, returns a character and image of said character.

/10pull: does 10 consecutive pulls, and returns a list with the results.

/info: displays a window with information such as rates, pity, total attempts and available tokens

/reset: (admin only) resets an user's total attempts and pity.

/givetoken: (admin only) grants any user a specified amount of tokens.

Future additions:

At this point I've made all major additions I've wanted to the bot, so I will not make any changes now. However, there are other things to add:

- Some way to keep track of obtained characters per user. (maybe a set?)

- "Soft" pity, which means rates for S-rank goes up the closer it gets to "hard" pity. I'm not certain how this will be implemented yet.