module.exports = {
    content: [
      // Update these paths to where your HTML and JavaScript files are located
      './templates/**/*.html',
      './static/**/*.js',
    ],
    theme: {
      extend: {
        colors: {
          'custom-pink': '#FF90E8',
          'custom-baby-blue': '#90A8ED',
          'custom-yellow': '#F1F333',
          'custom-teal': '#23A094',
          'custom-violet': '#B23386',
          'custom-orange': '#E2442F',
          'custom-red': '#98282A',
          'custom-dimgrey': '#78716C',
          'custom-smoke-white': '#F4F4F0',
          'custom-yellow-dark': '#FFC900',
          'custom-black': '#000000',
          'custom-white': '#FFFFFF',
        },
        borderColor: {
          DEFAULT: '#000000', // This sets the default border color
        },
        borderWidth: {
          '2': '2px',
        },
      },
    },
    plugins: [],
  }
  