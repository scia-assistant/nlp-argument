import axios from "axios"

axios.defaults.baseURL = "/api";

interface ApiResponse {
  response: string;
}

async function postRequest(question: string): Promise<string> {
  try {
    const apiResp = await axios.post<ApiResponse>('/question', { question: question });
    return apiResp.data.response;
  } catch (error) {
    return "error, I can't ask the question to the llm."
  }
}

export default postRequest
