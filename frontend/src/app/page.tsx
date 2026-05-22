"use client";

import { useState } from "react";

export default function Home() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [resumeAnalysis, setResumeAnalysis] = useState("");

  // Chat Function
  const sendMessage = async () => {

    if (!message) return;

    setLoading(true);

    const res = await fetch(
      `http://127.0.0.1:8000/chat?message=${message}`
    );

    const data = await res.json();

    setResponse(data.response);

    setLoading(false);
  };

  // Resume Upload Function
  const uploadResume = async () => {

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    setLoading(true);

    const res = await fetch(
      "http://127.0.0.1:8000/upload-resume",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();

    setResumeAnalysis(data.analysis);

    setLoading(false);
  };

  return (

    <div className="bg-gray-100 min-h-screen flex items-center justify-center p-6">

      <div className="bg-white shadow-2xl rounded-2xl w-[900px] min-h-[700px] p-6">

        <h1 className="text-4xl font-bold text-center mb-8 text-blue-600">
          AI Career Copilot
        </h1>

        {/* Resume Upload Section */}
        <div className="border rounded-2xl p-6 mb-8 bg-gray-50">

          <h2 className="text-2xl font-semibold mb-4">
            Upload Resume
          </h2>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              if (e.target.files) {
                setFile(e.target.files[0]);
              }
            }}
            className="mb-4"
          />

          <button
            onClick={uploadResume}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl"
          >
            Analyze Resume
          </button>

        </div>

        {/* Resume Analysis */}
        {resumeAnalysis && (
          <div className="border rounded-2xl p-6 mb-8 bg-white shadow">

            <h2 className="text-2xl font-semibold mb-4 text-green-700">
              Resume Analysis
            </h2>

            <div className="whitespace-pre-wrap">
              {resumeAnalysis}
            </div>

          </div>
        )}

        {/* Chat Section */}
        <div className="border rounded-2xl p-6 bg-gray-50">

          <h2 className="text-2xl font-semibold mb-4">
            AI Career Chat
          </h2>

          <div className="border rounded-xl p-4 h-[300px] overflow-y-auto bg-white">

            {message && (
              <div className="flex justify-end mb-4">
                <div className="bg-blue-500 text-white px-4 py-3 rounded-2xl max-w-[80%]">
                  {message}
                </div>
              </div>
            )}

            {response && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-200 text-black px-4 py-3 rounded-2xl max-w-[80%] whitespace-pre-wrap">
                  {response}
                </div>
              </div>
            )}

            {loading && (
              <div className="text-gray-500">
                AI is thinking...
              </div>
            )}

          </div>

          <div className="flex gap-3 mt-4">

            <input
              type="text"
              placeholder="Ask AI career questions..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="flex-1 border rounded-xl p-4 outline-none"
            />

            <button
              onClick={sendMessage}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-xl"
            >
              Send
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}