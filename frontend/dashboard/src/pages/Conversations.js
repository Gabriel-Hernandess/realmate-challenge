import React, { useEffect, useState } from "react";
import Modal from "../components/Modal";
import "../styles/Conversations.css";

export default function Conversations() {
  const [conversations, setConversations] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost/conversations/", { credentials: "include" })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) setConversations(data.conversations);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="conversations-page">
      <h2>Conversations</h2>
      <ul className="conversation-list">
        {conversations.map((c) => (
          <li key={c.id} onClick={() => setSelected(c)}>
            {c.id} - {c.messages.length} messages
          </li>
        ))}
      </ul>

      <Modal isOpen={!!selected} onClose={() => setSelected(null)}>
        {selected && (
          <div className="messages">
            {selected.messages.map((m, idx) => (
              <div
                key={idx}
                className={`message-bubble ${m.direction === "RECEIVED" ? "received" : "sent"}`}
              >
                <div className="message-content">{m.content}</div>
                <div className="message-date">{new Date(m.created_at).toLocaleString()}</div>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  );
}