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
          DEFAULT: "#c0392b",
          dark: "#a02f23",
          soft: "#e9968c",
        },
        ink: "#0f0d0c",
        wine: "#894141",
        rose: "#e9abb4",
        cream: {
          DEFAULT: "#f8f2e9",
          dark: "#d9cdb0",
        },
        stone: "#e5dfd7",
        azure: {
          DEFAULT: "#0073fd",
          dark: "#0b3f94",
          sky: "#38b6ff",
          link: "#3d9bff",
          soft: "#bedbff",
        },
        sage: "#a7a38b",
        butter: "#faffc3",
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
