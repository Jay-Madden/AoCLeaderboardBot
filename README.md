# AoCLeaderboardBot

Dead simple self hostable AoC leaderboard bot

Setup for local development: 
  1. Clone the repo
  2. Rename config.json.template -> config.json and fill in the variables
```
    Token: Your bots token
    LeaderboardTitle: The title you want the leaderboard embed to have
    LeaderboardChannel: The ID of the channel you want the bot to send the leaderboard message in
    SessionCookie: Your Advent of code session cookie to view the leaderboard
    LeaderboardEndpoint: The json endpoint for your leaderboard on the AoC website
```
 3. Run the main.py file
 
Setup for docker hosting: 

```
docker run ghcr.io/jay-madden/aocleaderboardbot:latest \
    -e PROD=1 \
    -e TOKEN=<YOUR_BOT_TOKEN> \
    -e LEADERBOARDTITLE=Title of your leaderboard\
    -e LEADERBOARDCHANNEL=<CHANNEL_ID_OF_YOUR_LEADERBOARD> \
    -e SESSIONCOOKIE=<YOUR_SESSION_COOKIE> \
    -e LEADERBOARDENDPOINT=<ENDPOINT_FOR_YOUR_LEADERBOARD> \
    -e LEADERBOARDINVITE=<LEADERBOARD_INVITE_CODE>
```
