import { ChakraProvider, useDisclosure } from "@chakra-ui/react";
import theme from "../theme";
import Layout from "./Layout";
import ConnectButton from "./ConnectButton";
import AccountModal from "./AccountModal";
import "@fontsource/inter";

export default function Center() {
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <ChakraProvider theme={theme}>
        <Layout>
            <ConnectButton handleOpenModal={onOpen} />
            <AccountModal isOpen={isOpen} onClose={onClose} />
        </Layout>
        </ChakraProvider>
    );
}