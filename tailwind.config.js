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
        cream: {
          DEFAULT: "#f5efe0",
          dark: "#d9cdb0",
        },
        azure: {
          DEFAULT: "#1a7bff",
          dark: "#1262d0",
          soft: "#8fbaff",
        },
        sage: "#c9c9a6",
        butter: "#fbf7b5",
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
