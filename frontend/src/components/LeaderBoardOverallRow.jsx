import React from "react";
import {
  Box,
  Divider,
  Grid,
  GridItem,
  Image,
  Text,
  VStack,
  useMediaQuery,
} from "@chakra-ui/react";

function ProfilePicture(props) {
  let imgCfg;
  if (props.rank === 1) {
    imgCfg = "border-yellow-300 border-2 rounded-full";
  } else if (props.rank === 2) {
    imgCfg = "border-gray-400 border-2 rounded-full";
  } else if (props.rank === 3) {
    imgCfg = "border-amber-700 border-2 rounded-full";
  } else {
    imgCfg = "rounded-full";
  }
  return <Image {...props} className={imgCfg} />;
}

function LeaderBoardRow(props) {
  let textCfg;
  const [isLargerScreen] = useMediaQuery("(min-width: 768px)");
  if (props.blended_rank === 1) {
    textCfg = "text-yellow-300 font-bold";
  } else if (props.blended_rank === 2) {
    textCfg = "text-gray-400 font-bold";
  } else if (props.blended_rank === 3) {
    textCfg = "text-amber-700 font-bold";
  } else {
    textCfg = "font-bold";
  }
  return (
    <>
      <Grid
        templateColumns={{ base: "repeat(7, 3rem)", md: "repeat(10, 7rem)" }}
        align="center"
        className="rounded py-3"
      >
        {props.enableBlendedRank ? (
          <>
            <GridItem colSpan={1}>
              <Text className={textCfg}>#{props.blended_rank}</Text>
            </GridItem>
            <GridItem colSpan={1}>
              <ProfilePicture
                borderRadius="full"
                boxSize={{ base: "2.25rem", md: "3rem" }}
                src={props.image_url}
                rank={props.blended_rank}
              />
            </GridItem>
          </>
        ) : (
          <>
            <GridItem colSpan={1}>
              <Text className={textCfg}>#{props.rank}</Text>
            </GridItem>
            <GridItem colSpan={1}>
              <ProfilePicture
                borderRadius="full"
                boxSize={{ base: "2.25rem", md: "3rem" }}
                src={props.image_url}
                rank={props.rank}
              />
            </GridItem>
          </>
        )}
        <GridItem colSpan={{ base: 2, md: 3 }}>
          <VStack spacing={0} align="start">
            <Text>{props.name}</Text>
            <Text>{props.username}</Text>
          </VStack>
        </GridItem>
        <GridItem colSpan={2}>
          <Text>{props.languages ? props.languages.join(", ") : ""}</Text>
        </GridItem>
        {isLargerScreen && (
          <>
            <GridItem colSpan={1}>
              <Text>{props.points}</Text>
            </GridItem>
            <GridItem colSpan={1}>
              <Text>{props.quality_score || "-"}</Text>
            </GridItem>
          </>
        )}
        <GridItem colSpan={1}>
          <Text>{props.blended_points}</Text>
        </GridItem>
      </Grid>
      <Divider />
    </>
  );
}

export default LeaderBoardRow;
