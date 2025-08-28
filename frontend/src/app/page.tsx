'use client';

import { SearchInterface } from '@/components/search/search-interface';

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col">
      <div className="flex-1">
        <SearchInterface />
      </div>
      
      {/* Animated Footer with Creator Info */}
      <footer className="bg-gradient-to-r from-gray-50 to-gray-100 border-t">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                © 2025 IntelliSearch Enterprise
              </div>
            </div>
            
            <div className="group flex items-center space-x-3 bg-white rounded-full px-4 py-2 shadow-sm border hover:shadow-md transition-all duration-300">
              <div className="relative">
                <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm group-hover:scale-110 transition-transform duration-300">
                  VN
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
              </div>
              <div className="text-sm">
                <div className="font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300">
                  Crafted by Vaibhav Nagre
                </div>
                <div className="text-xs text-gray-500 group-hover:text-gray-700 transition-colors duration-300">
                  Full-Stack Developer & AI Enthusiast
                </div>
              </div>
              <div className="text-lg group-hover:animate-bounce">
                🚀
              </div>
            </div>
            
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <span className="animate-pulse">⭐</span>
              <span>Made with passion for intelligent search</span>
              <span className="animate-pulse">⭐</span>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
