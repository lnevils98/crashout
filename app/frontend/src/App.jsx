import React, { useState } from "react";
import CompanySelector from "./components/CompanySelector";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

const BACKEND_URL = (import.meta.env.VITE_BACKEND_URL) ? import.meta.env.VITE_BACKEND_URL : 'http://localhost:5000';

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
      const resp = await fetch(`${BACKEND_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, company })
      });
      const data = await resp.json();
      const joel = { sender: "Joel", text: data.answer, sources: data.sources };
      setMessages((m) => [...m, Joel]);
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
