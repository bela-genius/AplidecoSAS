/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html", "./static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        // Brutalist editorial system — monochrome + one alarm red.
        obsidian: "#000000", // page canvas
        bone: {
          DEFAULT: "#ffffff",
          10: "rgba(255,255,255,0.1)",
          20: "rgba(255,255,255,0.2)",
        },
        ash: "#838383",
        alarm: {
          DEFAULT: "#ed1c24",
          dark: "#c8151c",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Antonio", "Inter", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        display: "-0.079em",
        "display-lg": "-0.02em",
      },
      lineHeight: {
        display: "0.70",
      },
      borderRadius: {
        none: "0px",
        full: "100px",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
