import { useState } from "react";

const sandapayLightTheme = {
  background:
    "linear-gradient(135deg, #e3f0ff 0%, #b3c6e6 40%, #1857a3 80%, #bfa100 100%)", 
  color: "#1a2233",
  accent: "#1857a3",
  accentSecondary: "#2a3d66",
  cardBg: "rgba(255,255,255,0.65)",
  cardShadow: "0 8px 32px 0 rgba(26,87,163,0.10)",
  navBg: "rgba(245,247,250,0.92)",
  navBorder: "1px solid #1857a3",
  inputBg: "rgba(255, 255, 255, 0.35)",
  glassBlur: "blur(12px)",
  gold: "#bfa100",
};
const sandapayDarkTheme = {
  background: "linear-gradient(135deg, #181c2b 60%, #1e2746 100%)",
  color: "#f5f7fa",
  accent: "#3ed0fa",
  accentSecondary: "#6e8efb",
  cardBg: "rgba(30, 39, 70, 0.55)",
  cardShadow: "0 8px 32px 0 rgba(62,208,250,0.18)",
  navBg: "rgba(24,28,43,0.92)",
  navBorder: "1px solid #3ed0fa",
  inputBg: "rgba(30, 39, 70, 0.35)",
  glassBlur: "blur(12px)",
};

const profile = {
  name: "Arunima Paul",
  avatar: "data:image/png;base64,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",
  email: "arunima.paul@email.com",
  joined: "2013",
  balance: "₹12,500.00",
  transactions: 128,
  products: 4,
};

const fadeIn = {
  animation: "fadeIn 1s cubic-bezier(.4,0,.2,1) both",
};

