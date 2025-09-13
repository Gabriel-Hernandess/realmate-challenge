import React, { useState } from "react";
import MenuLateral from "./components/Menu";
import Conversations from "./pages/Conversations";
import Apis from "./pages/Apis";
import Login from "./pages/Login";

export default function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [page, setPage] = useState("conversations");

  if (!authenticated) return <Login onLogin={() => setAuthenticated(true)} />;

  const handleLogout = () => {
    if (window.confirm("Do you really want to logout?")) {
      fetch("http://localhost/auth/logout/", { method: "POST", credentials: "include" });
      setAuthenticated(false);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <MenuLateral onSelect={setPage} onLogout={handleLogout} />
      <div style={{ flex: 1, overflow: "auto" }}>
        {page === "conversations" && <Conversations />}
        {page === "apis" && <Apis />}
      </div>
    </div>
  );
}