import React from 'react';

interface TopicStatsCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  change?: number;
  changeLabel?: string;
  color?: 'blue' | 'green' | 'red' | 'purple' | 'yellow' | 'gray';
}

const TopicStatsCard: React.FC<TopicStatsCardProps> = ({
  title,
  value,
  icon,
  change,
  changeLabel,
  color = 'blue'
}) => {
  // Color mapping for different card types
  const colorClasses = {
    blue: 'bg-blue-50 border-blue-200 text-blue-800',
    green: 'bg-green-50 border-green-200 text-green-800',
    red: 'bg-red-50 border-red-200 text-red-800',
    purple: 'bg-purple-50 border-purple-200 text-purple-800',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    gray: 'bg-gray-50 border-gray-200 text-gray-800',
  };
  
  // Change indicator classes
  const getChangeClasses = () => {
    if (!change) return 'text-gray-500';
    return change > 0 ? 'text-green-600' : 'text-red-600';
  };
  
  return (
    <div className={`rounded-lg border p-4 ${colorClasses[color]}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-sm font-medium opacity-80">{title}</h3>
          <div className="mt-1 text-2xl font-semibold">{value}</div>
          
          {change !== undefined && (
            <div className={`text-xs mt-1 font-medium ${getChangeClasses()}`}>
              {change > 0 ? '↑' : '↓'} {Math.abs(change)}%
              {changeLabel && <span className="ml-1 opacity-75">{changeLabel}</span>}
            </div>
          )}
        </div>
        
        {icon && (
          <div className="opacity-75">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

export default TopicStatsCard;