import express, { Request, Response } from "express";
import { ObjectId } from "mongodb";
import Player from "./models/Player";
import { collections } from "./service";

// Global Config

export const playerRouter = express.Router();

playerRouter.use(express.json());

// GET

playerRouter.get("/", async (_req: Request, res: Response) => {
    try {
        const players = (await collections!.players!.find({}).toArray()) as any;

        res.status(200).send(players);
    } catch (error: any) {
        res.status(500).send(error.message);
    }
});

playerRouter.get("/:id", async (req: Request, res: Response) => {
    const id = req?.params?.id;

    try {

        const query = { _id: new ObjectId(id) };
        const player = (await collections.players!.findOne(query)) as any;

        if (player) {
            res.status(200).send(player);
        }
    } catch (error) {
        res.status(404).send(`Unable to find matching document with id: ${req.params.id}`);
    }
});
// POST

const addPlayer = async (name: string, loss?: boolean, win?: boolean) => {
    const newPlayer: Player = {
        name: name,
        wins: win ? 1 : 0,
        losses: loss ? 1 : 0
    }
    return await collections.players!.insertOne(newPlayer);
}

playerRouter.post("/", async (req: Request, res: Response) => {
    try {
        //const newPlayer = { name: "asd", wins: 1, losses: 1 } as Player;
        const playerName: string = req.query.name as string
        const result = await addPlayer(playerName)

        result
            ? res.status(201).send(`Successfully created a new player with id ${result.insertedId}`)
            : res.status(500).send("Failed to create a new player.");
    } catch (error: any) {
        console.error(error);
        res.status(400).send(error.message);
    }
});

// PUT

playerRouter.post("/win/:name", async (req: Request, res: Response) => {
    const name = req?.params?.name;

    try {

        const query = { name: name };
        const oldPlayer = (await collections.players!.findOne(query)) as any;
        if (!oldPlayer) {
            const result = await addPlayer(name, false, true)

            result
                ? res.status(200).send(`Successfully added user with name ${name} and one victory`)
                : res.status(304).send(`Player with name: ${name} not updated`);
        } else {
            const wins: number = oldPlayer.wins + 1
            const updated = { ...oldPlayer, wins: wins }

            const result = await collections!.players!.updateOne(query, { $set: updated });

            result
                ? res.status(200).send(`Successfully added win with name ${name}`)
                : res.status(304).send(`Player with name: ${name} not updated`);
        }
    } catch (error: any) {
        console.error(error.message);
        res.status(400).send(error.message);
    }
});

playerRouter.post("/loss/:name", async (req: Request, res: Response) => {
    const name = req?.params?.name;

    try {

        const query = { name: name };
        const oldPlayer = (await collections.players!.findOne(query)) as any;
        if (!oldPlayer) {
            const result = await addPlayer(name, true, false)
            result
                ? res.status(200).send(`Successfully added user with name ${name} and one loss`)
                : res.status(304).send(`Player with name: ${name} not updated`);
        } else {
            const losses: number = oldPlayer.losses + 1
            const updated = { ...oldPlayer, losses: losses }

            const result = await collections!.players!.updateOne(query, { $set: updated });

            result
                ? res.status(200).send(`Successfully added loss with name ${name}`)
                : res.status(304).send(`Player with name: ${name} not updated`);
        }
    } catch (error: any) {
        console.error(error.message);
        res.status(400).send(error.message);
    }
});


// DELETE