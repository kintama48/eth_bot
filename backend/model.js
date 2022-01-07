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
  user: "bpksohjnqxghia",
  host: "ec2-34-230-133-163.compute-1.amazonaws.com",
  database: "d91ok380e2boea",
  password: "391cebb8cfc0080ac7f81493ebfa4e6b3b60e081da74b792ef0f9f1e0455a578",
  port: 5432
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
