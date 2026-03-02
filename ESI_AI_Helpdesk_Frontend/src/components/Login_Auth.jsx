// src/Login_Auth.jsx

import { login as loginApi } from "../backend_connection/auth";
import { useAuth } from "../context/AuthContext";
import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const LoginAuth = () => {
  const navigate  = useNavigate();
  const location  = useLocation();
  const { login } = useAuth();

  const searchParams = new URLSearchParams(location.search);
  const operations   = searchParams.get("operations");
  console.log("Operations from URL:", operations);

  const [formData, setFormData]   = useState({ username: "", password: "" });
  const [emailFocus, setEmailFocus]   = useState(false);
  const [passFocus,  setPassFocus]    = useState(false);
  const [hovering,   setHovering]     = useState(false);
  const [loading,    setLoading]      = useState(false);

  const YELLOW = "#FFD600";
  const BG     = "#1c1c1c";
  const CARD   = "#2a2a2a";
  const INPUT  = "#1e1e1e";

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await loginApi(formData.username, formData.password);
    setLoading(false);

    if (result.success) {
      login(result.user);
      const role = result.user.role;
      console.log("User role from backend:", role);
      if      (role === "admin")            navigate("/admin");
      else if (role === "support_engineer") navigate("/analyst");
      else if (role === "instructor")       navigate("/manager");
      else                                  navigate("/operator");
    } else {
      alert(result.error);
    }
  };

  // ── Styles ────────────────────────────────────────────────────────────────
  const styles = {
    page: {
      minHeight: "100vh",
      width: "100%",
      background: `radial-gradient(ellipse at 50% 40%, #2a2200 0%, ${BG} 70%)`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Segoe UI', Arial, sans-serif",
      boxSizing: "border-box",
    },
    card: {
      background: CARD,
      border: `1px solid rgba(255,214,0,0.2)`,
      borderRadius: 20,
      padding: "48px 40px 40px",
      width: "100%",
      maxWidth: 420,
      boxShadow: "0 24px 64px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,214,0,0.08)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      boxSizing: "border-box",
    },
    avatarWrap: {
      width: 64,
      height: 64,
      borderRadius: "50%",
      background: `linear-gradient(135deg, ${YELLOW}, #FFA000)`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      marginBottom: 20,
      boxShadow: `0 4px 20px rgba(255,214,0,0.4)`,
    },
    title: {
      margin: "0 0 32px",
      fontSize: 26,
      fontWeight: 700,
      color: "#fff",
      letterSpacing: 0.5,
    },
    fieldWrap: {
      width: "100%",
      marginBottom: 20,
      position: "relative",
    },
    label: (focused) => ({
      display: "block",
      marginBottom: 8,
      fontSize: 12,
      fontWeight: 600,
      color: focused ? YELLOW : "#888",
      textTransform: "uppercase",
      letterSpacing: 1,
      transition: "color 0.2s",
    }),
    input: (focused) => ({
      width: "100%",
      padding: "14px 16px",
      background: INPUT,
      border: `1.5px solid ${focused ? YELLOW : "rgba(255,255,255,0.1)"}`,
      borderRadius: 10,
      color: "#fff",
      fontSize: 15,
      outline: "none",
      boxSizing: "border-box",
      transition: "border-color 0.2s, box-shadow 0.2s",
      boxShadow: focused ? `0 0 0 3px rgba(255,214,0,0.12)` : "none",
    }),
    button: {
      width: "100%",
      padding: "15px",
      marginTop: 12,
      background: hovering
        ? `linear-gradient(135deg, #FFE57F, ${YELLOW})`
        : `linear-gradient(135deg, ${YELLOW}, #FFA000)`,
      border: "none",
      borderRadius: 10,
      color: "#111",
      fontSize: 16,
      fontWeight: 800,
      letterSpacing: 1,
      cursor: loading ? "not-allowed" : "pointer",
      transition: "all 0.25s",
      boxShadow: hovering
        ? "0 8px 28px rgba(255,214,0,0.45)"
        : "0 4px 16px rgba(255,214,0,0.25)",
      transform: hovering ? "translateY(-2px)" : "translateY(0)",
      opacity: loading ? 0.7 : 1,
    },
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        {/* Avatar */}
        <div style={styles.avatarWrap}>
          <svg width="28" height="28" viewBox="0 0 24 24" fill="#111">
            <path d="M12 1C9.24 1 7 3.24 7 6v1H5a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2V6c0-2.76-2.24-5-5-5zm0 2c1.66 0 3 1.34 3 3v1H9V6c0-1.66 1.34-3 3-3zm0 9a2 2 0 1 1 0 4 2 2 0 0 1 0-4z"/>
          </svg>
        </div>

        {/* Title */}
        <h1 style={styles.title}>Sign In</h1>

        {/* Form */}
        <form onSubmit={handleSubmit} style={{ width: "100%" }}>

          {/* Email */}
          <div style={styles.fieldWrap}>
            <label style={styles.label(emailFocus)}>Email *</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              onFocus={() => setEmailFocus(true)}
              onBlur={() => setEmailFocus(false)}
              placeholder="you@example.com"
              autoFocus
              required
              style={styles.input(emailFocus)}
            />
          </div>

          {/* Password */}
          <div style={styles.fieldWrap}>
            <label style={styles.label(passFocus)}>Password *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onFocus={() => setPassFocus(true)}
              onBlur={() => setPassFocus(false)}
              placeholder="••••••••"
              required
              style={styles.input(passFocus)}
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            style={styles.button}
            onMouseEnter={() => setHovering(true)}
            onMouseLeave={() => setHovering(false)}
          >
            {loading ? "Signing in…" : "Login"}
          </button>

        </form>
      </div>
    </div>
  );
};

export default LoginAuth;