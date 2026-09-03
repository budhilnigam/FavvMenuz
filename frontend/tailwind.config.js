/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cream: {
          50: '#FFFDF9',
          100: '#FAF7EE',
          200: '#F3EEDC',
          300: '#E7DFC4',
        },
        electric: {
          yellow: '#FFE600',
          hover: '#F2D800',
        },
        coral: {
          500: '#FF5238',
          600: '#E83E25',
        },
        cobalt: {
          500: '#2563EB',
          600: '#1D4ED8',
        },
        fresh: {
          green: '#00C853',
          dark: '#009624',
        },
        ink: '#121212',
      },
      boxShadow: {
        'brutal-sm': '2px 2px 0px #000000',
        'brutal': '4px 4px 0px #000000',
        'brutal-lg': '6px 6px 0px #000000',
        'brutal-xl': '8px 8px 0px #000000',
      },
      borderWidth: {
        '3': '3px',
      },
    },
  },
  plugins: [],
}
