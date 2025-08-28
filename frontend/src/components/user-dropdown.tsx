'use client';

import { useRouter } from 'next/navigation';

interface UserDropdownProps {
  user: any;
  isDropdownOpen: boolean;
  onToggleDropdown: () => void;
  onSignOut: () => void;
}

export function UserDropdown({ user, isDropdownOpen, onToggleDropdown, onSignOut }: UserDropdownProps) {
  const router = useRouter();

  const handleAdminClick = () => {
    router.push('/admin');
    onToggleDropdown();
  };

  const handleProfileClick = () => {
    router.push('/profile');
    onToggleDropdown();
  };

  return (
    <div className="relative">
      <button
        onClick={onToggleDropdown}
        className="flex items-center space-x-2 p-2 rounded-full hover:bg-gray-100 transition-colors"
        type="button"
      >
        <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
          {user?.name?.charAt(0)?.toUpperCase() || 'U'}
        </div>
      </button>
      
      {isDropdownOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={onToggleDropdown}
          />
          
          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-20">
            <div className="px-4 py-3 border-b border-gray-100">
              <p className="text-sm font-medium text-gray-900">{user?.name}</p>
              <p className="text-sm text-gray-500">{user?.email}</p>
              {user?.groups && user.groups.length > 0 && (
                <p className="text-xs text-gray-400 mt-1">
                  Groups: {user.groups.join(', ')}
                </p>
              )}
            </div>
            
            <div className="py-1">
              {user?.is_admin && (
                <button
                  onClick={handleAdminClick}
                  className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  type="button"
                >
                  Admin Dashboard
                </button>
              )}
              
              <button
                onClick={handleProfileClick}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                type="button"
              >
                Profile Settings
              </button>
              
              <div className="border-t border-gray-100 my-1"></div>
              
              <button
                onClick={onSignOut}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                type="button"
              >
                Sign out
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
