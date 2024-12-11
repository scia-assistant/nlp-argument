import axios from "axios"

axios.defaults.baseURL = "/api";

async function tryToLog(username: string, password: string): Promise<number> {
  try {
    const response = await axios.post(
      "/token",
      new URLSearchParams({ username, password }), // Data
      {
        headers: { "Content-Type": "application/x-www-form-urlencoded" } // Headers
      }
    );
    const data = response.data;
    localStorage.setItem("token", data.access_token);
    return response.status;
  } catch (error: any) {
    return error.status;
  }
};

export default tryToLog
