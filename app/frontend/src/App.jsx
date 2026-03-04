import React, { useState } from "react";
import CompanySelector from "./components/CompanySelector";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

/* const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL) ? import.meta.env.VITE_BACKEND_URL : 'http://localhost:5000'; */
const BACKEND_URL = 'http://localhost:8000'; /*try to change to container name */

export default function App() {
  const [company, setCompany] = useState("Trek");
  const [messages, setMessages] = useState([
    { sender: "Joel", text: "Hi — I'm Joel. Ask me about bike maintenance or manuals." }
  ]);
  const [loading, setLoading] = useState(false);
  const sendMessage = async (text) => {
    if (!text) return;
    const userMsg = { sender: "user", text };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);

    try {
      const resp = await fetch(`http://localhost:8000/query`, { /* use const */
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({'role': 'user', 'content': text, 'company': company})
      });
      const data = await resp.json();
      const joel = { sender: "Joel", text: data.content };
      setMessages((m) => [...m, joel]);
    } catch (e) {
      setMessages((m) => [...m, { sender: "Joel", text: "Sorry, Liam hasn't done his part yet." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="logo">
  <h1 className="logo-title">
    CRASH<span>OUT</span>
  </h1>

  <div className="logo-divider" />

  <h2 className="crashout-subheader">
    with <span>Joel</span>, your personal bike mechanic.
  </h2>
</header>

      <CompanySelector company={company} setCompany={setCompany} />
      <ChatWindow messages={messages} loading={loading} company={company} />
      <ChatInput onSend={sendMessage} />
    </div>
  );
}
