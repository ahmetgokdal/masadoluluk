import React from 'react';

const ActivityChart = ({ data, type }) => {
  const maxValue = Math.max(...data.map(d => type === 'daily' ? d.active : d.hours));

  return (
    <div className="w-full">
      <div className="flex items-end justify-between gap-2 h-64">
        {data.map((item, index) => {
          const value = type === 'daily' ? item.active : item.hours;
          const height = (value / maxValue) * 100;
          const label = type === 'daily' ? item.hour : item.day;

          return (
            <div key={index} className="flex-1 flex flex-col items-center gap-2">
              <div className="relative w-full flex items-end justify-center" style={{ height: '200px' }}>
                <div
                  className="w-full bg-gradient-to-t from-orange-500 via-amber-500 to-yellow-400 rounded-t-lg transition-all duration-500 hover:from-orange-600 hover:via-amber-600 hover:to-yellow-500 cursor-pointer shadow-md"
                  style={{ height: `${height}%` }}
                  title={`${label}: ${value} ${type === 'daily' ? 'aktif kabin' : 'saat'}`}
                >
                  <div className="absolute -top-8 left-0 right-0 text-center">
                    <span className="text-sm font-bold text-gray-700">{value}</span>
                  </div>
                </div>
              </div>
              <span className="text-xs font-medium text-gray-600">{label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ActivityChart;