import axios from "axios";

import { getApiUrl } from "./config.jsx";

// Handle login by fetching the Discord OAuth login URL and redirecting the user
export const handleLogin = async (idp) => {
  try {
    const apiUrl = await getApiUrl();
    await axios.get(`${apiUrl}/auth/${idp}/login`).then((response) => {
      const data = response.data;
      window.location.href = data.url;
    });
  } catch (error) {
    console.error(error);
  }
};

export const handleLoginCallback = async (params) => {
  try {
    let authProvider = params.get("auth_provider");
    let jwtAccessToken = params.get("access_token");
    let jwtRefreshToken = params.get("refresh_token");
    let userId = params.get("user_id");
    let isCompleteProfile = params.get("is_complete_profile") === "True";

    // Save token data to local storage
    localStorage.setItem("auth_provider", authProvider);
    localStorage.setItem("access_token", jwtAccessToken);
    localStorage.setItem("refresh_token", jwtRefreshToken);

    let user_id = userId;
    const apiUrl = await getApiUrl();
    const response = await axios.get(`${apiUrl}/users/${user_id}`);

    // Check if the response contains user data
    if (response.data) {
      localStorage.setItem("user", JSON.stringify(response.data));
    }

    return isCompleteProfile;
  } catch (error) {
    console.error(error);
  }
};

// Handle the user's logout action
export const handleLogout = async () => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(`${apiUrl}/auth/logout`);

    if (response.status === 200) {
      // Clear cached user data
      localStorage.removeItem("auth_provider");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");

      // Redirect to the frontend home page
      window.location.href = response.data.redirect_url;
    }
  } catch (error) {
    console.error(error);
  }
};

// Check if authenticated
export const isAuthenticated = async () => {
  try {
    let authProvider = localStorage.getItem("auth_provider");

    // Check if the auth_provider is set
    if (authProvider === null) {
      return false;
    }

    const apiUrl = await getApiUrl();
    const response = await axios.get(`${apiUrl}/auth/authenticated`, {
      headers: {
        Authorization:
          localStorage.getItem("access_token") != null
            ? `Bearer ${localStorage.getItem("access_token")}`
            : null,
      },
      params: {
        auth_provider: authProvider,
      },
    });

    return response.data.is_authenticated;
  } catch (error) {
    console.error(error);
  }
};
