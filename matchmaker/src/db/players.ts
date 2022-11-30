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

playerRouter.post("/", async (req: Request, res: Response) => {
    try {
        //const newPlayer = { name: "asd", wins: 1, losses: 1 } as Player;
        const playerName: string = req.query.name as string
        const newPlayer: Player = {
            name: playerName,
            wins: 0,
            losses: 0
        }
        const result = await collections.players!.insertOne(newPlayer);

        result
            ? res.status(201).send(`Successfully created a new player with id ${result.insertedId}`)
            : res.status(500).send("Failed to create a new player.");
    } catch (error: any) {
        console.error(error);
        res.status(400).send(error.message);
    }
});

// PUT

playerRouter.put("/win/:id", async (req: Request, res: Response) => {
    const id = req?.params?.id;

    try {

        const query = { _id: new ObjectId(id) };
        const oldPlayer = (await collections.players!.findOne(query)) as any;
        const wins: number = oldPlayer.wins + 1
        const updated = { ...oldPlayer, wins: wins }

        const result = await collections!.players!.updateOne(query, { $set: updated });

        result
            ? res.status(200).send(`Successfully added win with id ${id}`)
            : res.status(304).send(`Player with id: ${id} not updated`);
    } catch (error: any) {
        console.error(error.message);
        res.status(400).send(error.message);
    }
});

playerRouter.put("/loss/:id", async (req: Request, res: Response) => {
    const id = req?.params?.id;

    try {

        const query = { _id: new ObjectId(id) };
        const oldPlayer = (await collections.players!.findOne(query)) as any;
        const losses: number = oldPlayer.losses + 1
        const updated = { ...oldPlayer, losses: losses }

        const result = await collections!.players!.updateOne(query, { $set: updated });

        result
            ? res.status(200).send(`Successfully added win with id ${id}`)
            : res.status(304).send(`Player with id: ${id} not updated`);
    } catch (error: any) {
        console.error(error.message);
        res.status(400).send(error.message);
    }
});


// DELETE