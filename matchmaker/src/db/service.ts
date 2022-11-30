import * as mongoDB from "mongodb";
import * as dotenv from "dotenv";
import Player from "./models/Player";

// External Dependencies

// Global Variables
export const collections: { players?: mongoDB.Collection } = {}

// Initialize Connection
export const connectToDatabase = async () => {
    dotenv.config();
    const MONGODB_URI = process?.env?.MONGODB_URI
    if (!MONGODB_URI) return
    const client: mongoDB.MongoClient = new mongoDB.MongoClient(MONGODB_URI);

    await client.connect();


    const db: mongoDB.Db = client.db(process.env.DB_NAME);
    const playerCollection: mongoDB.Collection = db.collection(process.env.PLAYER_DB_NAME!);
    collections.players = playerCollection;
    const player: Player = {
        name: "asd",
        wins: 2,
        losses: 1
    }
    const play = (await collections.players.find({}).toArray()) as unknown as Player[];
    //const asd = await collections.players.insertOne(player)
    console.log(play)
    return `Successfully connected to database: ${db.databaseName} `;
}