import axios from "axios";

import { getApiUrl } from "./config.jsx";

export const getDailyLeaderboard = async (userID, day) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/leaderboards/daily/${userID}/${day}`,
      {
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getWeeklyLeaderboard = async (userID, week_of) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/leaderboards/weekly/${userID}/${week_of}`,
      {
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getLanguageLeaderboard = async (userID, language) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/leaderboards/language/${userID}/${language}`,
      {
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};

export const getOverallLeaderboard = async (userID, offset, recordsPerPage) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/leaderboards/${userID}/overall?offset=${offset}&limit=${recordsPerPage}`,
      {
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error) {
    console.error(error);
    throw error;
  }
};
