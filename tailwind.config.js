/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js,py}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}