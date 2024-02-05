import React from "react";
import { HStack, IconButton } from "@chakra-ui/react";
import { FaRegThumbsDown, FaRegThumbsUp } from "react-icons/fa";

// ThumbsUpDown is a React component that renders two buttons (thumbs up and thumbs down)
// with toggling functionality to indicate a positive or negative preference.
const ThumbsUpDown = ({ isThumbsUp, setIsThumbsUp }) => {
  // Handle the thumb button click, toggling the active state of the button
  const handleThumbsUpClick = () => {
    setIsThumbsUp(true);
  };

  const handleThumbsDownClick = () => {
    setIsThumbsUp(false);
  };

  // Render the thumbs up and thumbs down buttons in a horizontal stack
  return (
    <HStack spacing={1}>
      <IconButton
        onClick={handleThumbsUpClick}
        aria-label="thumbs up"
        icon={<FaRegThumbsUp size={"1.4rem"} color="green" />}
        colorScheme="green"
        variant="outline"
        size={{ base: "md", md: "lg" }}
      />
      <IconButton
        onClick={handleThumbsDownClick}
        aria-label="thumbs down"
        icon={<FaRegThumbsDown size={"1.4rem"} color="red" />}
        colorScheme="red"
        variant="outline"
        size={{ base: "md", md: "lg" }}
      />
    </HStack>
  );
};

export default ThumbsUpDown;
