import React from "react";
import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const Error404 = () => {
  const navigateTo = useNavigate();
  const redirectToHome = () => navigateTo("/");

  return (
    <div>
      <h1>401 Error</h1>
      <p>Sorry, you are not authorized to visit this page.</p>
      <p>Please go to the home page and log in again.</p>
      <Button onClick={redirectToHome}>Go Home</Button>
    </div>
  );
};

export default Error404;
