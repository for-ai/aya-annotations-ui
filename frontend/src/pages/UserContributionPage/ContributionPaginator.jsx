import React from "react";
import {
  Box,
  Button,
  HStack,
  Heading,
  SimpleGrid,
  Text,
  VStack,
} from "@chakra-ui/react";

import ContributionCard from "./ContributionCard.jsx";

const ContributionPaginator = ({
  contributions,
  selectedContribution,
  setSelectedContribution,
  currentPages,
  setCurrentPages,
  activeTaskType,
  taskType,
  recordsPerPage,
}) => {
  const handleFirstPage = () => {
    setCurrentPages((prevPages) => ({
      ...prevPages,
      [activeTaskType]: 1,
    }));
  };

  const handleLastPage = () => {
    if (!contributions[activeTaskType]) {
      console.log("Data is not yet available");
      return;
    }
    setCurrentPages((prevPages) => ({
      ...prevPages,
      [activeTaskType]: Math.ceil(
        contributions[activeTaskType].total_count / recordsPerPage
      ),
    }));
  };

  const handleNextPage = () => {
    if (!contributions[activeTaskType]) {
      console.log("Data is not yet available");
      return;
    }
    if (
      currentPages[activeTaskType] <
      Math.ceil(contributions[activeTaskType].total_count / recordsPerPage)
    ) {
      setCurrentPages((prevPages) => ({
        ...prevPages,
        [activeTaskType]: prevPages[activeTaskType] + 1,
      }));
    }
  };

  const handlePreviousPage = () => {
    if (currentPages[activeTaskType] > 1) {
      setCurrentPages((prevPages) => ({
        ...prevPages,
        [activeTaskType]: prevPages[activeTaskType] - 1,
      }));
    }
  };

  return (
    <VStack
      spacing={0}
      w="300px"
      marginRight={4}
      boxShadow="md"
      borderRadius="md"
      bg="white"
      rounded="2xl"
    >
      <Box flex="1" w="100%" maxHeight="700px" overflowY="auto" p="2">
        <SimpleGrid spacing="2">
          <Heading size="md" mb="4" textAlign="center">
            {`${
              taskType.charAt(0).toUpperCase() + taskType.slice(1)
            } Contributions`}
          </Heading>
          {contributions[taskType]?.results?.map((contribution, cIndex) => (
            <ContributionCard
              key={cIndex}
              contribution={contribution}
              selected={selectedContribution[taskType] === cIndex}
              onSelect={() => {
                setSelectedContribution((prev) => ({
                  ...prev,
                  [taskType]: cIndex,
                }));
              }}
            />
          ))}
        </SimpleGrid>
      </Box>
      <Box w="100%" borderTop="1px solid #E2E8F0" p="2">
        <HStack display="flex" justifyContent="center" spacing={3}>
          <Button onClick={handleFirstPage} colorScheme="green">
            First
          </Button>
          <Button onClick={handlePreviousPage} colorScheme="green">
            Prev
          </Button>
          {contributions[taskType] && (
            <Text>
              {currentPages[activeTaskType]}/
              {Math.ceil(contributions[taskType].total_count / recordsPerPage)}
            </Text>
          )}
          <Button onClick={handleNextPage} colorScheme="green">
            Next
          </Button>
          <Button onClick={handleLastPage} colorScheme="green">
            Last
          </Button>
        </HStack>
      </Box>
    </VStack>
  );
};

export default ContributionPaginator;
