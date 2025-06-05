import { createClient } from '@supabase/supabase-js'

// Debug environment variables
const debugEnv = () => {
  console.log('Supabase Configuration:', {
    url: import.meta.env.VITE_SUPABASE_URL,
    hasKey: !!import.meta.env.VITE_SUPABASE_ANON_KEY,
    isDevelopment: import.meta.env.DEV,
    mode: import.meta.env.MODE,
  });
};

debugEnv();

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error(
    `Environment Variables Missing:
    URL: ${!!supabaseUrl}
    Key: ${!!supabaseKey}
    Please check your .env file and Vite configuration.`
  );
}

export const supabase = createClient(supabaseUrl, supabaseKey);