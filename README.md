# AoCLeaderboardBot

Dead simple self hostable AoC leaderboard bot

Setup: 
  1. Clone the repo
  2. Rename config.json.template -> config.json and fill in the variables
  
    Token: Your bots token
    LeaderboardTitle: The title you want the leaderboard embed to have
    LeaderboardChannel: The ID of the channel you want the bot to send the leaderboard message in
    SessionCookie: Your Advent of code session cookie to view the leaderboard
    LeaderboardEndpoint: The json endpoint for your leaderboard on the AoC website
    
 3. once those are filled in simply build the container with `docker build .` and then run the container with `docker run <ImageId>`
