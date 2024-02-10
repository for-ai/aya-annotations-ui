import React from "react";
import { HStack, IconButton } from "@chakra-ui/react";
import { FaRegThumbsDown, FaRegThumbsUp } from "react-icons/fa";

const ThumbsUpDownDisplay = ({ value }) => {
  return (
    <HStack spacing={1}>
      {value === 1 && (
        <IconButton
          aria-label="thumbs up"
          icon={<FaRegThumbsUp size={"1.4rem"} color="green" />}
          colorScheme="green"
          variant="outline"
          size={{ base: "md", md: "lg" }}
          isDisabled={true}
        />
      )}

      {value === 0 && (
        <IconButton
          aria-label="thumbs down"
          icon={<FaRegThumbsDown size={"1.4rem"} color="red" />}
          colorScheme="red"
          variant="outline"
          size={{ base: "md", md: "lg" }}
          isDisabled={true}
        />
      )}
    </HStack>
  );
};

export default ThumbsUpDownDisplay;
