import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Container,
  Flex,
  HStack,
  Link,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  VStack,
  useMediaQuery,
  useToast,
} from "@chakra-ui/react";
import { BsFillArrowLeftCircleFill } from "react-icons/bs";
import { useNavigate } from "react-router-dom";
import Select from "react-select";

import { getLanguageOptions } from "../helpers/language.jsx";
import {
  getDailyLeaderboard,
  getLanguageLeaderboard,
  getOverallLeaderboard,
  getWeeklyLeaderboard,
} from "../helpers/leaderboard";
import { getUser, getUserLanguages } from "../helpers/user.jsx";
import LeaderBoardOverallDetailsRow from "./LeaderBoardOverallDetailsRow";
import LeaderBoardOverallRow from "./LeaderBoardOverallRow";
import LeaderBoardRow from "./LeaderBoardRow";

function getMondayOfCurrentWeek(dateString) {
  // Parse the date string into a Date object
  let date = new Date(dateString.replace(/-/g, "/"));

  let day = date.getDay();
  let diff = date.getDate() - day + (day === 0 ? -6 : 1); // adjust when day is Sunday

  // Create new Date with calculated difference
  let monday = new Date(date.setDate(diff));

  // Format Date object to YYYY-MM-DD string
  let year = monday.getFullYear();
  let month = monday.getMonth() + 1; // JavaScript months are 0-based
  let dayOfMonth = monday.getDate();

  // Pad month and day with leading zeros if necessary
  month = month < 10 ? "0" + month : month;
  dayOfMonth = dayOfMonth < 10 ? "0" + dayOfMonth : dayOfMonth;

  return `${year}-${month}-${dayOfMonth}`;
}

