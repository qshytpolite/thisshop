/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: {
      light: {
        primary: '#f97316',
        secondary: '#64748b',
        accent: '#3b82f6',
        neutral: '#f3f4f6',
        'base-100': '#ffffff',
        info: '#3ABFF8',
        success: '#36D399',
        warning: '#FBBD23',
        error: '#F87272',
      },
      dark: {
        primary: '#f97316',
        secondary: '#64748b',
        accent: '#3b82f6',
        neutral: '#3d4451',
        'base-100': '#ffffff',
        info: '#3ABFF8',
        success: '#36D399',
        warning: '#FBBD23',
        error: '#F87272',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
}

