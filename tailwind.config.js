/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.{html,js}",
    './templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'dark-800': '#363636',
        'gray-90': '#e5e5e5',
        'red-primary': '#ae2024',
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
}