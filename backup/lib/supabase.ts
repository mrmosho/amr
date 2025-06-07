import { createClient } from '@supabase/supabase-js';

// Add debug logging
console.log('Environment Loading:', {
  mode: import.meta.env.MODE,
  supabaseUrl: import.meta.env.VITE_SUPABASE_URL,
  hasKey: !!import.meta.env.VITE_SUPABASE_ANON_KEY,
  isDev: import.meta.env.DEV
});

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error(`Supabase credentials missing! 
    URL exists: ${!!supabaseUrl}
    Key exists: ${!!supabaseKey}
    Please check your environment variables.`);
}

export const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
});