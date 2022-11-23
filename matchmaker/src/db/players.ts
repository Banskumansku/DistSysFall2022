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
        const newPlayer = { name: "asd", wins: 1, losses: 1 } as Player;
        const result = await collections.players!.insertOne(newPlayer);

        result
            ? res.status(201).send(`Successfully created a new game with id ${result.insertedId}`)
            : res.status(500).send("Failed to create a new game.");
    } catch (error: any) {
        console.error(error);
        res.status(400).send(error.message);
    }
});

// PUT

// DELETE