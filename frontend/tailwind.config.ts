import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-space-grotesk)", "ui-sans-serif", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#e8fcf8",
          100: "#c7f8ee",
          200: "#8bf0d9",
          300: "#4de5c2",
          400: "#18d3aa",
          500: "#0caf8c",
          600: "#0c8c72",
          700: "#0e6f5d",
          800: "#11584c",
          900: "#12493f"
        }
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,.08), 0 20px 40px rgba(7,12,26,.22)",
      }
    },
  },
  plugins: [],
};

export default config;
