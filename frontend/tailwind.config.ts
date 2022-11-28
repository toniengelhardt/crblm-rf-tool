import type { Config } from 'tailwindcss'
import tailwindNesting from '@tailwindcss/nesting'
import tailwindTypography from '@tailwindcss/typography'

export default <Partial<Config>>{
  theme: {
    // extend: {
    //   colors: {
    //     primary: defaultTheme.colors.green
    //   }
    // }
  },
  plugins: [
    tailwindNesting,
    tailwindTypography,
    require('daisyui'),
  ],
  // daisyui: {
  //   themes: [
  //     'cupcake',
  //   ],
  // }
}
