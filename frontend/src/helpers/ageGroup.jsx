const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

export const fetchAndCacheAgeGroupOptions = () => {
  try {
    const options = [
      { id: [0, 17], name: "Under 17 years old", code: "0-17" },
      { id: [18, 24], name: "18-24 years old", code: "18-24" },
      { id: [25, 34], name: "25-34 years old", code: "25-34" },
      { id: [35, 44], name: "35-44 years old", code: "35-44" },
      { id: [45, 54], name: "45-54 years old", code: "45-54" },
      { id: [55, 64], name: "55-64 years old", code: "55-64" },
      { id: [65, 74], name: "65-74 years old", code: "65-74" },
      { id: [75, 120], name: "75 years or older", code: "75-120" },
    ];

    const timestamp = Date.now();
    localStorage.setItem(
      "ageGroupOptions",
      JSON.stringify({ options, timestamp })
    );
    return options;
  } catch (error) {
    console.error(error);
    return [];
  }
};

export const getCachedAgeGroupOptions = () => {
  const cachedData = localStorage.getItem("ageGroupOptions");
  if (!cachedData) return null;

  const { options, timestamp } = JSON.parse(cachedData);
  const currentTime = Date.now();
  return currentTime - timestamp < cacheExpirationTime ? options : null;
};

export const getAgeGroupOptions = () => {
  const cachedData = getCachedAgeGroupOptions();
  if (cachedData) {
    return cachedData;
  } else {
    return fetchAndCacheAgeGroupOptions();
  }
};
