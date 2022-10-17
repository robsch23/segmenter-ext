import {
  Box,
  Center,
  Flex,
  HStack,
  Image,
  Link,
  Spacer,
  Stack,
} from "@chakra-ui/react";

import logo from "./assets/loko.svg";

export function Page({ children }) {
  return (
    <Flex direction={"column"} w="100%" h="100%" mt="0">
      {children}
      <HStack w="100%" h="100%" align="center" bg="orange.200" mt="0">
        <Spacer />
        <Image src={logo} alt="LoKo Icon" h="20px" w="20px" />
        <Box as={Link} href="http://loko-ai.com" target="_blank">
          Powered by Loko.ai
        </Box>
        <Spacer />
      </HStack>
    </Flex>
  );
}
