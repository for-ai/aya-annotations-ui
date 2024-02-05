import React, { useEffect, useState } from "react";
import { Image } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

import { handleLogin, isAuthenticated } from "../helpers/auth.jsx";

export const GetStartedGoogleButton = () => {
  // useNavigate hook for programmatic navigation
  const navigateTo = useNavigate();
  const [authenticated, setAuthenticated] = useState(false);

  // Check if the user is already authenticated on component mount
  useEffect(() => {
    (async () => {
      const isUserAuthenticated = await isAuthenticated();
      setAuthenticated(isUserAuthenticated);
    })();
  }, []);

  const handleButtonClick = async () => {
    if (!authenticated) {
      await handleLogin("google");
      const isUserAuthenticated = await isAuthenticated();
      setAuthenticated(isUserAuthenticated);
    } else {
      navigateTo("/workspace");
    }
  };

  return (
    <>
      {!authenticated ? (
        <button
          onClick={handleButtonClick}
          className="mt-4 inline-flex h-12 w-full flex-row items-center justify-start rounded border-2 bg-white px-3 py-2 font-bold text-gray-600 hover:bg-gray-100 focus:outline-none md:mt-0 md:justify-center"
        >
          <Image
            boxSize="1.5rem"
            borderRadius="full"
            className="mr-2 self-center"
            src="/google-logo.png"
            alt="The Aya Project"
          />
          <span className="text-lg">Sign In with Google</span>
        </button>
      ) : (
        <></>
      )}
    </>
  );
};
