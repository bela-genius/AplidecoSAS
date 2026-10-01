/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html", "./static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        // Paleta institucional — Manual de Identidad Corporativa APLIDECO S.A.S.
        crema: {
          DEFAULT: "#F9FAF5", // Blanco Obra — fondo dominante (60%)
          100: "#F9FAF5",
          200: "#F0F2EA",
          300: "#E3E6D9",
        },
        carbon: {
          DEFAULT: "#1E2118", // texto principal
          700: "#2E3326",
          500: "#52583F",
        },
        rojo: {
          DEFAULT: "#C90003", // Rojo Aplideco — acentos (10%)
          600: "#C90003",
          700: "#A30002",
          100: "#F7D9D9",
        },
        obra: {
          DEFAULT: "#185100", // Verde Obra — estructura (25%)
          700: "#185100",
          800: "#0F3A00",
          600: "#2A7700",
          100: "#DCE9D4",
        },
        oliva: {
          DEFAULT: "#A4AA38", // Verde Oliva — acento (5%)
          600: "#A4AA38",
          700: "#878C2B",
          300: "#CBCE82",
        },
      },
      fontFamily: {
        sans: ["Jost", "system-ui", "sans-serif"],
        display: ["'Bebas Neue'", "Jost", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        tightest: "-0.02em",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
