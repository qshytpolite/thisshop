/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
},
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  safelist: [
  'alert-info',
  'alert-success',
  'alert-warning',
  'alert-error',
  ],
}

