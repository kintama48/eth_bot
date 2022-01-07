const { Pool } = require('pg');
const utils = require('./utils.js');
const express = require('express')
const app = express()
// const port = 3001

const userModel = require('./model')

app.use(express.json())
app.use(function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers');
  next();
});

app.post('/connect', (req, res) => {
  const {discordID, address}= req.body
  userModel.connectDiscordID(discordID, address)
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
})

app.get('/', (req, res) => {
  res.send('eth_bot API!');
})

// app.listen(port, () => {
//   console.log(`App running on port ${port}.`)
// })

let pool = new Pool({
  user: "ekmowbdkcnncmr",
  host: "ec2-3-219-131-161.compute-1.amazonaws.com",
  database: "d7qjcjq0ruqbef",
  password: "a1b64a204c91cd8b7bb03ef2461797545bdaf7deea08b75f148c2f23391bdb2d",
  port: 5432,
  ssl: true
})

// let pool = new Pool({
//     user: "hamzaasaad",
//     host: "localhost",
//     database: "hamzaasaad",
//     password: "",
//     port: 5431,
// })

pool.connect();

pool.query('SELECT NOW()', (err, res) => {
    if(err){
        console.log('Database connection failed',err);
    }
    else {
        console.log('Database connected!');
    }
});

async function checkAddressExists(address){
    const select = `
        SELECT * FROM "user" where address= $1
    `;
    const vals=[address]
    const result = await pool.query(select,vals);
    return result.rows;

}
 
module.exports ={
    connectDiscordID: async function (discordID, address){
        const isAccountConnected = await checkAddressExists(address)
        console.log(isAccountConnected)
        if (!isAccountConnected.length){
            const insert = `INSERT INTO "user" (discord_id, address) VALUES ($1,$2);`
            const values = [discordID,address]
            
            const result = await pool.query(insert, values)
            console.log(result)
            return true
        } else {
            console.log(isAccountConnected[0].discord_id)
            return isAccountConnected[0].discord_id
        }
    }
}
