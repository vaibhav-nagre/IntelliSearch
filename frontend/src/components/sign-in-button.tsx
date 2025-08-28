'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useQueryClient } from '@tanstack/react-query';

interface SignInButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function SignInButton({ className, children }: SignInButtonProps) {
  const router = useRouter();
  const queryClient = useQueryClient();

  const handleSignIn = () => {
    // For demo purposes, simulate authentication
    const mockUser = {
      id: 'demo-user',
      name: 'Demo User',
      email: 'demo@intellisearch.com',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
      groups: ['users'],
      permissions: ['search', 'view_docs']
    };
    
    // Store in localStorage for demo
    localStorage.setItem('auth_token', 'demo-token');
    localStorage.setItem('user_info', JSON.stringify(mockUser));
    
    // Update the auth query cache with mock user data
    queryClient.setQueryData(['auth', 'me'], mockUser);
    
    // Refresh the page to update UI
    window.location.reload();
  };

  return (
    <button
      onClick={handleSignIn}
      className={className}
      type="button"
    >
      {children || 'Sign in'}
    </button>
  );
}
