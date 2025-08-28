'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { User, AuthState } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useAuth() {
  const queryClient = useQueryClient();
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Check authentication status
  const { data: authData, isLoading: isAuthLoading } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      try {
        // First check localStorage for demo user
        const token = localStorage.getItem('auth_token');
        const userInfo = localStorage.getItem('user_info');
        
        if (token && userInfo) {
          try {
            const user = JSON.parse(userInfo);
            return user;
          } catch (e) {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_info');
          }
        }

        // Try backend authentication if no local user
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'Authorization': token ? `Bearer ${token}` : '',
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            return null; // Not authenticated
          }
          throw new Error('Failed to check authentication');
        }

        const user: User = await response.json();
        return user;
      } catch (error) {
        console.error('Auth check failed:', error);
        return null;
      }
    },
    retry: false,
    staleTime: 60000, // 1 minute
  });

  // Update auth state when data changes
  useEffect(() => {
    setAuthState({
      user: authData || null,
      isAuthenticated: !!authData,
      isLoading: isAuthLoading,
    });
  }, [authData, isAuthLoading]);

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: async () => {
      // Redirect to backend login endpoint
      window.location.href = `${API_BASE_URL}/auth/login`;
    },
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: async () => {
      // Clear localStorage first
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');

      try {
        const response = await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          credentials: 'include',
        });

        if (!response.ok) {
          console.warn('Backend logout failed, but local session cleared');
        }

        return { success: true };
      } catch (error) {
        console.warn('Backend logout failed, but local session cleared:', error);
        return { success: true };
      }
    },
    onSuccess: () => {
      // Clear all queries
      queryClient.clear();
      
      // Update auth state
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });

      // Refresh the page to update UI
      window.location.reload();
    },
    onError: (error) => {
      console.error('Logout failed:', error);
    },
  });

  const login = () => {
    loginMutation.mutate();
  };

  const logout = () => {
    logoutMutation.mutate();
  };

  // Check if user has specific permission
  const hasPermission = (permission: string) => {
    return authState.user?.permissions?.includes(permission) || false;
  };

  // Check if user is in specific group
  const hasGroup = (group: string) => {
    return authState.user?.groups?.includes(group) || false;
  };

  return {
    ...authState,
    login,
    logout,
    hasPermission,
    hasGroup,
    isLoggingIn: loginMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
  };
}

// Hook for handling OAuth callback
export function useAuthCallback() {
  const queryClient = useQueryClient();
  
  const callbackMutation = useMutation({
    mutationFn: async (code: string) => {
      const response = await fetch(`${API_BASE_URL}/auth/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error('Authentication failed');
      }

      return response.json();
    },
    onSuccess: () => {
      // Invalidate auth queries to refetch user data
      queryClient.invalidateQueries({ queryKey: ['auth'] });
      
      // Redirect to home page
      window.location.href = '/';
    },
    onError: (error) => {
      console.error('Auth callback failed:', error);
      // Redirect to home page with error
      window.location.href = '/?error=auth_failed';
    },
  });

  return {
    handleCallback: callbackMutation.mutate,
    isProcessing: callbackMutation.isPending,
    error: callbackMutation.error,
  };
}
