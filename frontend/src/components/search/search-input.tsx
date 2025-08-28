'use client';

import { useState } from 'react';

interface SearchInputProps {
  onSearch: (query: string) => void;
  onSuggestionSelect: (suggestion: any) => void;
  value: string;
  onChange: (value: string) => void;
  suggestions: any[];
  isLoading: boolean;
  placeholder?: string;
}

export function SearchInput({
  onSearch,
  onSuggestionSelect,
  value,
  onChange,
  suggestions,
  isLoading,
  placeholder = 'Search...'
}: SearchInputProps) {
  const [showSuggestions, setShowSuggestions] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim()) {
      onSearch(value);
      setShowSuggestions(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    onChange(newValue);
    setShowSuggestions(newValue.length > 0);
  };

  const handleSuggestionClick = (suggestion: any) => {
    onSuggestionSelect(suggestion);
    setShowSuggestions(false);
  };

  return (
    <div className="relative w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <input
            type="text"
            value={value}
            onChange={handleInputChange}
            onFocus={() => setShowSuggestions(value.length > 0)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
            placeholder={placeholder}
            className="search-input w-full"
            disabled={isLoading}
          />
          
          {/* Search icon */}
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
            {isLoading ? (
              <div className="animate-spin w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full" />
            ) : (
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            )}
          </div>
        </div>
      </form>

      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-80 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="suggestion-item w-full text-left"
            >
              <div className="flex items-center justify-between">
                <span>{suggestion.text}</span>
                {suggestion.source && (
                  <span className="text-xs text-gray-500">{suggestion.source}</span>
                )}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
