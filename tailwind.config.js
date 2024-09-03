/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js,py}"],
  theme: {
    extend: {
      colors: {
        'dark-800': '#363636',
        'dark-600': '#676767',
        'gray-221': '#dddddd',
        'gray-94': '#f0f0f0',
        'gray-90': '#e5e5e5',
        'gray-83': '#d4d4d4',
        'gray-69': '#b0b0b0',
        'gray-56': '#8f8f8f',
        'gray-2d2': '#2d2d2d',
        'gray-616': '#616161',
        'gray-cbc': '#cbcbcb',
        'gray-3c4': '#3c4043',
        'gray-d5d': '#d5d5d5',
        'gray-e1e': '#e1eefb',
        'red-primary': '#ae2024',
        'red-900': '#990000',
        'red-e21': '#e21e28',
        'blue-3d6': '#3d6aaf',
        'green-06c': '#06C755',
        'green-1b9': '#1b9e6e',
      },
      boxShadow: {
        'nav-bar': '0 1px 8px 0 rgba(0, 0, 0, .2)',
        'area': '0 1px 1px rgba(0, 0, 0, .15), -1px 0 0 rgba(0, 0, 0, .03), 1px 0 0 rgba(0, 0, 0, .03), 0 1px 0 rgba(0, 0, 0, .12)',
        'sign-in': '0 0 10px rgba(0, 0, 0, .38)',
        'watchlist': '0 1px 2px rgba(0, 0, 0, .25)',
      },
    },
    fontFamily: {
      'sans': ['Arial', 'Helvetica', 'sans-serif'],
      'jhenghei': ['"Microsoft JhengHei"', 'sans-serif'],
      'noto': ['Noto Sans TC', 'sans-serif'],
      'upgrade': ['Segoe UI', 'Segoe UI Historic', 'Helvetica', 'Arial', 'sans-serif'],
    },
  },
  plugins: [
    require('daisyui'),
  ],
}