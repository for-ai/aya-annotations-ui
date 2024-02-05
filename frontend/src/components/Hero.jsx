import React from "react";
import {
  Box,
  Container,
  Flex,
  HStack,
  Image,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Text,
  VStack,
  useBreakpointValue,
  useDisclosure,
} from "@chakra-ui/react";

import { GetStartedDiscordButton } from "./GetStartedDiscordButton.jsx";
import { GetStartedGoogleButton } from "./GetStartedGoogleButton.jsx";

const Hero = () => {
  const direction = useBreakpointValue({ base: "column", md: "row" });
  const imageBoxSize = useBreakpointValue({
    sm: "16rem",
    base: "22rem",
    md: "32rem",
  });
  const displayImage = useBreakpointValue({ base: "none", md: "block" });
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Modal
        isCentered
        size={"xl"}
        closeOnOverlayClick={false}
        isOpen={isOpen}
        onClose={onClose}
      >
        <ModalOverlay bg="blackAlpha.300" backdropFilter="blur(10px)" />
        <ModalContent
          px={{ base: "1rem", md: "3rem" }}
          py={{ base: "3rem", md: "7rem" }}
        >
          <ModalHeader mx={"auto"}>Sign In/Sign Up</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <VStack spacing={4}>
              <GetStartedDiscordButton />
              <GetStartedGoogleButton />
            </VStack>
          </ModalBody>
        </ModalContent>
      </Modal>
      <Container
        maxW="100%"
        px={{ base: "1rem", md: "3rem" }}
        py={{ base: "3rem", md: "11rem" }}
      >
        <HStack
          direction={direction}
          spacing={{ base: "5rem", md: "12rem" }}
          align="center"
          justify="center"
        >
          <VStack spacing={8} w={{ base: "75%", md: "30%" }} align="start">
            <Box
              className="bg-aya-color-very-light"
              px={{ base: "2rem", md: "3rem" }}
              py={"0.75rem"}
              borderRadius="xl"
            >
              <Text className="text-aya-color" fontWeight="medium">
                Cohere For AI
              </Text>
            </Box>
            <Text
              className="text-aya-color"
              fontSize={{ base: "2xl", md: "4xl" }}
              fontWeight="bold"
            >
              Aya: An Open Science Initiative to Accelerate Multilingual AI
              Progress
            </Text>
            <Text
              className="text-aya-color-light"
              fontSize={{ base: "md", md: "xl" }}
            >
              Our goal is to accelerate NLP breakthroughs for the rest of the
              world’s languages through open science collaboration.
            </Text>
            <Flex
              direction={{ base: "column", md: "row" }}
              align="center"
              className="x-4 space-y md:space-x-4 md:space-y-0"
            >
              <Box flexShrink={0} minWidth="200px">
                <a
                  href="https://discord.gg/PKy437NW3y"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="discord-button-link"
                >
                  <button
                    className="
                      mt-4
                      inline-flex
                      h-12
                      w-full
                      items-center
                      justify-center
                      rounded
                      border-0
                      bg-discord-color
                      px-3
                      py-2.5
                      font-bold
                      text-white
                      hover:bg-violet-600
                      focus:outline-none
                      md:mt-0"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      fill="currentColor"
                      className="bi bi-discord mr-2 self-center"
                      viewBox="0 0 16 16"
                    >
                      <path d="M13.545 2.907a13.227 13.227 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.19 12.19 0 0 0-3.658 0 8.258 8.258 0 0 0-.412-.833.051.051 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.041.041 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032c.001.014.01.028.021.037a13.276 13.276 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019c.308-.42.582-.863.818-1.329a.05.05 0 0 0-.01-.059.051.051 0 0 0-.018-.011 8.875 8.875 0 0 1-1.248-.595.05.05 0 0 1-.02-.066.051.051 0 0 1 .015-.019c.084-.063.168-.129.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.052.052 0 0 1 .053.007c.08.066.164.132.248.195a.051.051 0 0 1-.004.085 8.254 8.254 0 0 1-1.249.594.05.05 0 0 0-.03.03.052.052 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.235 13.235 0 0 0 4.001-2.02.049.049 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.034.034 0 0 0-.02-.019Zm-8.198 7.307c-.789 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612Zm5.316 0c-.788 0-1.438-.724-1.438-1.612 0-.889.637-1.613 1.438-1.613.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612Z" />
                    </svg>
                    <span>Join Aya Discord</span>
                  </button>
                </a>
              </Box>
              <button
                onClick={onOpen}
                className="mt-4 inline-flex h-12 w-full flex-row items-center justify-start rounded border-0 bg-aya-color px-3 py-2 font-bold text-white hover:bg-violet-500 focus:outline-none md:mt-0 md:justify-center"
              >
                <Image
                  boxSize="2rem"
                  borderRadius="full"
                  className="mr-2 self-center"
                  src="/JCA616_Aya_logo_White_AYA_logo.png"
                  alt="The Aya Project"
                />
                <span className="text-lg">Sign In/ Sign Up</span>
              </button>
            </Flex>
          </VStack>
          <Box display={displayImage}>
            <Image
              boxSize={imageBoxSize}
              src="/JCA616_Aya_logo_blue_AYA_logo.png"
            />
          </Box>
        </HStack>
      </Container>
    </>
  );
};

export default Hero;
