module.exports = {
    content: [
      // Update these paths to where your HTML and JavaScript files are located
      './templates/**/*.html',
      './static/**/*.js',
    ],
    theme: {
      extend: {
        colors: {
          pink: '#FF90E8',
          'baby-blue': '#90A8ED',
          yellow: '#F1F333',
          teal: '#23A094',
          violet: '#B23386',
          orange: '#E2442F',
          red: '#98282A',
          dimgrey: '#78716C',
          'smoke-white': '#F4F4F0',
          'yellow-dark': '#FFC900',
          black: '#000000',
          white: '#FFFFFF',
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
  