module.exports = {
  content: ["./src/**/*.{html,js}", "./popup.html"],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms')],
}