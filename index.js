const express = require('express')
const app = express()
const port = 3001
var Mongoose = require('mongoose')
require('./db/index')
require('./db/model/user')
var cors = require('cors')

const User = Mongoose.model('User');

//const userModel = require('./model')

app.use(express.json())
app.use(cors('*'))
/*
app.use(function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers');
  next();
});*/

app.post('/connect',async function (req,res,next){
  const{ discordID, address } = req.body
  try {
    const user = new User({
      discordID,
      address
    })
    return res.json(await user.save());
  } catch (e) {
    return res.status(401)
  }

})

app.post('/userexists', async function (req,res,next){
  const {address} = req.body
  try {
    const user = await User.findOne({address: address})
    console.log(user)
    res.json(user)
  } catch (e) {
    res.status(401)
  }
})

app.get('/', (req, res) => {
  res.send('eth_bot API!');
})

app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})
