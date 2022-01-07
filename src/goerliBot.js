require('dotenv').config({path: '../.env'})

const utils = require('./utils.js');
const Discord = require('discord.js');
const etherscan = require('./api.js');
const db = require('./db.js');
const Web3 = require('web3');
const web3 = new Web3(new Web3.providers.HttpProvider(process.env.INFURA_HTTPS_ENDPOINT));

const DEFAULT_GAS_PRICE = 1500000000000; // 1,500 gwei

const INELIGIBLE_NO_CUSTOM_CHECKS_MESSAGE = " is ineligible to receive goerli eth.";
const INELIGIBLE_CUSTOM_CHECKS_MESSAGE = " is ineligible to receive goerli eth.  You must pass the custom checks;";

const maxDepositAmount = Number(process.env.MAX_DEPOSIT_AMOUNT) 

const runCustomEligibilityChecks = async (address, topUpAmount) => {
  const res = await db.confirmTransaction(address, topUpAmount/Math.pow(10,18));
  console.log(res)
  return res

}

const receiverIsEligible = async (address, amountRequested, runCustomChecks)  => {
  const needsGoerliEth = true;
  if (runCustomChecks) {
    const passedCustomChecks = await runCustomEligibilityChecks(address, amountRequested);
    return needsGoerliEth && passedCustomChecks;
  } else {
    return needsGoerliEth;
  }
}

const runGoerliFaucet = async (message, address, runCustomChecks) => {

  const currentBalance = await etherscan.getBalance(address);
  if (currentBalance === null) {
    console.log("Something went wrong while connecting to API to recieve balance.");

    if (message) {
      let embed = new Discord.MessageEmbed().setDescription("Something went wrong while getting address details please try again..").
      setTimestamp().setColor(0xff1100);
      message.lineReply(embed);
    }
    return;
  };

  const topUpAmount = maxDepositAmount - (currentBalance);

  if(topUpAmount <= 0 ) {
    console.log("Address has max deposit amount.");

    if (message) {
      let embed = new Discord.MessageEmbed().setDescription("Address has max deposit amount.").
      setTimestamp().setColor(0xff1100);
      message.lineReply(embed);
    }
    return;
  };

  console.log("address " + address + " is requesting " + topUpAmount/Math.pow(10,18) + " goerli eth.  Custom checks: " + runCustomChecks);

  // Make sure the bot has enough Goerli ETH to send
  const faucetReady = await utils.faucetIsReady(process.env.FAUCET_ADDRESS, topUpAmount/Math.pow(10,18));
  if (!faucetReady) {
    console.log("Faucet does not have enough ETH.");

    if (message) {
      let embed = new Discord.MessageEmbed().setDescription("The Bot does not have enough Goerli ETH.  Please contact the maintainers.").
      setTimestamp().setColor(0xff1100);
      message.lineReply(embed);
    }
    return;
  }

  const receiverEligible = await receiverIsEligible(address, topUpAmount, runCustomChecks);
  if (receiverIsEligible === null){
    const m1 = 'Something went wrong while confirming your transaction please try again.'
    if (message) {
      let embed = new Discord.MessageEmbed().setDescription(m1).
      setTimestamp().setColor(3447003);
      message.lineReply(embed);
    }

  }

  if (!receiverEligible) {
    const m = runCustomChecks ? address + INELIGIBLE_CUSTOM_CHECKS_MESSAGE
      : address + INELIGIBLE_NO_CUSTOM_CHECKS_MESSAGE;

    console.log(m);

    if (message) {
      let embed = new Discord.MessageEmbed().setDescription(m).
      setTimestamp().setColor(3447003);
      message.lineReply(embed);
    }

    return;
  }

  console.log("Checks passed - sending to " +  address);
  if (message) {
    let embed = new Discord.MessageEmbed().setDescription("Checks passed - sending...").
    setTimestamp().setColor(3447003);
    message.lineReply(embed);
  }

  const nonce = utils.getCachedNonce();
  utils.sendGoerliEth(message, process.env.FAUCET_ADDRESS, process.env.FAUCET_PRIVATE_KEY, address, topUpAmount, nonce, DEFAULT_GAS_PRICE);
  
  utils.incrementCachedNonce();
}

// This runs once when imported (bot starting) to cache the nonce in a local file
utils.initializeCachedNonce();

module.exports = {
  name: 'goerliBot',
  description: 'Sends goerli eth to the user.',
  execute(message, args, runCustomChecks = true) {
    runGoerliFaucet(message, args[1], runCustomChecks);
  }
} 

utils.initializeCachedNonce();

//runGoerliFaucet(null, "0x066Adead2d82A1C2700b4B48ee82ec952b6b18dA", true);