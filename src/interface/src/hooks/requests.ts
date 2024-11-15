import axios from "axios"

axios.defaults.baseURL = process.env.REACT_APP_MY_API_URI;

interface ApiResponse {
  response: string;
}

async function postRequest(question: string): Promise<string> {
  try {
    console.log(`the process.env.MY_API_URI = ${process.env.MY_API_URI}.`)
    const apiResp = await axios.post<ApiResponse>('/question', { question: question });
    return apiResp.data.response;
  } catch (error) {
    return "error, I can't ask the question to the llm."
  }
}

export default postRequest
