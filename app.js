import React, { useState, useEffect } from "react";

const API = "https://your-backend.onrender.com";


export default function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const fetchMessages = async () => {
    const res = await fetch(`${API}/messages`);
    const data = await res.json();
    setMessages(data);
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    await fetch(`${API}/send`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    setMessage("");
    fetchMessages();
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">
        🔐 Quantum Secure Messenger
      </h1>

      <form onSubmit={sendMessage} className="flex gap-2 mb-6">
        <input
          className="border p-2 rounded w-80"
          placeholder="Enter message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          required
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">
          Send
        </button>
      </form>

      <div className="bg-white shadow p-4 rounded w-full max-w-2xl">
        <h2 className="font-semibold mb-2">📦 Blockchain Messages</h2>

        {messages.length === 0 ? (
          <p>No messages yet</p>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className="border-b p-2">
              <p><strong>From:</strong> {msg.sender}</p>
              <p><strong>Message:</strong> {msg.message}</p>
              <p className="text-xs text-gray-500">
                {msg.timestamp}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