const ProfilePage = () => {
  const [darkMode, setDarkMode] = useState(true);
  const theme = darkMode ? sandapayDarkTheme : sandapayLightTheme;

  const scrollToProfile = () => {
    const profileSection = document.querySelector('.profile-section');
    if (profileSection) {
      profileSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: theme.background,
        color: theme.color,
        fontFamily: "Inter, 'Segoe UI', Arial, sans-serif",
        transition:
          "background 0.6s cubic-bezier(.4,0,.2,1), color 0.6s cubic-bezier(.4,0,.2,1)",
        boxShadow: "0 0 80px 0 #3ed0fa22 inset",
      }}
    >
      <style>
        {`
        @keyframes fadeIn {
          0% { opacity: 0; transform: translateY(40px);}
          100% { opacity: 1; transform: translateY(0);}
        }
        .enlarge-on-hover {
          transition: transform 0.25s cubic-bezier(.4,0,.2,1), box-shadow 0.25s;
        }
        .enlarge-on-hover:hover, .enlarge-on-hover:focus {
          transform: scale(1.06);
          box-shadow: 0 8px 32px #3ed0fa44;
          z-index: 2;
        }
        .enlarge-btn:hover, .enlarge-btn:focus {
          transform: scale(1.08);
          box-shadow: 0 6px 24px #3ed0fa66, 0 0 12px #3ed0fa99;
          filter: brightness(1.1);
        }
        .enlarge-avatar:hover, .enlarge-avatar:focus {
          transform: scale(1.10);
          box-shadow: 0 8px 32px #3ed0fa99;
        }
        .glass {
          backdrop-filter: ${theme.glassBlur};
          -webkit-backdrop-filter: ${theme.glassBlur};
        }
        `}
      </style>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "2rem 4rem 1rem 4rem",
          background: theme.navBg,
          borderBottom: theme.navBorder,
          transition: "background 0.6s, border 0.6s",
          boxShadow: "0 2px 24px 0 #3ed0fa11",
          backdropFilter: theme.glassBlur,
          WebkitBackdropFilter: theme.glassBlur,
        }}
      >
        <div
          style={{
            fontWeight: "bold",
            fontSize: "1.5rem",
            letterSpacing: "2px",
            color: theme.accent,
          }}
        >
          AltScore
        </div>
        <nav style={{ display: "flex", gap: "2rem", alignItems: "center" }}>
          <a
            href="#"
            style={{ color: theme.color, textDecoration: "none", opacity: 0.8 }}
          >
            Dashboard
          </a>
          <a
            href="#"
            style={{ color: theme.color, textDecoration: "none", opacity: 0.8 }}
          >
            Cards
          </a>
          <a
            href="#"
            style={{ color: theme.color, textDecoration: "none", opacity: 0.8 }}
          >
            Transactions
          </a>
          <a
            href="#"
            style={{ color: theme.color, textDecoration: "none", opacity: 0.8 }}
          >
            Settings
          </a>
          <button
            onClick={() => setDarkMode((m) => !m)}
            style={{
              background: theme.accent,
              color: darkMode ? "#232323" : "#fff",
              border: "none",
              borderRadius: "50%",
              width: "2.5rem",
              height: "2.5rem",
              marginRight: "1rem",
              cursor: "pointer",
              fontWeight: "bold",
              fontSize: "1.2rem",
              boxShadow: theme.cardShadow,
              transition: "background 0.6s, color 0.6s",
            }}
            aria-label="Toggle dark mode"
            title="Toggle dark/light mode"
          >
            {darkMode ? "🌞" : "🌙"}
          </button>
          <img
            src={profile.avatar}
            alt="avatar"
            onClick={scrollToProfile}
            style={{
              width: "2.5rem",
              height: "2.5rem",
              borderRadius: "50%",
              border: `2px solid ${theme.accent}`,
              objectFit: "cover",
              boxShadow: theme.cardShadow,
              cursor: "pointer",
              transition: "transform 0.2s ease, box-shadow 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.transform = "scale(1.1)";
              e.target.style.boxShadow = "0 4px 16px rgba(62,208,250,0.3)";
            }}
            onMouseLeave={(e) => {
              e.target.style.transform = "scale(1)";
              e.target.style.boxShadow = theme.cardShadow;
            }}
          />
        </nav>
      </header>
      <main
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          padding: "4rem 0",
          minHeight: "calc(100vh - 100px)",
          width: "100%",
        }}
      >
        {/* Profile Card */}
        <section
          className="profile-section"
          style={{
            background: theme.cardBg,
            borderRadius: "2rem",
            boxShadow: theme.cardShadow,
            padding: "3rem 4rem",
            minWidth: "420px",
            maxWidth: "90vw",
            ...fadeIn,
            transition: "background 0.6s",
            marginBottom: "2.5rem",
            border: `1.5px solid ${theme.accentSecondary}`,
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "2rem",
              marginBottom: "2rem",
            }}
          >
            <img
              src={profile.avatar}
              alt="avatar"
              className="enlarge-avatar"
              style={{
                width: "6rem",
                height: "6rem",
                borderRadius: "50%",
                border: `4px solid ${theme.accent}`,
                objectFit: "cover",
                boxShadow: theme.cardShadow,
              }}
            />
            <div>
              <h1
                style={{
                  fontSize: "2.2rem",
                  fontWeight: 700,
                  margin: 0,
                  color: theme.color,
                }}
              >
                {profile.name}
              </h1>
              <div
                style={{
                  color: theme.accent,
                  fontWeight: 500,
                  marginTop: "0.3rem",
                }}
              >
                {profile.email}
              </div>
              <div
                style={{
                  color: darkMode ? "#bbb" : "#888",
                  fontSize: "1rem",
                  marginTop: "0.5rem",
                }}
              >
                Member since {profile.joined}
              </div>
            </div>
          </div>
          <div
            style={{
              display: "flex",
              gap: "2rem",
              marginBottom: "2.5rem",
              flexWrap: "wrap",
            }}
          >
            <div
              className="enlarge-on-hover"
              style={{
                background: darkMode ? "#181818" : "#fffbe6",
                borderRadius: "1.2rem",
                padding: "1.5rem 2rem",
                minWidth: "140px",
                boxShadow: theme.cardShadow,
                textAlign: "center",
                flex: 1,
                transition: "background 0.6s",
              }}
            >
              <div
                style={{
                  fontSize: "1.1rem",
                  color: theme.accent,
                  fontWeight: 600,
                }}
              >
                Balance
              </div>
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  marginTop: "0.5rem",
                  color: theme.color,
                }}
              >
                {profile.balance}
              </div>
            </div>
            <div
              className="enlarge-on-hover"
              style={{
                background: darkMode ? "#181818" : "#fffbe6",
                borderRadius: "1.2rem",
                padding: "1.5rem 2rem",
                minWidth: "140px",
                boxShadow: theme.cardShadow,
                textAlign: "center",
                flex: 1,
                transition: "background 0.6s",
              }}
            >
              <div
                style={{
                  fontSize: "1.1rem",
                  color: theme.accent,
                  fontWeight: 600,
                }}
              >
                Transactions
              </div>
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  marginTop: "0.5rem",
                  color: theme.color,
                }}
              >
                {profile.transactions}
              </div>
            </div>
            <div
              className="enlarge-on-hover"
              style={{
                background: darkMode ? "#181818" : "#fffbe6",
                borderRadius: "1.2rem",
                padding: "1.5rem 2rem",
                minWidth: "140px",
                boxShadow: theme.cardShadow,
                textAlign: "center",
                flex: 1,
                transition: "background 0.6s",
              }}
            >
              <div
                style={{
                  fontSize: "1.1rem",
                  color: theme.accent,
                  fontWeight: 600,
                }}
              >
                Products
              </div>
              <div
                style={{
                  fontSize: "2rem",
                  fontWeight: 700,
                  marginTop: "0.5rem",
                  color: theme.color,
                }}
              >
                {profile.products}
              </div>
            </div>
          </div>
          <div
            style={{ display: "flex", gap: "1.5rem", marginBottom: "1.5rem" }}
          >
            <button
              className="enlarge-btn"
              style={{
                background: theme.accent,
                color: darkMode ? "#232323" : "#fff",
                border: "none",
                borderRadius: "1.5rem",
                padding: "0.8rem 2.2rem",
                fontWeight: "bold",
                fontSize: "1rem",
                cursor: "pointer",
                boxShadow: theme.cardShadow,
                transition: "background 0.6s, color 0.6s",
              }}
            >
              Edit Profile
            </button>
            <button
              style={{
                background: "none",
                border: `2px solid ${theme.accent}`,
                color: theme.accent,
                borderRadius: "1.5rem",
                padding: "0.8rem 2.2rem",
                fontWeight: "bold",
                fontSize: "1rem",
                cursor: "pointer",
                transition: "border 0.6s, color 0.6s",
              }}
            >
              View Transactions
            </button>
          </div>
          <div
            style={{
              marginTop: "2rem",
              color: darkMode ? "#bbb" : "#888",
              fontSize: "1rem",
              textAlign: "center",
            }}
          >
            Need help?{" "}
            <a
              href="#"
              style={{ color: theme.accent, textDecoration: "underline" }}
            >
              Contact support
            </a>
          </div>
        </section>

        <section
          className="glass"
          style={{
            background: theme.cardBg,
            borderRadius: "1.5rem",
            boxShadow: theme.cardShadow,
            padding: "2rem 3rem",
            margin: "0 0 2rem 0",
            maxWidth: "600px",
            width: "100%",
            ...fadeIn,
            border: `1.5px solid ${theme.accentSecondary}`,
          }}
        >
          <h2 style={{ color: theme.accent, fontWeight: 700, fontSize: "1.4rem", marginBottom: "1.2rem" }}>Credit Score Dashboard</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "2rem", marginBottom: "1.2rem" }}>
            <div style={{ fontSize: "2.8rem", fontWeight: 800, color: theme.color }}>726</div>
            <div style={{ color: theme.accent, fontWeight: 600 }}>Good</div>
          </div>
          <div style={{ marginBottom: "1rem", color: theme.color }}>
            <strong>Key Factors:</strong>
            <ul style={{ margin: 0, paddingLeft: "1.2rem" }}>
              <li>+ On-time rent payments</li>
          
