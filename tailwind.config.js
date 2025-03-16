/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      // Custom Animations
      animation: {
        'gradient': 'gradient 15s ease infinite', // Gradient background animation
        'fade-in': 'fadeIn 1s ease-in-out', // Fade-in animation
        'slide-in-left': 'slideInLeft 1s ease-in-out', // Slide-in from left animation
        'slide-in-right': 'slideInRight 1s ease-in-out', // Slide-in from right animation
      },
      // Custom Keyframes
      keyframes: {
        gradient: {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
      // Custom Box Shadows (Neon Glow)
      boxShadow: {
        'neon': '0 0 15px rgba(59, 130, 246, 0.8), 0 0 30px rgba(59, 130, 246, 0.6)', // Neon glow effect
      },
      // Custom Background Images (Gradient)
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))', // Radial gradient
      },
      // Custom Font Families
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Default sans font
        poppins: ['Poppins', 'sans-serif'], // Poppins font
        oswald: ['Oswald', 'sans-serif'], // Oswald font
      },
      // Custom Styles for Reveal Elements
      visibility: {
        'hidden': 'hidden',
        'visible': 'visible',
      },
      // Custom Styles for Loading Bar
      height: {
        'loading-bar': '3px',
      },
      width: {
        'loading-bar': '0%',
      },
      // Custom Styles for Scrollbar
      scrollbar: {
        width: '8px',
        track: '#1e1e24',
        thumb: '#3b82f6',
        'thumb-hover': '#2563eb',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'), // Typography plugin
    require('daisyui'), // DaisyUI plugin
    // require('tailwind-scrollbar'), // Scrollbar plugin
  ],
  daisyui: {
    themes: ["light", "acid"], // DaisyUI themes
    utils: true, // Enable DaisyUI utilities
  },
  safelist: [
    'alert-info',
    'alert-success',
    'alert-warning',
    'alert-error',
  ],
};