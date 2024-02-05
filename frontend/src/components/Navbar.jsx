import React, { useEffect, useState } from "react";
import {
  Avatar,
  Box,
  Button,
  Flex,
  Image,
  Link,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  Spacer,
  useBreakpointValue,
} from "@chakra-ui/react";
import { MdLeaderboard } from "react-icons/all.js";
import { useNavigate } from "react-router-dom";

import { handleLogout } from "../helpers/auth.jsx";
import { trackButtonClickGA } from "../helpers/ga.jsx";

// The Navbar component is responsible for displaying the header
// with the Cohere for AI logo, the leaderboard button, and the user menu.
const Navbar = ({ linkTo = "/" }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const isSmallScreen = useBreakpointValue({ base: true, md: false });

  const navigateTo = useNavigate();

  const navigateToHome = () => {
    navigateTo("/");
  };

  const navigateToLeaderboard = () => {
    navigateTo("/leaderboard");
  };

  const navigateToSettings = () => {
    navigateTo("/settings");
  };

  // Fetch the user's avatar image on component mount
  useEffect(() => {
    const serializedUser = localStorage.getItem("user");
    const user = JSON.parse(serializedUser);
    const avatarUrl = user.image_url;
    fetch(avatarUrl) // Replace with your Flask endpoint URL
      .then((response) => response.blob())
      .then((blob) => {
        const objectUrl = URL.createObjectURL(blob);
        setImageSrc(objectUrl);
      });
  }, []);

  // Render the header with the logo, leaderboard button, and user menu
  return (
    <Box w="100%" h="4rem" p="1rem">
      <Flex>
        <Link onClick={navigateToHome} _hover={{ textDecoration: "none" }}>
          <Image
            boxSize="3rem"
            ml="1rem"
            className="rounded-full"
            src="/JCA616_Aya_logo_blue_AYA_logo.png"
            alt="The Aya Project"
          />
        </Link>
        <Spacer />
        <Button
          id="leaderboardButton"
          as="a"
          onClick={() => {
            trackButtonClickGA("leaderboard-button");
            navigateToLeaderboard();
          }}
          fontWeight="bold"
          borderRadius="5px"
          border="none"
          variant="outline"
          leftIcon={<MdLeaderboard />}
          className="text-slate-700"
        >
          Leaderboard
        </Button>
        <Menu>
          <MenuButton ml="2rem" mr="1rem" size="md">
            <Avatar
              src={imageSrc}
              size="xs"
              cursor="pointer"
              borderRadius="50%"
              padding={1}
              borderWidth={3}
              borderColor="#4368e0"
              style={{ width: "3rem", height: "3rem" }}
            />
          </MenuButton>
          <MenuList
            borderRadius="5px"
            color="gray.800"
            boxShadow="0px 8px 16px 0px rgba(0,0,0,0.2)"
          >
            <MenuItem
              p="1rem"
              minW="10rem"
              _hover={{ bgColor: "#60A5FA", color: "white" }}
              onClick={() => {
                trackButtonClickGA("my-contributions-button");
                navigateTo("/workspace");
              }}
            >
              Workspace
            </MenuItem>
            <MenuItem
              p="1rem"
              minW="10rem"
              _hover={{ bgColor: "#60A5FA", color: "white" }}
              onClick={() => {
                trackButtonClickGA("my-contributions-button");
                navigateTo("/contributions");
              }}
            >
              My Contributions
            </MenuItem>
            <MenuItem
              p="1rem"
              minW="10rem"
              _hover={{ bgColor: "#60A5FA", color: "white" }}
              onClick={() => {
                trackButtonClickGA("settings-button");
                navigateToSettings();
              }}
            >
              Settings
            </MenuItem>
            <MenuItem
              p="1rem"
              minW="10rem"
              _hover={{ bgColor: "#60A5FA", color: "white" }}
              onClick={() => {
                trackButtonClickGA("sign-out-button");
                handleLogout();
              }}
            >
              Logout
            </MenuItem>
          </MenuList>
        </Menu>
      </Flex>
    </Box>
  );
};

export default Navbar;
