import React, { useState } from 'react';

interface FilterOptions {
  sentiment: string[];
  bias: string[];
  sources: string[];
  dateRange: string;
}

interface ArticleFiltersProps {
  onFilterChange: (filters: FilterOptions) => void;
  availableSources: string[];
  initialFilters?: FilterOptions;
}

const ArticleFilters: React.FC<ArticleFiltersProps> = ({ 
  onFilterChange, 
  availableSources,
  initialFilters
}) => {
  const defaultFilters: FilterOptions = {
    sentiment: [],
    bias: [],
    sources: [],
    dateRange: 'all'
  };

  const [filters, setFilters] = useState<FilterOptions>(initialFilters || defaultFilters);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleFilterChange = (category: keyof FilterOptions, value: any) => {
    const newFilters = { ...filters };
    
    if (category === 'dateRange') {
      newFilters.dateRange = value;
    } else {
      // For array-based filters (sentiment, bias, sources)
      if (Array.isArray(newFilters[category])) {
        const index = newFilters[category].indexOf(value);
        if (index > -1) {
          // Remove if already selected
          newFilters[category] = newFilters[category].filter(item => item !== value);
        } else {
          // Add if not selected
          newFilters[category] = [...newFilters[category], value];
        }
      }
    }
    
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    setFilters(defaultFilters);
    onFilterChange(defaultFilters);
  };

  const activeFilterCount = 
    filters.sentiment.length + 
    filters.bias.length + 
    filters.sources.length + 
    (filters.dateRange !== 'all' ? 1 : 0);

  return (
    <div className="bg-white rounded-lg shadow mb-6">
      <div 
        className="px-6 py-4 border-b border-gray-200 flex justify-between items-center cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center">
          <h2 className="text-lg font-semibold text-gray-800">Filter Articles</h2>
          {activeFilterCount > 0 && (
            <span className="ml-2 bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              {activeFilterCount} active
            </span>
          )}
        </div>
        <svg 
          className={`w-5 h-5 transition-transform ${isExpanded ? 'transform rotate-180' : ''}`} 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
      
      {isExpanded && (
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Sentiment Filter */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Sentiment</h3>
              <div className="space-y-2">
                {['positive', 'neutral', 'negative'].map(sentiment => (
                  <label key={sentiment} className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                      checked={filters.sentiment.includes(sentiment)}
                      onChange={() => handleFilterChange('sentiment', sentiment)}
                    />
                    <span className="ml-2 text-sm text-gray-700 capitalize">{sentiment}</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* Bias Filter */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Political Perspective</h3>
              <div className="space-y-2">
                {['left-leaning', 'centrist', 'right-leaning'].map(bias => (
                  <label key={bias} className="flex items-center">
                    <input
                      type="checkbox"
                      className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                      checked={filters.bias.includes(bias)}
                      onChange={() => handleFilterChange('bias', bias)}
                    />
                    <span className="ml-2 text-sm text-gray-700 capitalize">{bias}</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* Date Range Filter */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Date Range</h3>
              <div className="space-y-2">
                {[
                  { value: 'all', label: 'All Time' },
                  { value: '7', label: 'Last 7 Days' },
                  { value: '30', label: 'Last 30 Days' },
                  { value: '90', label: 'Last 90 Days' }
                ].map(option => (
                  <label key={option.value} className="flex items-center">
                    <input
                      type="radio"
                      className="text-blue-600 focus:ring-blue-500 h-4 w-4"
                      checked={filters.dateRange === option.value}
                      onChange={() => handleFilterChange('dateRange', option.value)}
                    />
                    <span className="ml-2 text-sm text-gray-700">{option.label}</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* Sources Filter */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Sources</h3>
              {availableSources.length > 0 ? (
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {availableSources.map(source => (
                    <label key={source} className="flex items-center">
                      <input
                        type="checkbox"
                        className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                        checked={filters.sources.includes(source)}
                        onChange={() => handleFilterChange('sources', source)}
                      />
                      <span className="ml-2 text-sm text-gray-700">{source}</span>
                    </label>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No sources available</p>
              )}
            </div>
          </div>
          
          <div className="mt-6 flex justify-end">
            <button
              onClick={clearFilters}
              className="text-gray-700 bg-gray-100 hover:bg-gray-200 font-medium rounded-md text-sm px-5 py-2 mr-2"
            >
              Clear Filters
            </button>
            <button
              onClick={() => setIsExpanded(false)}
              className="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-md text-sm px-5 py-2"
            >
              Apply Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ArticleFilters;