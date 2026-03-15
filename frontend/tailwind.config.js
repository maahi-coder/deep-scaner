/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#040508',
        surface: '#0B0D14',
        primary: '#00F0FF',
        secondary: '#9D00FF',
        danger: '#FF003C'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        orbitron: ['Orbitron', 'sans-serif'],
        syncopate: ['Syncopate', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
