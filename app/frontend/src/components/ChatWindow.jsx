import React from "react";

export default function ChatWindow({ messages, loading, company }) {
  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-title">JOEL</div>
        <div className="chat-context ui-meta">
         Using <span>{company}</span> documentation
        </div>
         </div>

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.sender}`}>
            <div className="msg-text">{m.text}</div>

            {m.sources && (
              <div className="sources">
                <ul>
                  {m.sources.map((s, j) => (
                    <li key={j}>{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}

        {loading && <div className="typing">Joel is typing…</div>}
      </div>
    </div>
  );
}


