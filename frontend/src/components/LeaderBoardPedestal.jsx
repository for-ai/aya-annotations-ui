import React from "react";
import { Box, Text, VStack } from "@chakra-ui/react";

function LeaderBoardRow(props) {
  return (
    <Box className="mx-auto h-4 w-1/4 bg-blue-500">
      <VStack className="w-1/4 break-words">
        <Text>NameNameNameNameNameNameNameNameName</Text>
        <Text>700</Text>
        <Text>@UserName</Text>
      </VStack>
    </Box>
  );
}

export default LeaderBoardRow;
