import { Button, Box, Text } from "@chakra-ui/react";
import { useEthers, useEtherBalance } from "@usedapp/core";
import { formatEther } from "@ethersproject/units";
import Identicon from "./Identicon";
import { useParams } from "react-router"
import { useEffect,useState } from "react"
const axios = require('axios');

type Props = {
  handleOpenModal: any,
};

export default function ConnectButton({ handleOpenModal}: Props) {
  const { activateBrowserWallet, account } = useEthers();
  const etherBalance = useEtherBalance(account);
  let { discordID } = useParams()
  const [display, setDisplay] = useState(discordID)

  function handleConnectWallet() {
    activateBrowserWallet();
  }

  useEffect(() => {

    if (account === undefined || discordID === undefined ) return
    console.log("Verifying...")
    
    const connect = async () => {
      try {
        const res = await axios.post(`http://localhost:3001/userexists`,{
          address: account
        })
        console.log(res)
        if (res.data !== null){
          if(discordID !== res.data.discordID) {
            setDisplay("Address already connected.")
          }
          return
        }

        const result = await axios.post(`http://localhost:3001/connect`,{
          discordID: discordID,
          address: account
        })
        console.log(result.data)
      } catch (e) {
         console.log("API call failed")
      }
    } 
    connect();
  }, [account]);

  return account ? (
    <Box
      display="flex"
      alignItems="center"
      background="gray.700"
      borderRadius="xl"
      py="0"
    >
      <Box px="3">
        <Text color="white" fontSize="md">
          {etherBalance && parseFloat(formatEther(etherBalance)).toFixed(3)} ETH
        </Text>
      </Box>
      <Box px="3">
        <Text color="white" fontSize="md">
          {display} DiscordID
        </Text>
      </Box>
      <Button
        onClick={handleOpenModal}
        bg="gray.800"
        border="1px solid transparent"
        _hover={{
          border: "1px",
          borderStyle: "solid",
          borderColor: "blue.400",
          backgroundColor: "gray.700",
        }}
        borderRadius="xl"
        m="1px"
        px={3}
        height="38px"
      >
        <Text color="white" fontSize="md" fontWeight="medium" mr="2">
          {account &&
            `${account.slice(0, 6)}...${account.slice(
              account.length - 4,
              account.length
            )}`}
        </Text>
        <Identicon />
      </Button>
    </Box>
  ) : (
    <Button
      onClick={handleConnectWallet}
      bg="blue.800"
      color="blue.300"
      fontSize="lg"
      fontWeight="medium"
      borderRadius="xl"
      border="1px solid transparent"
      _hover={{
        borderColor: "blue.700",
        color: "blue.400",
      }}
      _active={{
        backgroundColor: "blue.800",
        borderColor: "blue.700",
      }}
    >
      Connect to a wallet
    </Button>
  );
}