import { ChakraProvider, useDisclosure } from "@chakra-ui/react";
import theme from "./theme";
import Layout from "./components/Layout";
import ConnectButton from "./components/ConnectButton";
import AccountModal from "./components/AccountModal";
import Center from "./components/Main";
import "@fontsource/inter";
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import { useParams } from "react-router"
import { useEffect } from "react"


function App() {  
  return (
    <BrowserRouter>
      <Routes>
            <Route path="/" element={<Center/>}/>
            <Route path="/:discordID" element={<Center/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
