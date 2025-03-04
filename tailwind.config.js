/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './static/**/*.js',
  ],
  theme: {
    extend: {
   },

},
  plugins: [
    require('@tailwindcss/typography'),require('daisyui'),
  ],
  daisyui: {
    themes: ["light","acid"],
    utils: true,
  },
  safelist: [
  'alert-info',
  'alert-success',
  'alert-warning',
  'alert-error',
  ],
}

