/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.{html,js}",
    './templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        'dark-600': '#676767',
        'dark-800': '#363636',
        'gray-221': '#dddddd',
        'gray-69': '#b0b0b0',
        'gray-83': '#d4d4d4',
        'gray-90': '#e5e5e5',
        'gray-94': '#f0f0f0',
        'red-primary': '#ae2024',
        'red-900': '#990000',
      },
      boxShadow: {
        'nav-bar': '0 1px 8px 0 rgba(0, 0, 0, .2)',
        'aside-right': '0 1px 1px rgba(0, 0, 0, .15), -1px 0 0 rgba(0, 0, 0, .03), 1px 0 0 rgba(0, 0, 0, .03), 0 1px 0 rgba(0, 0, 0, .12)',
      },
    },
    fontFamily: {
      'sans': ['Arial', 'Helvetica', 'sans-serif'],
    }
  },
  plugins: [
    require('daisyui'),
  ],
}