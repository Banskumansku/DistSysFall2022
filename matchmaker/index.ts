import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import * as mongoDB from "mongodb";
import { connectToDatabase } from './src/db/service';
import { playerRouter } from './src/db/players';

dotenv.config();

const app: Express = express();
const port = process.env.PORT;


app.get('/queue', async (req: Request, res: Response) => {
    const dbSpec = await connectToDatabase()
    res.send(dbSpec);
});

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
