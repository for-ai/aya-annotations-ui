import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

import Task1 from "./Task1.jsx";
import Task2 from "./Task2.jsx";
import Task3 from "./Task3.jsx";

const TaskSwitcher = () => {
  const location = useLocation();

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = "";
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      // Clean up by removing the event listener when the component unmounts
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);

  useEffect(() => {
    // Do something when the query parameter changes
  }, [location]);

  const renderComponent = () => {
    const queryParams = new URLSearchParams(location.search);
    const componentParam = queryParams.get("task");

    switch (componentParam) {
      case "1":
        return <Task1 />;
      case "2":
        return <Task2 />;
      case "3":
        return <Task3 />;
      default:
        return <Task1 />;
    }
  };

  return <div>{renderComponent()}</div>;
};

export default TaskSwitcher;
