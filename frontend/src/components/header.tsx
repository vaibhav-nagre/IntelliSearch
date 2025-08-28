'use client';

import { useAuth } from '@/hooks/useAuth';
import { useState } from 'react';
import { SignInButton } from './sign-in-button';
import { UserDropdown } from './user-dropdown';

export function Header() {
  const { isAuthenticated, user, logout, isLoading } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  if (isLoading) {
    return (
      <header className="absolute top-0 right-0 p-4">
        <div className="w-8 h-8 bg-gray-200 rounded-full animate-pulse"></div>
      </header>
    );
  }

  const handleSignOut = () => {
    logout();
    setIsDropdownOpen(false);
  };

  const handleToggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  return (
    <>
      {/* Creator Badge - Top Left */}
      <div className="absolute top-4 left-4 z-20">
        <div className="group relative">
          <div className="flex items-center space-x-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-medium shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer">
            <span className="animate-pulse">👨‍💻</span>
            <span>Created by Vaibhav Nagre</span>
            <span className="animate-bounce">✨</span>
          </div>
          <div className="absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-xl border opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform translate-y-2 group-hover:translate-y-0 p-4 z-30">
            <div className="text-center">
              <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full mx-auto mb-2 flex items-center justify-center text-white font-bold text-lg">
                VN
              </div>
              <h3 className="font-semibold text-gray-900">Vaibhav Nagre</h3>
              <p className="text-xs text-gray-600 mt-1">Full-Stack Developer</p>
              <p className="text-xs text-gray-500 mt-1">AI & Enterprise Search Specialist</p>
              <div className="mt-3 flex justify-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-xs text-gray-600">Building intelligent solutions</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Header - Top Right */}
      <header className="absolute top-0 right-0 p-4 z-10">
        {!isAuthenticated ? (
          <SignInButton className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm">
            Sign in
          </SignInButton>
        ) : (
          <UserDropdown
            user={user}
            isDropdownOpen={isDropdownOpen}
            onToggleDropdown={handleToggleDropdown}
            onSignOut={handleSignOut}
          />
        )}
      </header>
    </>
  );
}
