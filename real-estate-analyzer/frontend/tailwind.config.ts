import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0A0E1A",
        surface: "#111827",
        surface2: "#1A2235",
        accent: "#63B38A",
        "accent-hover": "#4F9A74",
        amber: "#F2A623",
        coral: "#E8593C",
        blue: "#3B8BD4",
        "text-primary": "#E8EBF0",
        "text-secondary": "#8B96A8",
        "text-muted": "#4A5568",
        "border-green": "rgba(99,179,138,0.15)"
      },
      fontFamily: {
        display: ["var(--font-display)", "serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"]
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(99,179,138,0.15), 0 18px 80px rgba(0,0,0,0.28)"
      }
    }
  },
  plugins: []
};

export default config;

