/** @type {import('tailwindcss').Config} */


module.exports = {
  content: ['./src/**/*.{html,js}', './index.html'], // Adjust paths to your project
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif'] // Telekom font family
      },
      gridTemplateColumns: {
        '70/30': '70% 28%',
      }
      }
    },    
    variants: {
      extend: {}
  },
  plugins: [],
};  