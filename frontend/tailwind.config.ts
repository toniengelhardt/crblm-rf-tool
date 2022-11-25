import type { Config } from 'tailwindcss'

export default <Partial<Config>>{
  theme: {
    // extend: {
    //   text: {
    //     dim: `${defaultTheme.colors.green} dark:${defaultTheme}`,
    //   }
    // }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('daisyui')
  ],
}
