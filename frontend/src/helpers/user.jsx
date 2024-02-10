import axios from "axios";

import { getApiUrl } from "./config.jsx";
import { setAnalyticsUserId } from "./ga.jsx";
import { getLanguagesByUUIDs } from "./language.jsx";

export const updateUserProfile = async (
  selectedCountry,
  selectedLanguages,
  selectedGender,
  selectedAgeBucket,
  dialects
) => {
  try {
    const countryUuid = selectedCountry
      ? selectedCountry.id || selectedCountry.value
      : null;
    const languageUuids = selectedLanguages.map(
      (language) => language.id || language.value
    );
    const gender = selectedGender
      ? selectedGender.id || selectedGender.value
      : null;
    const ageBucket = selectedAgeBucket
      ? selectedAgeBucket.id || selectedAgeBucket.value
      : null;
    const apiUrl = await getApiUrl();
    const serializedUser = localStorage.getItem("user");
    const user = JSON.parse(serializedUser);

    const user_request = {
      username: user.username,
      image_url: user.image_url,
      country_code: countryUuid,
      language_codes: languageUuids,
      age_range: ageBucket,
      gender: gender,
      dialects: dialects,
    };

    await axios
      .patch(`${apiUrl}/users/${user.id}`, user_request)
      .then((response) => {
        const user = response.data;
        const serializedUser = JSON.stringify(user);
        console.log("serializedUser", serializedUser);
        localStorage.setItem("user", serializedUser);
      });
  } catch (error) {
    console.error(error);
  }
};

export const getUser = () => {
  try {
    const serializedUser = localStorage.getItem("user");
    const user = JSON.parse(serializedUser);

    // Set the analytics user ID
    setAnalyticsUserId(user.username);

    return user;
  } catch (error) {
    console.error(error);
  }
};

export const getUserLanguages = async () => {
  try {
    const serializedUser = localStorage.getItem("user");
    const user = JSON.parse(serializedUser);
    return getLanguagesByUUIDs(user.language_codes);
  } catch (error) {
    console.error(error);
  }
};

export const getContributions = async (
  userId,
  taskType,
  pageNumber = 1,
  pageSize = 20
) => {
  try {
    const apiUrl = await getApiUrl();
    const response = await axios.get(
      `${apiUrl}/users/contributions/${userId}/${taskType}?page_number=${pageNumber}&page_size=${pageSize}`
    );
    return response.data;
  } catch (error) {
    console.error(error);
  }
};
