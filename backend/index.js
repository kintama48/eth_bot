const api = require('api.js')
const express = require('express')
const app = express()
const port = 3001

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
  //if (address === undefined) res.status(404)
  console.log(discordID, address)
  userModel.connectDiscordID(discordID, address)
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
})

app.get('/', (req, res) => {
  res.send('Hello world');
})

app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
