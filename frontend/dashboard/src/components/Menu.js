import React from "react";
import "../styles/Menu.css";

export default function Menu({ onSelect, onLogout }) {
  return (
    <div className="menu-lateral">
      <h2>Dashboard</h2>
      <ul>
        <li onClick={() => onSelect("conversations")}>Conversations</li>
        <li onClick={() => onSelect("apis")}>APIs</li>
        <li onClick={onLogout}>Logout</li>
      </ul>
    </div>
  );
}
