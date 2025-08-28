'use client';

import { SearchFilters } from '@/types';

interface FilterPanelProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
  resultCounts: Record<string, number>;
}

export function FilterPanel({ filters, onFiltersChange, resultCounts }: FilterPanelProps) {
  const handleSourceToggle = (source: 'forums' | 'docs' | 'tickets') => {
    const newSources = filters.sources.includes(source)
      ? filters.sources.filter(s => s !== source)
      : [...filters.sources, source];
    
    onFiltersChange({
      ...filters,
      sources: newSources,
    });
  };

  const handleTimeRangeChange = (timeRange: SearchFilters['timeRange']) => {
    onFiltersChange({
      ...filters,
      timeRange,
    });
  };

  const handleSortByChange = (sortBy: SearchFilters['sortBy']) => {
    onFiltersChange({
      ...filters,
      sortBy,
    });
  };

  return (
    <div className="space-y-6">
      {/* Sources */}
      <div>
        <h3 className="text-sm font-medium text-gray-900 mb-3">Sources</h3>
        <div className="space-y-2">
          {[
            { id: 'forums', label: 'Forums', icon: '💬' },
            { id: 'docs', label: 'Documentation', icon: '📚' },
            { id: 'tickets', label: 'Support Tickets', icon: '🎫' },
          ].map((source) => (
            <label
              key={source.id}
              className="flex items-center justify-between p-2 rounded-md hover:bg-gray-50 cursor-pointer"
            >
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={filters.sources.includes(source.id as any)}
                  onChange={() => handleSourceToggle(source.id as any)}
                  className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">
                  {source.icon} {source.label}
                </span>
              </div>
              <span className="text-xs text-gray-500">
                {resultCounts[source.id] || 0}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Time Range */}
      <div>
        <h3 className="text-sm font-medium text-gray-900 mb-3">Time Range</h3>
        <div className="space-y-2">
          {[
            { value: 'any', label: 'Any time' },
            { value: 'past_week', label: 'Past week' },
            { value: 'past_month', label: 'Past month' },
            { value: 'past_year', label: 'Past year' },
          ].map((option) => (
            <label
              key={option.value}
              className="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer"
            >
              <input
                type="radio"
                name="timeRange"
                value={option.value}
                checked={filters.timeRange === option.value}
                onChange={(e) => handleTimeRangeChange(e.target.value as any)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Sort By */}
      <div>
        <h3 className="text-sm font-medium text-gray-900 mb-3">Sort By</h3>
        <div className="space-y-2">
          {[
            { value: 'relevance', label: 'Relevance' },
            { value: 'date', label: 'Date' },
            { value: 'source', label: 'Source' },
          ].map((option) => (
            <label
              key={option.value}
              className="flex items-center space-x-3 p-2 rounded-md hover:bg-gray-50 cursor-pointer"
            >
              <input
                type="radio"
                name="sortBy"
                value={option.value}
                checked={filters.sortBy === option.value}
                onChange={(e) => handleSortByChange(e.target.value as any)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Reset Filters */}
      <div className="pt-4 border-t border-gray-200">
        <button
          onClick={() => onFiltersChange({
            sources: ['forums', 'docs', 'tickets'],
            timeRange: 'any',
            sortBy: 'relevance',
          })}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          Reset all filters
        </button>
      </div>
    </div>
  );
}
