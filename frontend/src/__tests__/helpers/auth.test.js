import axios from "axios";

import {
  handleLogin,
  handleLogout,
  isAuthenticated,
} from "../../helpers/auth.jsx";
import { getApiUrl } from "../../helpers/config.jsx";

jest.mock("axios");
jest.mock("../../helpers/config.jsx");

// Mock window.location
delete window.location;
window.location = { href: "" };

describe("auth functions", () => {
  beforeEach(() => {
    axios.get.mockClear();
    axios.post.mockClear();
    getApiUrl.mockClear();
    window.location.href = "";
  });

  test("handleLogin", async () => {
    const apiUrl = "http://test.api";
    const loginUrl = "http://test.login";
    getApiUrl.mockResolvedValue(apiUrl);
    axios.get.mockResolvedValue({ data: { url: loginUrl } });

    await handleLogin("google");

    expect(getApiUrl).toHaveBeenCalled();
    expect(axios.get).toHaveBeenCalledWith(`${apiUrl}/auth/google/login`);
    expect(window.location.href).toEqual(loginUrl);
  });

  test("handleLogin", async () => {
    const apiUrl = "http://test.api";
    const loginUrl = "http://test.login";
    getApiUrl.mockResolvedValue(apiUrl);
    axios.get.mockResolvedValue({ data: { url: loginUrl } });

    await handleLogin("discord");

    expect(getApiUrl).toHaveBeenCalled();
    expect(axios.get).toHaveBeenCalledWith(`${apiUrl}/auth/discord/login`);
    expect(window.location.href).toEqual(loginUrl);
  });

  test("handleLogout", async () => {
    const apiUrl = "http://test.api";
    const redirectUrl = "http://test.redirect";
    getApiUrl.mockResolvedValue(apiUrl);
    axios.get.mockResolvedValue({
      status: 200,
      data: { redirect_url: redirectUrl },
    });

    localStorage.setItem("user", "mockUser");

    await handleLogout();

    expect(getApiUrl).toHaveBeenCalled();
    expect(axios.get).toHaveBeenCalledWith(`${apiUrl}/auth/logout`);
    expect(localStorage.getItem("user")).toBeNull();
    expect(window.location.href).toEqual(redirectUrl);
  });

  test("isAuthenticated", async () => {
    const apiUrl = "http://test.api";
    const isAuthenticatedResult = true;
    getApiUrl.mockResolvedValue(apiUrl);
    axios.get.mockResolvedValue({
      data: {
        is_authenticated: isAuthenticatedResult,
      },
    });

    localStorage.setItem("auth_provider", "google");

    const result = await isAuthenticated();

    expect(getApiUrl).toHaveBeenCalled();
    expect(axios.get).toHaveBeenCalledWith(`${apiUrl}/auth/authenticated`, {
      headers: {
        Authorization: null,
      },
      params: {
        auth_provider: "google",
      },
    });
    expect(result).toEqual(isAuthenticatedResult);
  });
});
