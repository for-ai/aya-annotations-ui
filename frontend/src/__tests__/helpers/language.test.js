import axios from "axios";

import {
  fetchAndCacheLanguages,
  getCachedLanguageOptions,
  getLanguageOptions,
  getLanguagesByUUIDs,
} from "../../helpers/language.jsx";

const cacheExpirationTime = 12 * 60 * 60 * 1000; // 12 hours in milliseconds

jest.mock("axios");

describe("fetchAndCacheLanguages function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should fetch and cache languages data", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Language 1" },
        { id: 2, name: "Language 2" },
      ],
    };

    axios.get.mockResolvedValueOnce(process.env.BACKEND_URL);
    axios.get.mockResolvedValueOnce({ data: responseData });

    await fetchAndCacheLanguages();

    const cachedData = localStorage.getItem("languageOptions");
    expect(cachedData).toBeTruthy();

    const { data, timestamp } = JSON.parse(cachedData);
    expect(data).toEqual(responseData.options);
    expect(typeof timestamp).toBe("number");
  });

  it("should return an empty array if an error occurs", async () => {
    axios.get.mockRejectedValueOnce(new Error("Error"));

    const result = await fetchAndCacheLanguages();

    expect(result).toEqual([]);
  });
});

describe("getCachedLanguageOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return null if no data is cached", () => {
    const result = getCachedLanguageOptions();
    expect(result).toBeNull();
  });

  it("should return null if cached data has expired", () => {
    const timestamp = Date.now() - cacheExpirationTime - 1;
    const cachedData = JSON.stringify({ data: [], timestamp });
    localStorage.setItem("languageOptions", cachedData);

    const result = getCachedLanguageOptions();
    expect(result).toBeNull();
  });

  it("should return cached data if it has not expired", () => {
    const timestamp = Date.now();
    const responseData = {
      options: [
        { id: 1, name: "Language 1" },
        { id: 2, name: "Language 2" },
      ],
    };
    const cachedData = JSON.stringify({
      data: responseData.options,
      timestamp,
    });
    localStorage.setItem("languageOptions", cachedData);

    const result = getCachedLanguageOptions();
    expect(result).toEqual(responseData.options);
  });
});

describe("getLanguageOptions function", () => {
  afterEach(() => {
    localStorage.clear();
  });

  it("should return cached data if it exists", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Language 1" },
        { id: 2, name: "Language 2" },
      ],
    };
    const cachedData = JSON.stringify({
      data: responseData.options,
      timestamp: Date.now(),
    });
    localStorage.setItem("languageOptions", cachedData);

    const result = await getLanguageOptions();
    expect(result).toEqual(responseData.options);
  });

  it("should fetch and cache data if it does not exist", async () => {
    const responseData = {
      options: [
        { id: 1, name: "Language 1" },
        { id: 2, name: "Language 2" },
      ],
    };

    axios.get.mockResolvedValueOnce(process.env.BACKEND_URL);
    axios.get.mockResolvedValueOnce({ data: responseData });

    const result = await getLanguageOptions();

    expect(result).toEqual(responseData.options);

    const cachedData = localStorage.getItem("languageOptions");
    expect(cachedData).toBeTruthy();

    const { data, timestamp } = JSON.parse(cachedData);
    expect(data).toEqual(responseData.options);
    expect(typeof timestamp).toBe("number");
  });

  it("should return an empty array if an error occurs", async () => {
    axios.get.mockRejectedValueOnce(new Error("Error"));
    const result = await getLanguageOptions();

    expect(result).toEqual([]);
  });
});

describe("getLanguagesByUUIDs function", () => {
  it("should return an empty array if no language UUIDs are provided", async () => {
    const result = await getLanguagesByUUIDs([]);
    expect(result).toEqual([]);
  });

  it("should return an empty array if an error occurs", async () => {
    const languageUUIDs = [1, 2];

    jest.spyOn(console, "error");

    axios.get.mockRejectedValueOnce(new Error("Error"));

    const result = await getLanguagesByUUIDs(languageUUIDs);

    expect(result).toEqual([]);
    expect(console.error).toHaveBeenCalled();
  });

  it("should return the languages in the requested order", async () => {
    const allLanguages = [
      { id: 1, name: "Language 1" },
      { id: 2, name: "Language 2" },
      { id: 3, name: "Language 3" },
    ];
    const languageUUIDs = [3, 2, 1];

    jest.spyOn(console, "error");

    axios.get.mockResolvedValueOnce(process.env.BACKEND_URL);
    axios.get.mockResolvedValueOnce({ data: { options: allLanguages } });

    const result = await getLanguagesByUUIDs(languageUUIDs);

    expect(result).toEqual([
      { id: 3, name: "Language 3" },
      { id: 2, name: "Language 2" },
      { id: 1, name: "Language 1" },
    ]);
  });
});
