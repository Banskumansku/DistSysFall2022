import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import { connectToDatabase } from './src/db/service';
import { playerRouter } from './src/db/players';
import axios from 'axios';
const cors = require('cors')

dotenv.config();

//If I was to make this again, I would use a Map here for easier checking
let playerQueue: player[] = []

const app: Express = express();
const port = process.env.PORT;
app.use(cors())
app.set('trust proxy', true)
app.use(express.json());

interface player {
    name: string,
    id: string,
    return_url: string,
    timestamp: number
}

interface opponent {
    name: string,
    url: string
}

interface opponentMessage {
    opponents: opponent[]
}

app.post('/removeFromQueue', async (req: Request, res: Response) => {
    const body = req.body
    console.log("removed from queue", req.body)
    playerQueue = playerQueue.filter(player => player.return_url !== body.return_url)
    res.sendStatus(200);
})

app.get('/queue', async (req: Request, res: Response) => {
    res.send({"queue": playerQueue.length});
})

app.post('/queueTransfer', async (req: Request, res: Response) => {
    const body = req.body
    console.log("added from queue", req.body)
    playerQueue = playerQueue.filter(player => player.return_url !== req.body.return_url)
    playerQueue.unshift(body)
    res.sendStatus(200);
})

app.post('/request-match', async (req: Request, res: Response) => {
    const body = req.body
    console.log(req.body)
    //If player wants to enter the queue again they are removed from the original queue
    playerQueue = playerQueue.filter(player => player.return_url !== req.body.return_url)
    const newPlayer = {
        name: body.name,
        id: body.id,
        return_url: body.return_url,
        timestamp: new Date().getTime()
    }
    playerQueue.push(newPlayer)
    res.send({ "status": "success" });
    if (playerQueue.length > 1) {
        await matchOn()
    }

});

const matchOn = async () => {
    const player1 = playerQueue.shift()
    const player2 = playerQueue.shift()

    const player1Message: opponentMessage = {
        opponents: [{
            name: player1!.name,
            url: player1!.return_url
        }, {
            name: player2!.name,
            url: player2!.return_url
        }]
    }
    const player2Message: opponentMessage =
    {
        opponents: [{
            name: player1!.name,
            url: player1!.return_url
        }, {
            name: player2!.name,
            url: player2!.return_url
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
}, 5000);

setInterval(async () => {
    if (playerQueue.length > 0) {
        const time = new Date().getTime()
        if (time - playerQueue[0].timestamp >= 1000 * 90) {
            console.log("Player has spent 90 seconds in the queue, dropping from queue")
            console.log(playerQueue.shift())
        }
        else if (time - playerQueue[0].timestamp >= 1000 * 20) {
            await pollAndSend(playerQueue.shift())
        }
    }
}, 1000);

const sendData = async (player: player, opponentMessage: opponentMessage) => {
    try {
        console.log(player, opponentMessage)
        const response = await axios.post(`${player.return_url}/matchmaking-success`, opponentMessage)
        console.log(response.data)
    } catch (error) {
        console.log(error)
    }
}

const pollAndSend = async (player?: player) => {
    if (!!player) {
        const queue1 = await axios.get(`${process.env.queue1Url}/queue`)
        const queue2 = await axios.get(`${process.env.queue2Url}/queue`)
        if (queue2.data.queue > 0) {
            await axios.all([
                axios.post(`${process.env.queue1Url}/removeFromQueue`, player),
                axios.post(`${process.env.queue2Url}/queueTransfer`, player)
            ])
            console.log("Player moved")
        } else if (queue1.data > 0) {
            await axios.all([
                axios.post(`${process.env.queue2Url}/removeFromQueue`, player),
                axios.post(`${process.env.queue1Url}/queueTransfer`, player)
            ])
            console.log("Player moved")
        } else {
            playerQueue.unshift(player)
        }
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
