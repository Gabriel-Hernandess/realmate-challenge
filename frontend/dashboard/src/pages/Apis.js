import React from "react";
import "../styles/Apis.css";

export default function APIsPage() {
  const routes = [
    { path: "/auth/login/", method: "POST", description: "Login user" },
    { path: "/auth/refresh/", method: "POST", description: "Refresh token" },
    { path: "/auth/logout/", method: "POST", description: "Logout user" },
    { path: "/conversations/", method: "GET", description: "List all conversations" },
    { path: "/conversations/<uuid:pk>/", method: "GET", description: "Get a single conversation by UUID" },
    { path: "/conversations/<uuid:pk>/summaries/", method: "GET", description: "Get summaries from a single conversation" },
    { path: "/webhook/", method: "POST", description: "Webhook endpoint" },
  ];

  return (
    <div className="apis-page">
      <h2>API Routes</h2>
      <ul>
        {routes.map((r) => (
          <li key={r.path}>
            <strong>{r.method}</strong> {r.path} - {r.description}
          </li>
        ))}
      </ul>
    </div>
  );
}