/**
 * Tailwind CSS Configuration
 */

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'medical-red': '#ef4444',
        'medical-green': '#10b981',
        'medical-blue': '#0ea5e9',
      },
      borderRadius: {
        '3xl': '1.5rem',
      },
      spacing: {
        '128': '32rem',
      },
      animation: {
        'fadeInUp': 'fadeInUp 0.6s ease-out',
        'shimmer': 'shimmer 2s infinite',
        'pulse-ring': 'pulse-ring 2s infinite',
      },
    },
  },
  plugins: [],
}
