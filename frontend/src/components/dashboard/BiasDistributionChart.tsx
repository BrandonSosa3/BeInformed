import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface BiasDistributionProps {
  data: {
    leftLeaning: number;
    centrist: number;
    rightLeaning: number;
  };
  title?: string;
}

const BiasDistributionChart: React.FC<BiasDistributionProps> = ({ data, title = 'Political Perspective Distribution' }) => {
  // Format data for Recharts
  const chartData = [
    {
      name: 'Left-Leaning',
      value: data.leftLeaning,
      fill: '#3B82F6' // blue
    },
    {
      name: 'Centrist',
      value: data.centrist,
      fill: '#8B5CF6' // purple
    },
    {
      name: 'Right-Leaning',
      value: data.rightLeaning,
      fill: '#EF4444' // red
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-medium text-gray-700 mb-4">{title}</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis 
              dataKey="name" 
              tick={{ fontSize: 12 }}
              tickLine={false}
            />
            <YAxis 
              tick={{ fontSize: 12 }} 
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{ 
                backgroundColor: '#fff',
                borderRadius: '8px',
                boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                border: 'none',
                padding: '10px'
              }}
              cursor={{ fill: 'rgba(0, 0, 0, 0.05)' }}
              formatter={(value: number) => [`${value} articles`, 'Count']}
            />
            <Bar 
              dataKey="value" 
              radius={[4, 4, 0, 0]}
              animationDuration={1000}
              barSize={60}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default BiasDistributionChart;