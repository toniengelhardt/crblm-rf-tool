import type { Config } from 'tailwindcss'
import tailwindNesting from '@tailwindcss/nesting'
import tailwindTypography from '@tailwindcss/typography'

export default <Partial<Config>>{
  plugins: [
    tailwindNesting,
    tailwindTypography,
    require('daisyui'),
  ],
}
