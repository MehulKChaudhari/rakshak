module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: {
    tailwindcss: [require('@tailwindcss/forms')],
    autoprefixer: {},
  }
}
