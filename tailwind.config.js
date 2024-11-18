/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './static/**/*.js',
  ],
  theme: {
    extend: {colors: {
      // Primary and accent colors
      'primary': '#2D3748',
      'accent': '#38B2AC',

      // Neutral colors
      'gray-100': '#F7FAFC',
      'gray-200': '#EDF2F7',
      'gray-300': '#E2E8F0',
      'gray-400': '#CBD5E0',
      'gray-500': '#A0AEC0',
      'gray-600': '#718096',
      'gray-700': '#4A5568',
      'gray-800': '#2D3748',
      'gray-900': '#1A202C',

      // Background and text colors
      'background': '#F7FAFC',
      'text': '#2D3748',

      // Button colors
      'button-primary': '#38B2AC',
      'button-primary-hover': '#319795',
      'button-secondary': '#718096',
      'button-secondary-hover': '#4A5568',
    },
    fontFamily: {
      // Customize your font stack here
      // Example:
      // 'sans': ['Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      // 'serif': ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
    },
    fontSize: {
      // Customize font sizes for headings and text
      // Example:
      // 'xs': '.75rem',
      // 'sm': '.875rem',
      // 'base': '1rem',
      // 'lg': '1.125rem',
      // 'xl': '1.25rem',
      // '2xl': '1.5rem',
      // '3xl': '1.875rem',
      // '4xl': '2.25rem',
      // '5xl': '3rem',
      // '6xl': '4rem',
    },
    spacing: {
      // Customize spacing values for margins, paddings, etc.
      // Example:
      // 'px': '1px',
      // '0': '0',
      // '1': '0.25rem',
      // '2': '0.5rem',
      // '3': '0.75rem',
      // '4': '1rem',
      // '5': '1.25rem',
      // '6': '1.5rem',
      // '8': '2rem',
      // '10': '2.5rem',
      // '12': '3rem',
      // '16': '4rem',
      // '20': '5rem',
      // '24': '6rem',
      // '32': '8rem',
      // '40': '10rem',
      // '48': '12rem',
      // '56': '14rem',
      // '64': '16rem',
    },
    boxShadow: {
      // Customize box shadows for different elements
      // Example:
      // 'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      // 'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      // 'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      // 'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      // '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      // 'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      // 'outline': '0 0 0 3px rgba(66, 153, 225, 0.5)',
      // 'none': 'none',
    },},
  daisyui: {
    themes: ["cmyk", "dark", "acid"],
    utils: true,
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

