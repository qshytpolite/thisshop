/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
  ],
  theme: {
    extend: {
      /* Spacing */
      theme: {
        extend: {
          spacing: {
            '1/2': '0.125rem', // Adjust to your preferred spacing
            '1': '0.25rem', // Adjust to your preferred spacing
            '2': '0.5rem', // Adjust to your preferred spacing
            '3': '0.75rem', // Adjust to your preferred spacing
            '4': '1rem', // Adjust to your preferred spacing
            '5': '1.25rem', // Adjust to your preferred spacing
            '6': '1.5rem', // Adjust to your preferred spacing
            '8': '2rem', // Adjust to your preferred spacing
            '10': '2.5rem', // Adjust to your preferred spacing
            '12': '3rem', // Adjust to your preferred spacing
            '16': '4rem', // Adjust to your preferred spacing
            '20': '5rem', // Adjust to your preferred spacing
            '24': '6rem', // Adjust to your preferred spacing
            '32': '8rem', // Adjust to your preferred spacing
            '40': '10rem', // Adjust to your preferred spacing
            '48': '12rem', // Adjust to your preferred spacing
            '56': '14rem', // Adjust to your preferred spacing
            '64': '16rem', // Adjust to your preferred spacing
          },
        },
      },

      /* Border Radius */
      theme: {
        extend: {
          borderRadius: {
            none: '0',
            sm: '0.125rem', // Adjust to your small border radius
            default: '0.25rem', // Adjust to your default border radius
            md: '0.375rem', // Adjust to your medium border radius
            lg: '0.5rem', // Adjust to your large border radius
            full: '9999px', // Adjust to your full border radius
          },
        },
      },

      /* Shadows */
      theme: {
        extend: {
          boxShadow: {
            sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)', // Adjust to your small shadow
            default: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)', // Adjust to your default shadow
            md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)', // Adjust to your medium shadow
            lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)', // Adjust to your large shadow
            xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)', // Adjust to your extra large shadow
            '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)', // Adjust to your 2xl shadow
            inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)', // Adjust to your inner shadow
            outline: '0 0 0 3px rgba(66, 153, 225, 0.5)', // Adjust to your outline shadow
            none: 'none', // No shadow
          },
        },
      },

      /* Grid */
      theme: {
        extend: {
          gridTemplateColumns: {
            '12': 'repeat(12, minmax(0, 1fr))', // Adjust to your grid layout
          },
        },
      },

      /* Z-index */
      theme: {
        extend: {
          zIndex: {
            '0': 0,
            '10': 10,
            '20': 20,
            '30': 30,
            '40': 40,
            '50': 50,
            'auto': 'auto',
          },
        },
      },

      /* Transition Duration */
      theme: {
        extend: {
          transitionDuration: {
            '0': '0ms',
            '75': '75ms',
            '100': '100ms',
            '150': '150ms',
            '200': '200ms',
            '300': '300ms',
            '500': '500ms',
            '700': '700ms',
            '1000': '1000ms',
          },
        },
      },
    },
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

