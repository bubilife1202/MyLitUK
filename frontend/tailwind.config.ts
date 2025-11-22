import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Dark Academia Color Palette
        charcoal: '#2C2C2C',
        cream: '#F5F5DC',
        gold: '#C5A059',
        'faded-gold': '#D4AF6A',
        'deep-brown': '#3D2817',
        'vintage-red': '#8B0000',
        'dusty-grey': '#696969',
      },
      fontFamily: {
        'playfair': ['"Playfair Display"', 'serif'],
        'courier': ['"Courier Prime"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.8s ease-in-out',
        'slide-up': 'slideUp 0.6s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
export default config
