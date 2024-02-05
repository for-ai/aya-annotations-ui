const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

export const fetchAndCacheGenderOptions = () => {
  try {
    const options = [
      { id: "male", name: "Male", code: "001" },
      { id: "female", name: "Female", code: "002" },
      { id: "non-binary", name: "Non-binary", code: "003" },
      { id: "prefer not to say", name: "Prefer not to say", code: "004" },
      { id: "other", name: "Other", code: "005" },
    ];

    const timestamp = Date.now();
    localStorage.setItem(
      "genderOptions",
      JSON.stringify({ options, timestamp })
    );
    return options;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const getCachedGenderOptions = () => {
  const cachedData = localStorage.getItem("genderOptions");
  if (!cachedData) return null;

  const { options, timestamp } = JSON.parse(cachedData);
  const currentTime = Date.now();
  return currentTime - timestamp < cacheExpirationTime ? options : null;
};

export const getGenderOptions = () => {
  const cachedData = getCachedGenderOptions();
  if (cachedData) {
    return cachedData;
  } else {
    return fetchAndCacheGenderOptions();
  }
};
