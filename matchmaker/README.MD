Matchmaker
- Simple express typescript server
- Adds people to queue and when two are present sends IP to each other
- Takes in victories/losses
- Install with ``npm install``
- Run with ``npm start``

- To Deploy to fly.io ``flyctl launch``
- After that go to the generated ``fly.toml`` file and in the ``env`` put the things you would put to the .env file

***DO NOT REVEAL CONTENTS OF .ENV***
- To .env add
  - PORT
  - MONGODB_URI
  - DB_NAME
  - PLAYER_DB_NAME


Database
- MongoDB
- Return results to Matchmaker queries
