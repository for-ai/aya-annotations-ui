import {
  fetchAndCacheAgeGroupOptions,
  getAgeGroupOptions,
  getCachedAgeGroupOptions,
} from "../../helpers/ageGroup.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

describe("fetchAndCacheAgeGroupOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should cache age group options data", () => {
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

    fetchAndCacheAgeGroupOptions();

    const cachedData = localStorage.getItem("ageGroupOptions");
    expect(cachedData).toBeTruthy();

    const { options: cachedOptions, timestamp } = JSON.parse(cachedData);
    expect(cachedOptions).toEqual(options);
    expect(typeof timestamp).toBe("number");
  });
});

describe("getCachedAgeGroupOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return null if no data is cached", () => {
    const result = getCachedAgeGroupOptions();
    expect(result).toBeNull();
  });

  it("should return null if cached data has expired", () => {
    const timestamp = Date.now() - cacheExpirationTime - 1;
    const cachedData = JSON.stringify({ options: [], timestamp });
    localStorage.setItem("ageGroupOptions", cachedData);

    const result = getCachedAgeGroupOptions();
    expect(result).toBeNull();
  });

  it("should return cached data if it has not expired", () => {
    const timestamp = Date.now();
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

    const cachedData = JSON.stringify({ options, timestamp });
    localStorage.setItem("ageGroupOptions", cachedData);

    const result = getCachedAgeGroupOptions();
    expect(result).toEqual(options);
  });
});

describe("getAgeGroupOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return cached data if it exists", () => {
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

    const cachedData = JSON.stringify({ options, timestamp: Date.now() });
    localStorage.setItem("ageGroupOptions", cachedData);

    const result = getAgeGroupOptions();
    expect(result).toEqual(options);
  });

  it("should fetch and cache data if it does not exist", () => {
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

    fetchAndCacheAgeGroupOptions();

    const result = getAgeGroupOptions();
    expect(result).toEqual(options);
  });
});
