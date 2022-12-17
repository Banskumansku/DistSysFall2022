Matchmaker
- Simple express typescript server
- Adds people to queue and when two are present sends IP to each other
- Takes in victories/losses
- Install with ``npm install``
- Run with ``npm start``

- To Deploy to fly.io ``flyctl launch``
- After that go to the generated ``fly.toml`` file and in the ``env`` put the things you would put to the .env file
- The system assumes you will be using 3 nodes, so you will have to make 3 deployments
  - After this you should make 3 different fly.toml files and run them like ``flyctl deploy --config fly.toml``
  - In these toml files you must add the other containers ``queue1Url`` and ``queue2Url`` urls beneath the env params you already have
  - ``queue1Url = "https://hidden-haze-6040.fly.dev" queue2Url = "https://rough-sea-6787.fly.dev"``

***DO NOT REVEAL CONTENTS OF .ENV***
- To .env add
  - PORT
  - MONGODB_URI
  - DB_NAME
  - PLAYER_DB_NAME


Database
- MongoDB
- Return results to Matchmaker queries
