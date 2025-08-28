import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Login - IntelliSearch Enterprise',
  description: 'Sign in to access IntelliSearch Enterprise',
};

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-auto flex items-center justify-center">
            <h1 className="text-2xl font-bold text-gray-900">IntelliSearch</h1>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Use your Google account to access the enterprise search platform
          </p>
        </div>
        <div className="mt-8 space-y-6">
          <div>
            <button
              type="button"
              onClick={() => {
                // Redirect to Google OAuth
                window.location.href = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/google`;
              }}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Sign in with Google
            </button>
          </div>
          
          <div className="text-center">
            <p className="text-xs text-gray-500">
              By signing in, you agree to access internal enterprise resources
            </p>
          </div>
          
          {/* Creator Attribution */}
          <div className="text-center mt-8 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-center space-x-2 text-xs text-gray-400">
              <span>✨</span>
              <span>Crafted with passion by</span>
              <span className="font-semibold text-indigo-600">Vaibhav Nagre</span>
              <span>✨</span>
            </div>
            <div className="mt-1 text-xs text-gray-400">
              Full-Stack Developer • AI & Search Specialist
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