function LeaderBoardDisplay() {
  const toast = useToast();
  const [data, setData] = useState([]);
  const [currentUserData, setCurrentUserData] = useState({});

  const [userId, setUserId] = useState(null);
  const [tabIndex, setTabIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const [languages, setLanguages] = useState([]);
  const [languageOptionsListed, setLanguageOptionsListed] = useState([]);
  const [selectedLanguageCode, setSelectedLanguageCode] = useState(null);
  const [userLanguages, setUserLanguages] = useState([]);
  const [userLanguageOptionsListed, setUserLanguageOptionsListed] = useState(
    []
  );
  const [groupOptions, setGroupOptions] = useState([]);

  const [overallData, setOverallData] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const recordsPerPage = 20;
  const [isLargerScreen] = useMediaQuery("(min-width: 768px)");

  useEffect(() => {
    const user = getUser();
    if (user && user.id) {
      setUserId(user.id);
    }

    // Fetch the user's language list
    (async () => {
      const fetchedLanguages = await getUserLanguages();
      const allLanguages = await getLanguageOptions();
      setLanguages(allLanguages);
      setUserLanguages(fetchedLanguages);
    })();
  }, []);

  useEffect(() => {
    setLanguageOptionsListed(
      languages.map((option) => ({
        value: option.code,
        label: option.name,
      }))
    );
  }, [languages]);

  useEffect(() => {
    setUserLanguageOptionsListed(
      userLanguages.map((option) => ({
        value: option.code,
        label: option.name,
      }))
    );
  }, [userLanguages]);

  useEffect(() => {
    const value =
      userLanguageOptionsListed.length > 0
        ? userLanguageOptionsListed[0].value
        : null;

    const groupOptions = [
      {
        label: "My Languages",
        options: userLanguageOptionsListed,
      },
      {
        label: "All Languages",
        options: languageOptionsListed,
      },
    ];
    setSelectedLanguageCode(value);
    setGroupOptions(groupOptions);
  }, [languageOptionsListed, userLanguages]);

  useEffect(() => {
    const fetchData = async () => {
      await fetchOverallLeaderboard(userId, currentPage, recordsPerPage);
    };
    fetchData();
  }, [currentPage]);

  const getCurrentDate = () => {
    const currentDate = new Date();
    return `${currentDate.getFullYear()}-${
      currentDate.getMonth() + 1
    }-${currentDate.getDate()}`;
  };

  const fetchDailyLeaderboard = async (userID) => {
    const dailyData = await getDailyLeaderboard(userID, getCurrentDate());
    if (dailyData.records.length === 0) {
      toast({
        title: "No Contributions Today",
        description:
          "That means if you make a contribution now, you'll be at the top of the leaderboard!",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
    }
    setData(dailyData.records);
    setCurrentUserData(dailyData.current_user);
  };

  const fetchWeeklyLeaderboard = async (userID) => {
    const weeklyData = await getWeeklyLeaderboard(
      userID,
      getMondayOfCurrentWeek(getCurrentDate())
    );
    if (weeklyData.records.length === 0) {
      toast({
        title: "No Contributions this week!",
        description:
          "That means if you make a contribution now, you'll be at the top of the leaderboard!",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
    }
    setData(weeklyData.records);
    setCurrentUserData(weeklyData.current_user);
  };

  const fetchOverallLeaderboard = async (
    userID,
    currentPage,
    recordsPerPage
  ) => {
    const offset = (currentPage - 1) * recordsPerPage;
    const overallData = await getOverallLeaderboard(
      userID,
      offset,
      recordsPerPage
    );
    setOverallData(overallData);
    if (overallData.records.length === 0) {
      toast({
        title: "No Contributions ever!",
        description:
          "That means if you make a contribution now, you'll be at the top of the leaderboard!",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
    }
    setData(overallData.records);
    setCurrentUserData(overallData.current_user);
  };

  const fetchLanguageLeaderboard = async (userID) => {
    const langData = await getLanguageLeaderboard(userID, selectedLanguageCode);
    if (langData.records.length === 0) {
      toast({
        title: "No Contributions for this Language!",
        description:
          "That means if you make a contribution now, you'll be at the top of the leaderboard!",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
    }
    setData(langData.records);
    setCurrentUserData(langData.current_user);
  };

  const handleTabChange = async (userID, index) => {
    setIsLoading(true);
    setTabIndex(index);
    const userCurrentLanguage = userLanguageOptionsListed[0]?.value || null;
    switch (index) {
      case 0:
        await fetchDailyLeaderboard(userID);
        break;
      case 1:
        await fetchWeeklyLeaderboard(userID);
        break;
      case 2:
        await fetchOverallLeaderboard(userID, currentPage, recordsPerPage);
        break;
      case 3:
        setSelectedLanguageCode(userCurrentLanguage);
        await fetchLanguageLeaderboard(userID);
        break;
      default:
        break;
    }

    setIsLoading(false);
  };

  useEffect(() => {
    fetchDailyLeaderboard(userId);
  }, [userId]);

  useEffect(() => {
    if (selectedLanguageCode && tabIndex === 3) {
      fetchLanguageLeaderboard(userId);
    }
  }, [selectedLanguageCode, tabIndex]);

  const handleLanguageChange = (value) => {
    setSelectedLanguageCode(value);
  };

  const handleFirstPage = () => {
    setCurrentPage(1);
  };

  const handleLastPage = () => {
    setCurrentPage(Math.ceil(overallData.total_count / recordsPerPage));
  };

  const handleNextPage = () => {
    if (!overallData) {
      console.log("Data is not yet available");
      return;
    }

    if (currentPage < Math.ceil(overallData.total_count / recordsPerPage)) {
      setCurrentPage((prevPage) => prevPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const navigate = useNavigate();

  return (
    <>
      <Container maxW={{ base: "90%", md: "xl" }}>
        <VStack
          py={{ base: "4", md: "14" }}
          alignItems="center"
          justifyContent="center"
          spacing={{ base: "1rem", md: "3rem" }}
        >
          <Flex justify="space-between" align="center" w="full">
            <BsFillArrowLeftCircleFill
              size="2rem"
              color="#3182CE"
              onClick={() => navigate("/workspace?task=1")}
            />
            <Text fontSize={{ base: "4xl", md: "6xl" }} fontWeight="bold">
              Leaderboard
            </Text>
            <Box></Box>
          </Flex>
          {isLoading ? (
            <Box>Loading...</Box>
          ) : (
            <Tabs
              variant="soft-rounded"
              colorScheme="blue"
              onChange={(index) => handleTabChange(userId, index)}
              index={tabIndex}
            >
              <TabList
                px={{ base: "3", md: "6" }}
                py={{ base: "2", md: "3" }}
                display="flex"
                justifyContent="center"
                className="rounded-xl text-white"
              >
                <Tab
                  className="base:mr-2 md:mr-8"
                  _selected={{ color: "white", bg: "green.500" }}
                >
                  Daily
                </Tab>
                <Tab
                  className="base:mr-2 md:mr-8"
                  _selected={{ color: "white", bg: "green.500" }}
                >
                  Weekly
                </Tab>
                <Tab
                  className="base:mr-2 md:mr-8"
                  _selected={{ color: "white", bg: "green.500" }}
                >
                  Overall
                </Tab>
                <Tab
                  className="base:mr-2 md:mr-8"
                  _selected={{ color: "white", bg: "green.500" }}
                >
                  Language
                </Tab>
              </TabList>
              <TabPanels>
                {/* First TabPanel */}
                <TabPanel>
                  <VStack
                    spacing={0}
                    className="rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    {data.map((item) => (
                      <LeaderBoardRow {...item} />
                    ))}
                  </VStack>
                  <VStack
                    spacing={0}
                    className="mt-8 rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    <LeaderBoardRow {...currentUserData} />
                  </VStack>
                </TabPanel>
                {/* Second TabPanel */}
                <TabPanel>
                  <VStack
                    spacing={0}
                    className="rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    {data.map((item) => (
                      <LeaderBoardRow {...item} />
                    ))}
                  </VStack>
                  <VStack
                    spacing={0}
                    className="mt-8 rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    <LeaderBoardRow {...currentUserData} />
                  </VStack>
                </TabPanel>
                {/* Third TabPanel */}
                <TabPanel>
                  <VStack
                    spacing={0}
                    className="mb-2 rounded-2xl bg-slate-800 px-6 py-4 text-white md:px-12"
                  >
                    <LeaderBoardOverallDetailsRow showLanguage={true} />
                  </VStack>
                  <VStack
                    spacing={0}
                    className="rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    {data.map((item) => (
                      <LeaderBoardOverallRow
                        {...item}
                        enableBlendedRank={true}
                      />
                    ))}
                  </VStack>
                  <VStack
                    spacing={0}
                    className="mt-8 rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    {/* here is the current user information at the bottom of each page*/}
                    <LeaderBoardOverallRow
                      {...currentUserData}
                      enableBlendedRank={true}
                    />
                  </VStack>
                  {/* Add the pagination code only in the Overall tab */}
                  <HStack
                    display="flex"
                    justifyContent="center"
                    spacing={4}
                    my={4}
                  >
                    <Button onClick={handleFirstPage} colorScheme="green">
                      <Link>First</Link>
                    </Button>
                    <Button onClick={handlePreviousPage} colorScheme="green">
                      <Link>Previous</Link>
                    </Button>
                    {overallData && (
                      <Text>
                        {currentPage}/
                        {Math.ceil(overallData.total_count / recordsPerPage)}
                      </Text>
                    )}
                    <Button onClick={handleNextPage} colorScheme="green">
                      <Link>Next</Link>
                    </Button>
                    <Button onClick={handleLastPage} colorScheme="green">
                      <Link>Last</Link>
                    </Button>
                  </HStack>
                </TabPanel>
                {/* Fourth TabPanel */}
                <TabPanel>
                  <Select
                    className="basic-single mb-4 ml-auto w-2/5 rounded-full bg-black md:w-1/4"
                    classNamePrefix="select"
                    isSearchable={true}
                    isClearable={false}
                    name="Language"
                    defaultValue={userLanguageOptionsListed[0]}
                    options={groupOptions}
                    onChange={(selectedOption) => {
                      const value = selectedOption
                        ? selectedOption.value
                        : userLanguageOptionsListed?.[0]?.value || null;
                      handleLanguageChange(value);
                    }}
                    sx={{
                      borderRadius: "9999px",
                      zIndex: "10",
                    }}
                  />
                  <VStack
                    spacing={0}
                    className="mb-2 rounded-2xl bg-slate-800 px-6 py-4 text-white md:px-12"
                  >
                    <LeaderBoardOverallDetailsRow showLanguage={false} />
                  </VStack>
                  <VStack
                    spacing={0}
                    className="rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    {data.map((item) => (
                      <LeaderBoardOverallRow
                        {...item}
                        enableBlendedRank={true}
                      />
                    ))}
                  </VStack>
                  <VStack
                    spacing={0}
                    className="mt-8 rounded-2xl bg-slate-800 px-6 py-8 text-white md:px-12"
                  >
                    <LeaderBoardOverallRow
                      {...currentUserData}
                      enableBlendedRank={true}
                    />
                  </VStack>
                </TabPanel>
              </TabPanels>
            </Tabs>
          )}
        </VStack>
      </Container>
    </>
  );
}

export default LeaderBoardDisplay;
