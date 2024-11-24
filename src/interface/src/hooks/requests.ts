import axios from "axios"

axios.defaults.baseURL = "/api";

interface ApiResponse {
  response: string;
}

async function postRequest(question: string): Promise<string> {
  const token = localStorage.getItem('token');
  console.log(token)

  if (!token) {
    throw new Error("Unauthorized: Token not found.");
  }

  const apiResp = await axios.post<ApiResponse>(
    'http://127.0.0.1:8086/question',
    { question: question },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
  console.log(apiResp)

  return apiResp.data.response;
}

export default postRequest
