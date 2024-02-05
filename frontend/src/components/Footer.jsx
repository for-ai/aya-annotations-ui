import React from "react";
import {
  Box,
  Flex,
  HStack,
  Image,
  Link,
  Spacer,
  Text,
  useBreakpointValue,
} from "@chakra-ui/react";

const Footer = () => {
  const isMobileScreen = useBreakpointValue({ base: true, md: false });
  const boxSize = useBreakpointValue({ base: "1.5rem", md: "2rem" });
  const fontSize = useBreakpointValue({ base: "sm", md: "md", lg: "xl" });

  return (
    <Box maxW={"100%"} bg="gray.800" px={{ base: 4, md: 20 }} py={4}>
      <Flex
        direction={isMobileScreen ? "column" : "row"}
        justify="space-between"
        alignItems="center"
      >
        <Text fontSize="sm" color="white">
          Made by the C4AI Open Science Community.
        </Text>
        {isMobileScreen && <Spacer />}
        <Box>
          <HStack justify={isMobileScreen ? "flex-start" : "center"}>
            <Link
              href="https://cohere.for.ai/"
              _hover={{ textDecoration: "none" }}
            >
              <Image
                boxSize={boxSize}
                borderRadius="full"
                src="/JCA616_Aya_logo_White_AYA_logo.png"
                alt="The Aya Project"
              />
            </Link>
            <Text
              ml={2}
              fontSize={fontSize}
              fontWeight="semibold"
              color="white"
            >
              The Aya Project
            </Text>
          </HStack>
        </Box>
        {isMobileScreen && <Spacer />}
      </Flex>
    </Box>
  );
};

export default Footer;
