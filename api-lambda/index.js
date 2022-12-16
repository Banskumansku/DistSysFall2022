const axios = require('axios');


exports.handler = async (event) => {
    const options = ["https://rough-sea-6787.fly.dev/request-match", "https://autumn-thunder-7459.fly.dev/request-match", "https://hidden-haze-6040.fly.dev/request-match"]

    try {
        const randomInt = getRandomInt(3)
        console.log(randomInt)
        const asd = await axios.post(options[randomInt], event.body)
        console.log(asd.data)
        return getResponse(asd.data);
    } catch (error) {
        try {
            const asd = await axios.post(options[getRandomInt(3)], event.body)
            return getResponse(asd.data);
        } catch (error) {
            try {
                const asd = await axios.post(options[getRandomInt(3)], event.body)
                return getResponse(asd.data);
            } catch (error) {
               return getResponse("error")
            }
        }
    }
};


const getRandomInt = (max) => {
    return Math.floor(Math.random() * max);
}

const getResponse = (body) => {
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
        },
        body: body,
    };
}