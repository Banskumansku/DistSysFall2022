import { ObjectId } from "mongodb";

export default class Player {
    constructor(public name: string, public wins: number, public losses: number, public id?: ObjectId) { }
}