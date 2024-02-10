import React from "react";
import { Box, Container, Text, useBreakpointValue } from "@chakra-ui/react";

function About() {
  const fontSizeTitle = useBreakpointValue({ base: "3xl", md: "5xl" });
  const fontSizeContent = useBreakpointValue({ base: "md", md: "lg" });

  return (
    <Box py="4rem">
      <Container className="mx-auto" minW="50%">
        <Text
          mb="3rem"
          textAlign="center"
          fontSize={fontSizeTitle}
          fontWeight="extrabold"
          className="text-aya-color"
        >
          What is Aya?
        </Text>
        <Text
          textAlign="center"
          fontSize={fontSizeContent}
          className="text-aya-color-light"
        >
          Recent breakthroughs in NLP technology have focused on English,
          leaving other languages behind. One of the biggest hurdles to
          improving multilingual model performance is access to high-quality
          examples of multilingual text. In January 2023 the Cohere For AI
          community set out on an ambitious open science research project.
          <br />
          <br />
          With members from over 100 countries around the world, we sought to
          leverage the great strength of our diversity to make meaningful
          contributions to fundamental machine-learning questions. Our ultimate
          goal is to release a high-quality multilingual dataset. In sharing
          this artifact broadly, we will support future projects that aim to
          build technology for everyone, including those who use any of the
          7,000+ languages spoken around the world. As technological progress
          races forward, join us to ensure no language is left behind.
          <br />
          <br />
          What does the word Aya mean? The word Aya has its origins in the Twi
          language, and is translated to “fern”. Aya is a symbol of endurance,
          resourcefulness and defiance. Similar to our initiatives names, we
          believe it is a long term effort of endurance to make sure that no
          language is left behind.
        </Text>
      </Container>
    </Box>
  );
}

export default About;
