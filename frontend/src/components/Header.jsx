import React from "react";
import {
  Box,
  Button,
  Center,
  Flex,
  Heading,
  IconButton,
  Image,
  Link,
  Text,
  useBreakpointValue,
} from "@chakra-ui/react";
import { FaChartPie, FaUsers } from "react-icons/fa";

const Header = () => {
  const breakpoint = useBreakpointValue({ base: "base", lg: "lg", xl: "xl" });

  return (
    <Box px={{ base: "1rem", md: "5rem" }}>
      <Flex align="center" justify="space-between" direction="row">
        <Link href="/" _hover={{ textDecoration: "none" }}>
          <Image
            boxSize={breakpoint === "base" ? "2.5rem" : "3rem"}
            borderRadius="full"
            src="/JCA616_Aya_logo_blue_AYA_logo.png"
            alt="The Aya Project"
          />
        </Link>
        <Flex justify="center" align="center" width="100%">
          {breakpoint === "base" ? (
            <>
              <Center w="100%">
                <Box textAlign="center" mb={5} mt={1} padding={3}>
                  <Heading as="h1" fontSize="xl" color="#4368e0">
                    The Aya Project
                  </Heading>
                  <Text fontSize="md" color="gray.500" mt={1}>
                    A C4AI Community Project
                  </Text>
                </Box>
              </Center>
              <IconButton
                id="gradioAnalyticsButton"
                as="a"
                href="/analytics"
                fontWeight="bold"
                borderRadius="5px"
                border="1px solid"
                variant="outline"
                icon={<FaChartPie />}
                color="#4368e0"
                ml="0.5rem"
              ></IconButton>
            </>
          ) : (
            <Flex width="100%" justify="space-between">
              <Box flex="1" />
              <Box flex="2" textAlign="center" mb={5} mt={2}>
                <Flex align="center" justify="center" direction="column">
                  <Heading as="h1" size="lg" color="#4368e0">
                    The Aya Project
                  </Heading>
                  <Text
                    fontSize="md"
                    className="text-aya-color-light"
                    mt={2}
                    textAlign="center"
                  >
                    A C4AI Community Project
                  </Text>
                </Flex>
              </Box>
              <Box
                flex="1"
                mt={{ base: "2rem", md: "2rem" }}
                textAlign="center"
                mb={5}
              >
                <Flex gap={3}>
                  <Button
                    id="aboutUsButton"
                    as="a"
                    href="/team"
                    fontWeight="bold"
                    borderRadius="5px"
                    border="1px solid"
                    variant="outline"
                    leftIcon={<FaUsers />}
                    color="#4368e0"
                  >
                    The Team
                  </Button>
                  <Button
                    id="gradioAnalyticsButton"
                    as="a"
                    href="/analytics"
                    fontWeight="bold"
                    borderRadius="5px"
                    border="1px solid"
                    variant="outline"
                    leftIcon={<FaChartPie />}
                    color="#4368e0"
                  >
                    Analytics
                  </Button>
                </Flex>
              </Box>
            </Flex>
          )}
        </Flex>
      </Flex>
    </Box>
  );
};

export default Header;
