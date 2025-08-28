'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SearchInput } from './search-input';
import { SearchResults } from './search-results';
import { ChatInterface } from './chat-interface';
import { FilterPanel } from './filter-panel';
import { QuickAnswer } from './quick-answer';
import { Header } from '@/components/header';
import { useSearch } from '@/hooks/useSearch';
import { useAuth } from '@/hooks/useAuth';
import { SearchFilters, SearchSuggestion } from '@/types';

const DEFAULT_FILTERS: SearchFilters = {
  sources: ['forums', 'docs', 'tickets'],
  timeRange: 'any',
  sortBy: 'relevance',
};

export function SearchInterface() {
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'all' | 'forums' | 'docs' | 'tickets' | 'ai-deeper'>('all');
  const [filters, setFilters] = useState<SearchFilters>(DEFAULT_FILTERS);
  const [isHomepage, setIsHomepage] = useState(true);
  
  const { user, isAuthenticated } = useAuth();
  const { 
    results, 
    isLoading, 
    error, 
    searchTime, 
    totalResults,
    suggestions,
    answer,
    citations,
    search,
    clearResults 
  } = useSearch();

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;
    
    setQuery(searchQuery);
    setIsHomepage(false);
    
    // Filter sources based on authentication status
    let availableSources = isAuthenticated 
      ? filters.sources 
      : ['docs']; // Only public docs for non-authenticated users
    
    if (activeTab !== 'all') {
      // If user is not authenticated and tries to access protected tabs, show only docs
      if (!isAuthenticated && (activeTab === 'forums' || activeTab === 'tickets')) {
        availableSources = ['docs'];
      } else {
        availableSources = [activeTab] as any;
      }
    }
    
    const searchFilters = { ...filters, sources: availableSources };
    await search(searchQuery, searchFilters, isAuthenticated);
  };

  const handleSuggestionSelect = (suggestion: SearchSuggestion) => {
    handleSearch(suggestion.text);
  };

  const handleTabChange = (tab: typeof activeTab) => {
    setActiveTab(tab);
    if (query && tab !== 'ai-deeper') {
      // Re-run search with new filter
      handleSearch(query);
    }
  };

  const handleBackToHome = () => {
    setIsHomepage(true);
    setQuery('');
    clearResults();
  };

  return (
    <div className="min-h-screen bg-white relative">
      <Header />
      
      <AnimatePresence mode="wait">
        {isHomepage ? (
          <HomePage 
            key="homepage"
            onSearch={handleSearch}
            onSuggestionSelect={handleSuggestionSelect}
            query={query}
            onQueryChange={setQuery}
            suggestions={suggestions}
            isLoading={isLoading}
            isAuthenticated={isAuthenticated}
          />
        ) : (
          <SearchPage
            key="searchpage"
            query={query}
            onSearch={handleSearch}
            onSuggestionSelect={handleSuggestionSelect}
            onQueryChange={setQuery}
            suggestions={suggestions}
            results={results}
            isLoading={isLoading}
            error={error}
            searchTime={searchTime}
            totalResults={totalResults}
            activeTab={activeTab}
            onTabChange={handleTabChange}
            filters={filters}
            onFiltersChange={setFilters}
            answer={answer}
            citations={citations}
            onBackToHome={handleBackToHome}
            isAuthenticated={isAuthenticated}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

function HomePage({ 
  onSearch, 
  onSuggestionSelect, 
  query, 
  onQueryChange, 
  suggestions, 
  isLoading,
  isAuthenticated
}: {
  onSearch: (query: string) => void;
  onSuggestionSelect: (suggestion: SearchSuggestion) => void;
  query: string;
  onQueryChange: (query: string) => void;
  suggestions: SearchSuggestion[];
  isLoading: boolean;
  isAuthenticated: boolean;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex flex-col"
    >
      {/* Main content */}
      <main className="flex-1 flex flex-col justify-center px-6 pt-16">
        <div className="search-container">
          {/* Logo */}
          <motion.div
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="text-center mb-8"
          >
            <h1 className="text-6xl font-light text-gray-700 mb-2">
              IntelliSearch
            </h1>
            <p className="text-lg text-gray-500">
              {isAuthenticated 
                ? "Search across forums, docs, and support tickets"
                : "Search public documentation and resources"
              }
            </p>
          </motion.div>

          {/* Authentication notice for non-authenticated users */}
          {!isAuthenticated && (
            <motion.div
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.15 }}
              className="text-center mb-6"
            >
              <div className="inline-flex items-center bg-blue-50 text-blue-700 px-4 py-2 rounded-lg text-sm">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                Sign in to access forums and support tickets
              </div>
            </motion.div>
          )}

          {/* Search input */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <SearchInput
              onSearch={onSearch}
              onSuggestionSelect={onSuggestionSelect}
              value={query}
              onChange={onQueryChange}
              suggestions={suggestions}
              isLoading={isLoading}
              placeholder="Search for anything..."
            />
          </motion.div>

          {/* Action buttons */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex justify-center space-x-4"
          >
            <button 
              className="search-button"
              onClick={() => query && onSearch(query)}
              disabled={!query.trim()}
            >
              Search
            </button>
            <button 
              className="search-button"
              onClick={() => onSearch('getting started')}
            >
              I'm Exploring
            </button>
          </motion.div>

          {/* Quick links */}
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="mt-12 text-center"
          >
            <p className="text-sm text-gray-500 mb-4">Quick access:</p>
            <div className="flex justify-center space-x-6 text-sm">
              <button
                onClick={() => onSearch('API documentation')}
                className="text-blue-600 hover:text-blue-800 transition-colors"
              >
                API Docs
              </button>
              <button
                onClick={() => onSearch('getting started')}
                className="text-blue-600 hover:text-blue-800 transition-colors"
              >
                Getting Started
              </button>
              <button
                onClick={() => onSearch('integration guide')}
                className="text-blue-600 hover:text-blue-800 transition-colors"
              >
                Integration Guide
              </button>
              {isAuthenticated && (
                <>
                  <button
                    onClick={() => onSearch('troubleshooting')}
                    className="text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    Troubleshooting
                  </button>
                  <button
                    onClick={() => onSearch('support tickets')}
                    className="text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    Support
                  </button>
                </>
              )}
            </div>
          </motion.div>

          {/* Creator Attribution */}
          <motion.div
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-16 flex justify-center"
          >
            <div className="group relative">
              <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 p-0.5 rounded-full">
                <div className="bg-white rounded-full px-6 py-3 flex items-center space-x-3 hover:bg-gray-50 transition-all duration-300 cursor-pointer">
                  <div className="relative">
                    <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm animate-pulse">
                      VN
                    </div>
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-bounce"></div>
                  </div>
                  <div className="text-sm">
                    <div className="font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300">
                      Crafted with ❤️ by Vaibhav Nagre
                    </div>
                    <div className="text-xs text-gray-500 group-hover:text-gray-700 transition-colors duration-300">
                      Full-Stack Developer • AI Enthusiast
                    </div>
                  </div>
                  <div className="text-lg group-hover:animate-spin transition-transform duration-300">
                    ✨
                  </div>
                </div>
              </div>
              
              {/* Tooltip */}
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-72 bg-gray-900 text-white text-xs rounded-lg py-3 px-4 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300">
                <div className="text-center">
                  <div className="font-semibold mb-1">👨‍💻 Vaibhav Nagre</div>
                  <div className="text-gray-300 mb-2">Passionate about building intelligent search solutions</div>
                  <div className="flex justify-center space-x-4 text-gray-400">
                    <span>🚀 Full-Stack</span>
                    <span>🤖 AI/ML</span>
                    <span>🔍 Search Expert</span>
                  </div>
                </div>
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
              </div>
            </div>
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="p-6 text-center text-xs text-gray-500">
        <div className="space-x-6">
          <a href="#" className="hover:text-gray-700">Privacy</a>
          <a href="#" className="hover:text-gray-700">Terms</a>
          <a href="#" className="hover:text-gray-700">Help</a>
        </div>
      </footer>
    </motion.div>
  );
}

function SearchPage({
  query,
  onSearch,
  onSuggestionSelect,
  onQueryChange,
  suggestions,
  results,
  isLoading,
  error,
  searchTime,
  totalResults,
  activeTab,
  onTabChange,
  filters,
  onFiltersChange,
  answer,
  citations,
  onBackToHome,
  isAuthenticated,
}: any) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen pt-16"
    >
      {/* Header */}
      <header className="border-b border-gray-200 bg-white sticky top-0 z-40">
        <div className="results-container py-4">
          <div className="flex items-center space-x-8">
            {/* Logo */}
            <button 
              onClick={onBackToHome}
              className="text-2xl font-light text-gray-700 hover:text-gray-900 transition-colors"
            >
              IntelliSearch
            </button>

            {/* Search input */}
            <div className="flex-1 max-w-2xl">
              <SearchInput
                onSearch={onSearch}
                onSuggestionSelect={onSuggestionSelect}
                value={query}
                onChange={onQueryChange}
                suggestions={suggestions}
                isLoading={isLoading}
                placeholder="Search..."
              />
            </div>
          </div>

          {/* Search tabs */}
          <div className="flex space-x-0 mt-4">
            {[
              { id: 'all', label: 'All', protected: false },
              { id: 'forums', label: 'Forums', protected: true },
              { id: 'docs', label: 'Docs', protected: false },
              { id: 'tickets', label: 'Tickets', protected: true },
              { id: 'ai-deeper', label: 'AI Deeper', protected: true },
            ].map((tab) => {
              const isDisabled = tab.protected && !isAuthenticated;
              
              return (
                <button
                  key={tab.id}
                  onClick={() => !isDisabled && onTabChange(tab.id)}
                  disabled={isDisabled}
                  className={`search-tab ${
                    activeTab === tab.id ? 'search-tab-active' : ''
                  } ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                  title={isDisabled ? 'Sign in to access this section' : ''}
                >
                  {tab.label}
                  {tab.protected && !isAuthenticated && (
                    <svg className="w-3 h-3 ml-1 inline" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="results-container py-6">
        {/* Authentication prompt for protected content */}
        {!isAuthenticated && (activeTab === 'forums' || activeTab === 'tickets' || activeTab === 'ai-deeper') && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="text-sm font-medium text-blue-800">Authentication Required</h3>
                <p className="text-sm text-blue-700 mt-1">
                  Sign in to search {activeTab === 'forums' ? 'community forums' : activeTab === 'tickets' ? 'support tickets' : 'AI chat'}. 
                  Showing public documentation results instead.
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-8">
          {/* Left column - Results */}
          <div className="flex-1">
            {activeTab === 'ai-deeper' ? (
              isAuthenticated ? (
                <ChatInterface />
              ) : (
                <div className="text-center py-12">
                  <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                  </svg>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">AI Deeper Chat</h3>
                  <p className="text-gray-600">Sign in to access AI-powered conversational search</p>
                </div>
              )
            ) : (
              <>
                {/* Quick answer */}
                {answer && (
                  <QuickAnswer
                    answer={answer}
                    citations={citations}
                    className="mb-6"
                  />
                )}

                {/* Search results */}
                <SearchResults
                  results={results}
                  query={query}
                  totalResults={totalResults}
                  searchTime={searchTime}
                  isLoading={isLoading}
                  error={error}
                />
              </>
            )}
          </div>

          {/* Right column - Filters and context */}
          {activeTab !== 'ai-deeper' && (
            <div className="w-80">
              <FilterPanel
                filters={filters}
                onFiltersChange={onFiltersChange}
                resultCounts={{
                  forums: results.filter(r => r.source === 'forums').length,
                  docs: results.filter(r => r.source === 'docs').length,
                  tickets: results.filter(r => r.source === 'tickets').length,
                }}
              />
            </div>
          )}
        </div>
      </main>
    </motion.div>
  );
}
