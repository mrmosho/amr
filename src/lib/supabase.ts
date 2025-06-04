import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

console.log('Supabase URL:', supabaseUrl) // Debugging
console.log('Supabase Key exists:', !!supabaseKey) // Debugging

if (!supabaseUrl || !supabaseKey) {
  throw new Error(`Missing environment variables: ${!supabaseUrl ? 'VITE_SUPABASE_URL' : ''} ${!supabaseKey ? 'VITE_SUPABASE_ANON_KEY' : ''}`)
}

export const supabase = createClient(supabaseUrl, supabaseKey)