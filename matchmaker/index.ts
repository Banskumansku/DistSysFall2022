import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import { connectToDatabase } from './src/db/service';
import { playerRouter } from './src/db/players';
import axios from 'axios';
const cors = require('cors')

dotenv.config();

const playerQueue: player[] = []

const app: Express = express();
const port = process.env.PORT;
app.use(cors())
app.set('trust proxy', true)

interface player {
    name: string,
    id: string,
    ip: string
}

interface opponentMessage {
    opponents: [
        {
            name: string,
            url: string
        }
    ]
}

app.get('/queue', async (req: Request, res: Response) => {
    //const dbSpec = await connectToDatabase()
    if (playerQueue.find(p => p.id = req.body.id)) {
        res.send("player already in queue");
    } else {
        const newPlayer = {
            name: req.body.name,
            id: req.body.id,
            ip: `http://${req.ip}:8080`
        }
        playerQueue.push(newPlayer)
        res.send(200);
    }
});

setInterval(() => {
    if (playerQueue.length > 1) {
        const player1 = playerQueue.pop()
        const player2 = playerQueue.pop()

        const player1Message: opponentMessage = {
            opponents: [{
                name: player2!.name,
                url: player2!.ip
            }]
        }
        const player2Message: opponentMessage =
        {
            opponents: [{
                name: player1!.name,
                url: player1!.ip
            }]
        }
        sendData(player1!, player1Message)
        sendData(player2!, player2Message)
    }
}, 5000);

const sendData = async (player: player, opponentMessage: opponentMessage) => {
    try {
        const response = await axios.post(player.ip, opponentMessage)
        const data = response.data
        console.log(data)
    } catch (error) {
        console.log(error)
    }
}

connectToDatabase()
    .then(() => {
        app.use("/player", playerRouter);

        app.listen(port, () => {
            console.log(`Server started at http://localhost:${port}`);
        });
    })
    .catch((error: Error) => {
        console.error("Database connection failed", error);
        process.exit();
    });
