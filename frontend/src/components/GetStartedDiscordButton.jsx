import React, { useEffect, useState } from "react";
import { Image } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

import { handleLogin, isAuthenticated } from "../helpers/auth.jsx";

export const GetStartedDiscordButton = () => {
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
      await handleLogin("discord");
      const isUserAuthenticated = await isAuthenticated();
      setAuthenticated(isUserAuthenticated);
    } else {
      navigateTo("/workspace");
    }
  };

  return (
    <button
      onClick={handleButtonClick}
      className="mt-4 inline-flex h-12 w-full flex-row items-center justify-start rounded border-0 bg-aya-color px-3 py-2 font-bold text-white hover:bg-violet-500 focus:outline-none md:mt-0 md:justify-center"
    >
      <Image
        boxSize="2rem"
        borderRadius="full"
        className="mr-2 self-center"
        src="/JCA616_Aya_logo_White_AYA_logo.png"
        alt="The Aya Project"
      />
      <span className="text-lg">
        {authenticated ? "Go to workspace" : "Get Started with Discord"}
      </span>
    </button>
  );
};
