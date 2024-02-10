import axios from "axios";

import {
  fetchAndCacheCountries,
  getCachedCountryOptions,
  getCountryOptions,
} from "../../helpers/country.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

jest.mock("axios");

describe("fetchAndCacheCountries function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should fetch and cache countries data", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Country 1" },
        { id: 2, name: "Country 2" },
      ],
    };

    axios.get.mockResolvedValueOnce(process.env.BACKEND_URL);
    axios.get.mockResolvedValueOnce({ data: responseData });

    await fetchAndCacheCountries();

    const cachedData = localStorage.getItem("countryOptions");
    expect(cachedData).toBeTruthy();

    const { data, timestamp } = JSON.parse(cachedData);
    expect(data).toEqual(responseData.options);
    expect(typeof timestamp).toBe("number");
  });

  it("should return an empty array if an error occurs", async () => {
    axios.get.mockRejectedValueOnce(new Error("Error"));

    const result = await fetchAndCacheCountries();

    expect(result).toEqual([]);
  });
});

describe("getCachedCountryOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return null if no data is cached", () => {
    const result = getCachedCountryOptions();
    expect(result).toBeNull();
  });

  it("should return null if cached data has expired", () => {
    const timestamp = Date.now() - cacheExpirationTime - 1;
    const cachedData = JSON.stringify({ data: [], timestamp });
    localStorage.setItem("countryOptions", cachedData);

    const result = getCachedCountryOptions();
    expect(result).toBeNull();
  });

  it("should return cached data if it has not expired", () => {
    const timestamp = Date.now();
    const responseData = {
      options: [
        { id: 1, name: "Country 1" },
        { id: 2, name: "Country 2" },
      ],
    };
    const cachedData = JSON.stringify({
      data: responseData.options,
      timestamp,
    });
    localStorage.setItem("countryOptions", cachedData);

    const result = getCachedCountryOptions();
    expect(result).toEqual(responseData.options);
  });
});

describe("getCountryOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return cached data if it exists", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Country 1" },
        { id: 2, name: "Country 2" },
      ],
    };
    const cachedData = JSON.stringify({
      data: responseData.options,
      timestamp: Date.now(),
    });
    localStorage.setItem("countryOptions", cachedData);

    const result = await getCountryOptions();
    expect(result).toEqual(responseData.options);
  });

  it("should fetch and cache data if it does not exist", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Country 1" },
        { id: 2, name: "Country 2" },
      ],
    };

    axios.get.mockResolvedValueOnce(process.env.BACKEND_URL);
    axios.get.mockResolvedValueOnce({ data: responseData });

    const result = await getCountryOptions();

    expect(result).toEqual(responseData.options);

    const cachedData = localStorage.getItem("countryOptions");
    expect(cachedData).toBeTruthy();

    const { data, timestamp } = JSON.parse(cachedData);
    expect(data).toEqual(responseData.options);
    expect(typeof timestamp).toBe("number");
  });

  it("should return an empty array if an error occurs", async () => {
    axios.get.mockRejectedValueOnce(new Error("Error"));
    const result = await getCountryOptions();

    expect(result).toEqual([]);
  });
});
