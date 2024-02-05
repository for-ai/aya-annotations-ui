import axios from "axios";

export const getApiUrl = async () => {
  try {
    // Retrieve the backend URL from the server
    const backendUrlResponse = await axios.get("/backend-url");
    const backendUrl = backendUrlResponse.data.backendUrl + "/api/v1";
    return backendUrl;
  } catch (error) {
    console.error(error);
  }
};
