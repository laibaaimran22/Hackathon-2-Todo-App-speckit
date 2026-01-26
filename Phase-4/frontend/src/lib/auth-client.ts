// Create a custom auth client that makes direct calls to the backend
export const authClient = {
  signIn: {
    email: async ({ email, password }: { email: string; password: string }) => {
      try {
        const response = await fetch(`/api/auth/sign-in/email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        const result = await response.json();

        if (response.ok) {
          // Store the token in localStorage and cookie for middleware
          if (typeof window !== 'undefined') {
            localStorage.setItem('auth-token', result.session.token);
            document.cookie = `auth-token=${result.session.token}; path=/; max-age=604800; SameSite=Lax`;
          }

          return { data: result, error: null };
        } else {
          return { data: null, error: { message: result.detail || result.message || "Sign in failed" } };
        }
      } catch (error) {
        return { data: null, error: { message: "Network error occurred" } };
      }
    },
  },
  signUp: {
    email: async ({ email, password, name }: { email: string; password: string; name: string }) => {
      try {
        const response = await fetch(`/api/auth/sign-up/email`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }), // Backend doesn't require name
        });

        const result = await response.json();

        if (response.ok) {
          // Store the token in localStorage and cookie for middleware
          if (typeof window !== 'undefined') {
            localStorage.setItem('auth-token', result.session.token);
            document.cookie = `auth-token=${result.session.token}; path=/; max-age=604800; SameSite=Lax`;
          }

          return { data: result, error: null };
        } else {
          return { data: null, error: { message: result.detail || result.message || "Sign up failed" } };
        }
      } catch (error) {
        return { data: null, error: { message: "Network error occurred" } };
      }
    },
  },
  signOut: async () => {
    try {
      await fetch(`/api/auth/sign-out`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // Clear the stored token from localStorage and cookie
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth-token');
        document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      }

      return { success: true };
    } catch (error) {
      return { success: false };
    }
  }
};
