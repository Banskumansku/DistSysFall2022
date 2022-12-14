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
app.use(express.json())

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

app.post('/queue', async (req: Request, res: Response) => {
    console.log(req.body)
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
        res.sendStatus(200);
        if (playerQueue.length > 1) {
            await matchOn()
        }
    }
});

const matchOn = async () => {
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

setInterval(async () => {
    console.log(playerQueue)
    if (playerQueue.length > 1) {
        await matchOn()
    }
}, 1000);

const sendData = async (player: player, opponentMessage: opponentMessage) => {
    try {
        console.log(player, opponentMessage)
        const response = await axios.post(player.ip, opponentMessage)
        console.log(response.data)
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
