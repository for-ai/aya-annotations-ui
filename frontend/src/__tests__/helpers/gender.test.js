import {
  fetchAndCacheGenderOptions,
  getCachedGenderOptions,
  getGenderOptions,
} from "../../helpers/gender.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

describe("fetchAndCacheGenderOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should cache gender options data", () => {
    const options = [
      { id: "male", name: "Male", code: "001" },
      { id: "female", name: "Female", code: "002" },
      { id: "non-binary", name: "Non-binary", code: "003" },
      { id: "prefer not to say", name: "Prefer not to say", code: "004" },
      { id: "other", name: "Other", code: "005" },
    ];

    fetchAndCacheGenderOptions();

    const cachedData = localStorage.getItem("genderOptions");
    expect(cachedData).toBeTruthy();

    const { options: cachedOptions, timestamp } = JSON.parse(cachedData);
    expect(cachedOptions).toEqual(options);
    expect(typeof timestamp).toBe("number");
  });
});

describe("getCachedGenderOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return null if no data is cached", () => {
    const result = getCachedGenderOptions();
    expect(result).toBeNull();
  });

  it("should return null if cached data has expired", () => {
    const timestamp = Date.now() - cacheExpirationTime - 1;
    const cachedData = JSON.stringify({ options: [], timestamp });
    localStorage.setItem("genderOptions", cachedData);

    const result = getCachedGenderOptions();
    expect(result).toBeNull();
  });

  it("should return cached data if it has not expired", () => {
    const timestamp = Date.now();
    const options = [
      { id: "male", name: "Male", code: "001" },
      { id: "female", name: "Female", code: "002" },
      { id: "non-binary", name: "Non-binary", code: "003" },
      { id: "prefer not to say", name: "Prefer not to say", code: "004" },
      { id: "other", name: "Other", code: "005" },
    ];

    const cachedData = JSON.stringify({ options, timestamp });
    localStorage.setItem("genderOptions", cachedData);

    const result = getCachedGenderOptions();
    expect(result).toEqual(options);
  });
});

describe("getGenderOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return cached data if it exists", () => {
    const options = [
      { id: "male", name: "Male", code: "001" },
      { id: "female", name: "Female", code: "002" },
      { id: "non-binary", name: "Non-binary", code: "003" },
      { id: "prefer not to say", name: "Prefer not to say", code: "004" },
      { id: "other", name: "Other", code: "005" },
    ];

    const cachedData = JSON.stringify({ options, timestamp: Date.now() });
    localStorage.setItem("genderOptions", cachedData);

    const result = getGenderOptions();
    expect(result).toEqual(options);
  });

  it("should fetch and cache data if it does not exist", () => {
    const options = [
      { id: "male", name: "Male", code: "001" },
      { id: "female", name: "Female", code: "002" },
      { id: "non-binary", name: "Non-binary", code: "003" },
      { id: "prefer not to say", name: "Prefer not to say", code: "004" },
      { id: "other", name: "Other", code: "005" },
    ];
    fetchAndCacheGenderOptions();

    const result = getGenderOptions();
    expect(result).toEqual(options);
  });
});
