import React, { useEffect, useState } from "react";
import { Box } from "@chakra-ui/react";
import { useLocation, useNavigate } from "react-router-dom";
import Select from "react-select";

import Footer from "../components/Footer.jsx";
import Navbar from "../components/Navbar.jsx";
import TaskSwitcher from "../components/TaskSwitcher.jsx";

// The Workspace component is responsible for displaying the workspace page
// where users can rate and improve prompts and completions.
const Workspace = () => {
  const location = useLocation();
  const navigateTo = useNavigate();

  // Add a useState hook to keep track of the window's width
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  const handleTaskChange = (selectedOption) => {
    navigateTo(`/workspace?task=${selectedOption.value}`);
  };

  // Push default task value when component mounts
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const taskParam = queryParams.get("task");

    if (taskParam === null) {
      navigateTo(`/workspace?task=1`);
    }
  }, []);

  // This useEffect hook will update windowWidth whenever the window's size changes
  useEffect(() => {
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    window.addEventListener("resize", handleResize);

    // Cleanup after the effect
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const getDefaultTaskValue = () => {
    const queryParams = new URLSearchParams(location.search);
    const taskParam = queryParams.get("task");

    switch (taskParam) {
      case "2":
        return { value: "2", label: "Contribute Your Language" };
      case "3":
        return { value: "3", label: "Review User Feedback" };
      case "1":
        return { value: "1", label: "Rate Model Performance" };
      default:
        return { value: "1", label: "Rate Model Performance" };
    }
  };

  return (
    <>
      <Navbar linkTo="/workspace" />
      <Box maxW={{ base: "90%", md: "60%" }} className="mx-auto mb-12 mt-4">
        <Select
          borderWidth="0"
          className="basic-single"
          classNamePrefix="select"
          isSearchable={false}
          isClearable={false}
          name="Task"
          onChange={handleTaskChange}
          options={[
            { value: "1", label: "Rate Model Performance" },
            { value: "2", label: "Contribute Your Language" },
            { value: "3", label: "Review User Feedback" },
          ]}
          defaultValue={getDefaultTaskValue()}
          styles={{
            control: (provided) => ({
              ...provided,
              width: 250,
              borderRadius: "999px",
              background: "#FFFFFF",
              border: "solid 1px #E2E8F0",
              padding: "0.25rem",
              margin: "auto 16",
              "@media (min-width: 768px)": {
                width: 400,
                borderRadius: "20px",
                fontSize: "1.6rem",
                fontWeight: 500,
              },
            }),
          }}
        />
        <TaskSwitcher />
      </Box>
      <Footer />
    </>
  );
};

export default Workspace;
