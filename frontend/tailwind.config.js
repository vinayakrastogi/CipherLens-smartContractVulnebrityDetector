/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'risk-high': '#ef4444',
        'risk-moderate': '#f59e0b',
        'risk-low': '#10b981',
        'risk-safe': '#059669',
      }
    },
  },
  plugins: [],
}
