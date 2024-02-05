/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "discord-color": "#7289DA",
        "aya-color": "#4368e0",
        "aya-color-light": "#6581db",
        "aya-color-very-light": "#d7dff7",
      },
    },
  },
  plugins: [],
};
