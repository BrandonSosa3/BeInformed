import React from 'react';
import { useSources } from '../context/SourceContext';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const { sources, loading, error } = useSources();

  return (
    <div className="container mx-auto px-4">
      {/* Keep your existing welcome header */}
      {/* ... */}

      {/* Error notification if API error */}
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p className="font-bold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Summary cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {/* Sources card */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Sources</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-bold text-blue-600">{sources.length}</p>
              <p className="text-sm text-gray-500">Total sources</p>
            </div>
            {/* Keep your existing icon */}
            {/* ... */}
          </div>
          <div className="mt-4">
            <Link to="/add-source" className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded text-center transition-colors">
              Add New Source
            </Link>
          </div>
        </div>

        {/* Keep your existing Analysis and Insights cards */}
        {/* ... */}
      </div>

      {/* Sources list */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Recent Sources</h2>
        
        {loading ? (
          <div className="flex justify-center py-6">
            <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        ) : sources.length > 0 ? (
          <div className="divide-y divide-gray-200">
            {sources.slice(0, 5).map(source => (
              <div key={source.id} className="py-4">
                <h3 className="text-lg font-medium text-gray-900">{source.title}</h3>
                <p className="text-sm text-gray-500 truncate">{source.url}</p>
                {source.description && (
                  <p className="mt-1 text-gray-600 line-clamp-2">{source.description}</p>
                )}
                <div className="mt-2 flex items-center">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {source.source_type}
                  </span>
                  {source.credibility_score !== null && (
                    <span className="ml-3 text-xs text-gray-500">
                      Credibility: {source.credibility_score.toFixed(1)}/10
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-500">No sources added yet.</p>
            <p className="text-gray-500 text-sm mt-1">Add your first source to get started.</p>
          </div>
        )}
        
        {sources.length > 5 && (
          <div className="mt-4 text-center">
            <Link to="/search" className="text-blue-600 hover:text-blue-800 font-medium">
              View all sources
            </Link>
          </div>
        )}
      </div>

      {/* Keep your existing Quick Actions section */}
      {/* ... */}
    </div>
  );
};

export default Dashboard;