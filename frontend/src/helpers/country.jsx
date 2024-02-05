import axios from "axios";

import { getApiUrl } from "./config.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

export const fetchAndCacheCountries = async () => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(`${apiUrl}/users/options/countries`);

    const data = response.data.options;
    const timestamp = Date.now();
    localStorage.setItem("countryOptions", JSON.stringify({ data, timestamp }));
    return data;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const getCachedCountryOptions = () => {
  const cachedData = localStorage.getItem("countryOptions");
  if (!cachedData) return null;

  const { data, timestamp } = JSON.parse(cachedData);
  const currentTime = Date.now();
  return currentTime - timestamp < cacheExpirationTime ? data : null;
};

export const getCountryOptions = async () => {
  const cachedData = getCachedCountryOptions();
  if (cachedData) {
    return cachedData;
  } else {
    return await fetchAndCacheCountries();
  }
};
