import React, { useEffect, useState } from "react";
import {
  Box,
  Flex,
  Heading,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  useBreakpointValue,
  useToast,
} from "@chakra-ui/react";

import Navbar from "../../components/Navbar.jsx";
import { getContributions, getUser } from "../../helpers/user.jsx";
import ContributionPaginator from "./ContributionPaginator.jsx";
import ContributionPaginatorSmall from "./ContributionPaginatorSmall.jsx";
import TaskDetails from "./TaskDetails.jsx";
import TaskSwitcher from "./TaskSwitcher.jsx";

const UserContributionPage = () => {
  const RECORDS_PER_PAGE = 20;

  const [userId, setUserId] = useState(null);
  const toast = useToast();

  const isSmallScreen = useBreakpointValue({ base: true, md: false });
  const [isLoading, setIsLoading] = useState(true);

  const [contributions, setContributions] = useState({
    task1: null,
    task2: null,
    task3: null,
  });

  const [selectedContribution, setSelectedContribution] = useState({
    task1: 0,
    task2: 0,
    task3: 0,
  });

  const [currentPages, setCurrentPages] = useState({
    task1: 1,
    task2: 1,
    task3: 1,
  });

  const taskMap = ["task1", "task2", "task3"];
  const [activeTaskType, setActiveTask] = useState(taskMap[0]);

  const [pageOptions, setPageOptions] = useState([]);

  useEffect(() => {
    setIsLoading(true);
    (async () => {
      const user = getUser();
      if (user && user.id) {
        setUserId(user.id);
        await fetchAndUpdateContributions(user.id, "task1", 1, 20);
      }
      setIsLoading(false);
    })();
  }, []);

  useEffect(() => {
    (async () => {
      if (userId) {
        await fetchAndUpdateContributions(
          userId,
          activeTaskType,
          currentPages[activeTaskType],
          RECORDS_PER_PAGE
        );
      }
    })();
  }, [currentPages[activeTaskType], activeTaskType]);

  useEffect(() => {
    if (!contributions || !contributions[activeTaskType]) {
      setPageOptions([]);
      return;
    }

    const options = Array.from(
      {
        length: Math.ceil(
          contributions[activeTaskType].total_count / RECORDS_PER_PAGE
        ),
      },
      (_, index) => ({
        label: `Page ${index + 1}`,
        value: index + 1,
      })
    );

    setPageOptions(options);
  }, [contributions, activeTaskType, RECORDS_PER_PAGE]);

  const handleTabChange = async (index) => {
    const taskType = taskMap[index];
    setActiveTask(taskType);

    // Fetch using the current page for the new task type
    const pageForTask = currentPages[taskType];
    await fetchAndUpdateContributions(
      userId,
      taskType,
      pageForTask,
      RECORDS_PER_PAGE
    );
  };

  const fetchAndUpdateContributions = async (
    userID,
    taskType,
    pageNumber,
    recordsPerPage = 20
  ) => {
    getContributions(userID, taskType, pageNumber, recordsPerPage).then(
      (fetchedContributions) => {
        setContributions((prev) => ({
          ...prev,
          [taskType]: fetchedContributions,
        }));

        if (fetchedContributions.results.length === 0) {
          toast({
            title: "No Contributions for Task!",
            description:
              "That means if you make a contribution now, they will appear here!",
            status: "warning",
            duration: 3000,
            isClosable: true,
          });
        } else {
          return fetchedContributions;
        }
      }
    );
  };

  return (
    <>
      <Navbar linkTo="/my-contributions" />
      <Box p="4">
        <Heading size="lg" align="center" mb="10">
          My Contributions
        </Heading>
        {isLoading ? (
          <Text align="center" mt={5}>
            Loading...
          </Text>
        ) : (
          <Tabs
            variant="soft-rounded"
            colorScheme="blue"
            onChange={handleTabChange}
          >
            <TaskSwitcher></TaskSwitcher>
            {isSmallScreen &&
              contributions &&
              contributions[activeTaskType] &&
              contributions[activeTaskType].results && (
                <ContributionPaginatorSmall
                  contributions={contributions}
                  selectedContribution={selectedContribution}
                  setSelectedContribution={setSelectedContribution}
                  currentPages={currentPages}
                  setCurrentPages={setCurrentPages}
                  activeTaskType={activeTaskType}
                  pageOptions={pageOptions}
                ></ContributionPaginatorSmall>
              )}
            <TabPanels>
              {taskMap.map((taskType, index) => (
                <TabPanel key={index}>
                  <Flex>
                    {!isSmallScreen && (
                      <ContributionPaginator
                        contributions={contributions}
                        selectedContribution={selectedContribution}
                        setSelectedContribution={setSelectedContribution}
                        currentPages={currentPages}
                        setCurrentPages={setCurrentPages}
                        activeTaskType={activeTaskType}
                        taskType={taskType}
                        recordsPerPage={RECORDS_PER_PAGE}
                      ></ContributionPaginator>
                    )}
                    <TaskDetails
                      contributions={contributions}
                      selectedContribution={selectedContribution}
                      activeTaskType={activeTaskType}
                    ></TaskDetails>
                  </Flex>
                </TabPanel>
              ))}
            </TabPanels>
          </Tabs>
        )}
      </Box>
    </>
  );
};

export default UserContributionPage;
