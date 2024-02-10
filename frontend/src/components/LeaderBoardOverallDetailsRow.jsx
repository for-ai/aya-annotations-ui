import React from "react";
import {
  Grid,
  GridItem,
  HStack,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverCloseButton,
  PopoverContent,
  PopoverHeader,
  PopoverTrigger,
  Text,
  useMediaQuery,
} from "@chakra-ui/react";
import { BsPatchQuestion } from "react-icons/bs";

function LeaderBoardOverallDetailsRow(showLanguage) {
  const [isLargerScreen] = useMediaQuery("(min-width: 768px)");

  return (
    <>
      <Grid
        templateColumns={{ base: "repeat(7, 3rem)", md: "repeat(10, 7rem)" }}
        align="center"
        className="rounded py-3"
      >
        <GridItem colSpan={1}>
          <Text className="font-bold">Rank</Text>
        </GridItem>
        <GridItem colSpan={{ base: 3, md: 4 }}>
          <Text className="font-bold">Username</Text>
        </GridItem>
        {showLanguage ? (
          <GridItem colSpan={2}>
            <Text className="font-bold">Languages</Text>
          </GridItem>
        ) : (
          <GridItem colSpan={2}>
            <Text className="font-bold"></Text>
          </GridItem>
        )}
        {isLargerScreen && (
          <>
            <GridItem colSpan={1}>
              <Text className="font-bold">Points</Text>
            </GridItem>
            <GridItem colSpan={1}>
              <Text className="font-bold">Quality</Text>
            </GridItem>
          </>
        )}
        <GridItem colSpan={1}>
          <Popover placement="right">
            <PopoverTrigger>
              <HStack spacing={1}>
                <Text className="font-bold">Aya Score</Text>
                <BsPatchQuestion className="text-white" />
              </HStack>
            </PopoverTrigger>
            <PopoverContent className="text-slate-600">
              <PopoverArrow />
              <PopoverCloseButton />
              <PopoverHeader>
                <strong>What is Aya Score?</strong>
              </PopoverHeader>
              <PopoverBody>
                Aya Score accounts for quality of edits to boost the points of
                users who make high quality edits. It is based upon the quality
                score computed from task 3, thumbs up and thumbs down received,
                task 2 contributions, and tasks further edited in task 3.
              </PopoverBody>
            </PopoverContent>
          </Popover>
        </GridItem>
      </Grid>
    </>
  );
}

export default LeaderBoardOverallDetailsRow;
