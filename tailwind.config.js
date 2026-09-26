/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./apps/**/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        graphite: {
          950: "#101010",
          900: "#1A1A1A",
          800: "#232323",
          700: "#2E2E2E",
          600: "#3D3D3D",
          500: "#585858",
          400: "#767676",
          200: "#C9C9C9",
          100: "#E7E7E5",
          50: "#F6F6F4",
        },
        accent: {
          DEFAULT: "#FF5A1F",
          dark: "#D6480F",
          light: "#FF8B57",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Manrope", "Inter", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        tightest: "-0.04em",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
