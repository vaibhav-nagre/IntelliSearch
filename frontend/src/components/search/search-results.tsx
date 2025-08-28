'use client';

import { formatDistanceToNow } from 'date-fns';
import { SearchResult } from '@/types';

interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  totalResults: number;
  searchTime: number;
  isLoading: boolean;
  error: string | null;
  onLoadMore?: () => void;
  hasMore?: boolean;
}

export function SearchResults({
  results,
  query,
  totalResults,
  searchTime,
  isLoading,
  error,
  onLoadMore,
  hasMore = false,
}: SearchResultsProps) {
  if (isLoading && results.length === 0) {
    return <SearchSkeleton />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h3 className="text-lg font-medium">Search Error</h3>
          <p className="text-gray-600 mt-2">{error}</p>
        </div>
        <button
          onClick={() => window.location.reload()}
          className="search-button"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (results.length === 0 && !isLoading) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 mb-4">
          <svg className="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <h3 className="text-lg font-medium">No results found</h3>
          <p className="text-gray-600 mt-2">
            Try different keywords or check your spelling
          </p>
        </div>
        <div className="text-sm text-gray-500">
          <p>Search tips:</p>
          <ul className="mt-2 space-y-1">
            <li>• Use specific keywords related to your issue</li>
            <li>• Try searching for error messages or specific features</li>
            <li>• Check different sources using the tabs above</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Results metadata */}
      <div className="mb-6 text-sm text-gray-600">
        About {totalResults.toLocaleString()} results 
        {searchTime > 0 && ` (${(searchTime / 1000).toFixed(2)} seconds)`}
      </div>

      {/* Results list */}
      <div className="space-y-6">
        {results.map((result, index) => (
          <SearchResultItem key={`${result.url}-${index}`} result={result} query={query} />
        ))}
      </div>

      {/* Load more */}
      {hasMore && (
        <div className="text-center mt-8">
          <button
            onClick={onLoadMore}
            disabled={isLoading}
            className="search-button"
          >
            {isLoading ? 'Loading...' : 'Load More Results'}
          </button>
        </div>
      )}

      {/* Loading indicator for additional results */}
      {isLoading && results.length > 0 && (
        <div className="text-center py-4">
          <div className="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto" />
        </div>
      )}
    </div>
  );
}

function SearchResultItem({ result, query }: { result: SearchResult; query: string }) {
  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'forums':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        );
      case 'docs':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
          </svg>
        );
      case 'tickets':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22 10V6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v4c1.1 0 2 .9 2 2s-.9 2-2 2v4c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2v-4c-1.1 0-2-.9-2-2s.9-2 2-2z"/>
          </svg>
        );
      default:
        return null;
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'forums':
        return 'text-blue-600';
      case 'docs':
        return 'text-green-600';
      case 'tickets':
        return 'text-orange-600';
      default:
        return 'text-gray-600';
    }
  };

  const highlightText = (text: string, query: string) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-200 px-1 rounded">
          {part}
        </mark>
      ) : (
        part
      )
    );
  };

  return (
    <article className="result-card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* URL and source */}
          <div className="flex items-center space-x-2 mb-1">
            <span className={`flex items-center space-x-1 text-sm ${getSourceColor(result.source)}`}>
              {getSourceIcon(result.source)}
              <span className="capitalize">{result.source}</span>
            </span>
            <span className="text-gray-400">•</span>
            <span className="result-url">{result.url}</span>
          </div>

          {/* Title */}
          <h3 className="result-title">
            <a 
              href={result.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:underline"
            >
              {highlightText(result.title, query)}
            </a>
          </h3>

          {/* Snippet */}
          <p className="result-snippet">
            {highlightText(result.snippet, query)}
          </p>

          {/* Metadata */}
          <div className="result-meta">
            {result.updated_at && (
              <span>
                Updated {formatDistanceToNow(new Date(result.updated_at), { addSuffix: true })}
              </span>
            )}
            {result.author && (
              <>
                <span>•</span>
                <span>by {result.author}</span>
              </>
            )}
            {result.tags && result.tags.length > 0 && (
              <>
                <span>•</span>
                <div className="flex items-center space-x-1">
                  {result.tags.slice(0, 3).map((tag, index) => (
                    <span
                      key={index}
                      className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                    >
                      {tag}
                    </span>
                  ))}
                  {result.tags.length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{result.tags.length - 3} more
                    </span>
                  )}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2 ml-4">
          <button
            onClick={() => navigator.clipboard.writeText(result.url)}
            className="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100"
            title="Copy link"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
      </div>
    </article>
  );
}

function SearchSkeleton() {
  return (
    <div className="space-y-6">
      {Array.from({ length: 5 }).map((_, index) => (
        <div key={index} className="result-card animate-pulse">
          <div className="flex items-center space-x-2 mb-2">
            <div className="skeleton w-16 h-4" />
            <div className="skeleton w-48 h-4" />
          </div>
          <div className="skeleton w-3/4 h-6 mb-2" />
          <div className="space-y-2">
            <div className="skeleton w-full h-4" />
            <div className="skeleton w-4/5 h-4" />
            <div className="skeleton w-2/3 h-4" />
          </div>
          <div className="flex items-center space-x-2 mt-3">
            <div className="skeleton w-24 h-3" />
            <div className="skeleton w-16 h-3" />
          </div>
        </div>
      ))}
    </div>
  );
}
