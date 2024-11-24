import axios from "axios"

axios.defaults.baseURL = "/api";

async function tryToLog(username: string, password: string): Promise<void> {
  const response = await axios.post(
    "/token",
    new URLSearchParams({ username, password }), // Data
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" } // Headers
    }
  );
  const data = await response.data;
  localStorage.setItem("token", data.access_token);
};

export default tryToLog
