import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Reports from "./pages/Reports";
import Students from "./pages/Students";
import Settings from "./pages/Settings";
import AuthGuard from "./components/AuthGuard";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<AuthGuard><Dashboard /></AuthGuard>} />
          <Route path="/reports" element={<AuthGuard><Reports /></AuthGuard>} />
          <Route path="/students" element={<AuthGuard><Students /></AuthGuard>} />
          <Route path="/settings" element={<AuthGuard><Settings /></AuthGuard>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
