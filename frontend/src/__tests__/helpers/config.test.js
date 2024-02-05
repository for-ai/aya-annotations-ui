import axios from "axios";

import { getApiUrl } from "../../helpers/config.jsx";

jest.mock("axios");

describe("getApiUrl", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should return the production backend URL when the environment is production", async () => {
    const backendUrl = "https://yourproductionurl.com";
    axios.get.mockResolvedValue({ data: { backendUrl } });

    const apiUrl = await getApiUrl();

    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith("/backend-url");
    expect(apiUrl).toEqual(`${backendUrl}/api/v1`);
  });

  it("should log an error if retrieving the backend URL fails", async () => {
    process.env.ENVIRONMENT = "production";
    const consoleErrorSpy = jest
      .spyOn(console, "error")
      .mockImplementation(() => {});
    axios.get.mockRejectedValue(new Error("Error fetching backend URL"));

    await getApiUrl();

    expect(axios.get).toHaveBeenCalledTimes(1);
    expect(axios.get).toHaveBeenCalledWith("/backend-url");
    expect(consoleErrorSpy).toHaveBeenCalledTimes(1);
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      new Error("Error fetching backend URL")
    );

    consoleErrorSpy.mockRestore();
  });
});
