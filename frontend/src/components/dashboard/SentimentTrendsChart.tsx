import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

interface SentimentTrendsProps {
  data: {
    dates: string[];
    sentiment: number[];
    counts: number[];
  };
  title?: string;
  isLoading?: boolean;
}

const SentimentTrendsChart: React.FC<SentimentTrendsProps> = ({ 
  data, 
  title = 'Sentiment Trends Over Time',
  isLoading = false
}) => {
  // Format data for the chart
  const formattedData = data.dates.map((date, index) => ({
    date: new Date(date).toLocaleDateString(),
    sentiment: data.sentiment[index],
    count: data.counts[index]
  }));

  // Determine if we have data
  const hasData = formattedData.length > 0;
  
  // Function to format the date tick labels
  const formatDateTick = (tickItem: string) => {
    // For shorter display we might want to only show month/day
    const date = new Date(tickItem);
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-4 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-64 bg-gray-100 rounded"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-medium text-gray-700 mb-4">{title}</h3>
      
      {hasData ? (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={formattedData}
              margin={{ top: 5, right: 30, left: 20, bottom: 30 }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                tickLine={false}
                minTickGap={15}
                tickFormatter={formatDateTick}
              />
              <YAxis 
                tick={{ fontSize: 12 }} 
                tickLine={false} 
                axisLine={false}
                domain={[-1, 1]}
                ticks={[-1, -0.5, 0, 0.5, 1]}
                tickFormatter={(value) => value.toFixed(1)}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#fff',
                  borderRadius: '8px',
                  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                  border: 'none',
                  padding: '10px'
                }}
                formatter={(value: number, name: string) => {
                  if (name === 'sentiment') {
                    return [value.toFixed(2), 'Sentiment Score'];
                  }
                  return [value, 'Articles'];
                }}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Legend verticalAlign="top" height={36} />
              <ReferenceLine y={0} stroke="#666" strokeDasharray="3 3" />
              <Line 
                type="monotone" 
                dataKey="sentiment" 
                stroke="#3B82F6" 
                strokeWidth={2}
                activeDot={{ r: 6 }}
                name="Sentiment"
                dot={{ strokeWidth: 2, r: 4 }}
              />
              <Line 
                type="monotone" 
                dataKey="count" 
                stroke="#8B5CF6" 
                strokeWidth={2} 
                name="Article Count"
                dot={{ strokeWidth: 2, r: 4 }}
                yAxisId="right"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="h-64 flex items-center justify-center">
          <p className="text-gray-500">No sentiment data available for this time period.</p>
        </div>
      )}
      
      <div className="mt-2 text-xs text-gray-500 text-center">
        Sentiment score ranges from -1 (negative) to 1 (positive)
      </div>
    </div>
  );
};

export default SentimentTrendsChart;