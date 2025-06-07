import { supabase } from '@/lib/supabase';
import { User } from '@supabase/supabase-js';

export const authService = {
  async login(email: string, password: string) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) throw error;
    return data;
  },

  async register(userData: {
    email: string;
    password: string;
    name: string;
  }) {
    console.log('Starting registration process...', { email: userData.email });

    const { data, error } = await supabase.auth.signUp({
      email: userData.email,
      password: userData.password,
      options: {
        data: {
          full_name: userData.name
        },
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      }
    });

    if (error) {
      console.error('Registration error:', error);
      throw error;
    }

    console.log('Auth signup response:', data);

    // Only create profile if we have a user
    if (data.user) {
      console.log('Creating user profile...');
      const { error: profileError } = await supabase
        .from('profiles')
        .insert({
          id: data.user.id,
          email: userData.email,
          full_name: userData.name,
        });

      if (profileError) {
        console.error('Profile creation error:', profileError);
        throw profileError;
      }
    }

    return data;
  },

  async resetPassword(email: string) {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/reset-password`,
    });

    if (error) throw error;
  },

  async updatePassword(newPassword: string) {
    const { error } = await supabase.auth.updateUser({
      password: newPassword
    });

    if (error) throw error;
  },

  async getCurrentUser(): Promise<User | null> {
    const { data: { user } } = await supabase.auth.getUser();
    return user;
  },

  async logout() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  }
};