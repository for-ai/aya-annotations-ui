import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardBody,
  Container,
  Heading,
  SimpleGrid,
  Stack,
  Text,
  useBreakpointValue,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

import { handleLogin, isAuthenticated } from "../helpers/auth.jsx";
import { trackButtonClickGA } from "../helpers/ga.jsx";

function HowItWorks() {
  const fontSize = useBreakpointValue({ base: "3xl", md: "5xl" });
  const columns = useBreakpointValue({ base: 1, md: 3 });
  const isSmallScreen = useBreakpointValue({ base: true, md: false });

  const navigateTo = useNavigate();
  const [authenticated, setAuthenticated] = useState(false);

  // Check if the user is already authenticated on component mount
  useEffect(() => {
    (async () => {
      const isUserAuthenticated = await isAuthenticated();
      setAuthenticated(isUserAuthenticated);
    })();
  }, []);

  const handleButtonClick = async (taskId) => {
    if (!authenticated) {
      await handleLogin();
      const isUserAuthenticated = await isAuthenticated();
      setAuthenticated(isUserAuthenticated);
    } else {
      navigateTo(`/workspace?task=${taskId}`);
    }
  };

  return (
    <Box className="bg-blue-900" py="4rem">
      <Container className="mx-auto" minW="75%">
        <Text
          mb="3rem"
          textAlign="center"
          fontSize={fontSize}
          fontWeight="extrabold"
          className="text-white"
        >
          How it Works?
        </Text>
        <SimpleGrid columns={columns} spacing={8}>
          <Card
            align="center"
            border="4px solid"
            borderColor="gray.300"
            boxShadow="lg"
            maxW="sm"
            borderRadius="xl"
            className="mx-auto bg-gradient-to-r from-sky-100 to-sky-200"
          >
            <CardBody>
              <Stack m="1rem" spacing={3}>
                <Heading
                  textAlign="center"
                  fontSize="3xl"
                  fontWeight="extrabold"
                  className="text-blue-900"
                >
                  Rate Model Performance
                </Heading>
                <Text
                  fontSize="md"
                  mx="2rem"
                  fontWeight="medium"
                  className="text-blue-700"
                >
                  You will be asked to rate and edit model data to improve it.
                </Text>
                <div className="text-center">
                  <Button
                    colorScheme="blue"
                    w="75%"
                    onClick={() => {
                      trackButtonClickGA("get-started-button-task-1");
                      handleButtonClick(1);
                    }}
                  >
                    Get Started
                  </Button>
                </div>
              </Stack>
            </CardBody>
          </Card>
          <Card
            align="center"
            border="4px solid"
            borderColor="gray.300"
            boxShadow="lg"
            maxW="sm"
            borderRadius="xl"
            className="mx-auto bg-gradient-to-r from-sky-100 to-sky-200"
          >
            <CardBody>
              <Stack m="1rem" spacing={3}>
                <Heading
                  textAlign="center"
                  fontSize="3xl"
                  fontWeight="extrabold"
                  className="text-blue-900"
                >
                  Contribute Your Language
                </Heading>
                <Text
                  fontSize="md"
                  mx="2rem"
                  fontWeight="medium"
                  className="text-blue-700"
                >
                  You can share your own examples of data that you think is
                  great.
                </Text>
                <div className="text-center">
                  <Button
                    colorScheme="blue"
                    w="75%"
                    onClick={() => {
                      trackButtonClickGA("get-started-button-task-2");
                      handleButtonClick(2);
                    }}
                  >
                    Get Started
                  </Button>
                </div>
              </Stack>
            </CardBody>
          </Card>
          <Card
            align="center"
            border="4px solid"
            borderColor="gray.300"
            boxShadow="lg"
            maxW="sm"
            borderRadius="xl"
            className="mx-auto bg-gradient-to-r from-sky-100 to-sky-200"
          >
            <CardBody>
              <Stack m="1rem" spacing={3}>
                <Heading
                  textAlign="center"
                  fontSize="3xl"
                  fontWeight="extrabold"
                  className="text-blue-900"
                >
                  Review User Feedback
                </Heading>
                <Text
                  fontSize="md"
                  mx="2rem"
                  fontWeight="medium"
                  className="text-blue-700"
                >
                  Audit the work of other contributors to ensure quality and
                  consistency.
                </Text>
                <div className="text-center">
                  <Button
                    colorScheme="blue"
                    w="75%"
                    onClick={() => {
                      trackButtonClickGA("get-started-button-task-3");
                      handleButtonClick(3);
                    }}
                  >
                    Get Started
                  </Button>
                </div>
              </Stack>
            </CardBody>
          </Card>
        </SimpleGrid>
      </Container>
    </Box>
  );
}

export default HowItWorks;
