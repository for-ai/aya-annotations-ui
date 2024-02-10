import axios from "axios";

import { getApiUrl } from "./config.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

export const fetchAndCacheLanguages = async () => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(`${apiUrl}/users/options/languages`);

    const data = response.data.options;
    const timestamp = Date.now();
    localStorage.setItem(
      "languageOptions",
      JSON.stringify({ data, timestamp })
    );
    return data;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const getCachedLanguageOptions = () => {
  const cachedData = localStorage.getItem("languageOptions");
  if (!cachedData) return null;

  const { data, timestamp } = JSON.parse(cachedData);
  const currentTime = Date.now();
  return currentTime - timestamp < cacheExpirationTime ? data : null;
};

export const getLanguageOptions = async () => {
  const cachedData = getCachedLanguageOptions();
  if (cachedData) {
    return cachedData;
  } else {
    return await fetchAndCacheLanguages();
  }
};

export const getLanguagesByUUIDs = async (languageUUIDs) => {
  try {
    const allLanguages = await getLanguageOptions();
    const filteredLanguages = allLanguages.filter((language) =>
      languageUUIDs.includes(language.id)
    );

    // Sort the languages in the requested order
    const orderedLanguages = filteredLanguages.sort(
      (a, b) => languageUUIDs.indexOf(a.id) - languageUUIDs.indexOf(b.id)
    );

    return orderedLanguages;
  } catch (error) {
    console.error(error);
    return [];
  }
};
