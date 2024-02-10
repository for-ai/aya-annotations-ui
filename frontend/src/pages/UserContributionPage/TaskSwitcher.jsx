import React from "react";
import { Flex, Tab, TabList } from "@chakra-ui/react";

const TaskSwitcher = ({ value }) => {
  return (
    <Flex justifyContent="center">
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
          Task 1
        </Tab>
        <Tab
          className="base:mr-2 md:mr-8"
          _selected={{ color: "white", bg: "green.500" }}
        >
          Task 2
        </Tab>
        <Tab
          className="base:mr-2 md:mr-8"
          _selected={{ color: "white", bg: "green.500" }}
        >
          Task 3
        </Tab>
      </TabList>
    </Flex>
  );
};

export default TaskSwitcher;
