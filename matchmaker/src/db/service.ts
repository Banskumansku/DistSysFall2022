import * as mongoDB from "mongodb";
import * as dotenv from "dotenv";

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

    return `Successfully connected to database: ${db.databaseName} `;
}