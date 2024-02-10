import React from "react";
import { Button } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const Error404 = () => {
  const navigateTo = useNavigate();
  const redirectToHome = () => navigateTo("/");

  return (
    <div>
      <h1>404 Error</h1>
      <p>Sorry, the page you're looking for doesn't exist.</p>
      <Button onClick={redirectToHome}>Go Home</Button>
    </div>
  );
};

export default Error404;
