// Mock data for Smart Cabin Monitoring System

export const mockCabins = Array.from({ length: 50 }, (_, i) => {
  const cabinNo = i + 1;
  const statuses = ['active', 'idle', 'long_break', 'empty'];
  const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
  
  return {
    id: cabinNo,
    cabin_no: cabinNo,
    status: randomStatus,
    student_id: randomStatus !== 'empty' ? `STU${String(cabinNo).padStart(3, '0')}` : null,
    student_name: randomStatus !== 'empty' ? `Öğrenci ${cabinNo}` : null,
    current_session_start: randomStatus === 'active' ? new Date(Date.now() - Math.random() * 3600000).toISOString() : null,
    current_session_duration: randomStatus === 'active' ? Math.floor(Math.random() * 7200) : 0,
    last_session_end: randomStatus !== 'empty' && randomStatus !== 'active' ? new Date(Date.now() - Math.random() * 86400000).toISOString() : null,
    daily_total: Math.floor(Math.random() * 28800),
    weekly_total: Math.floor(Math.random() * 144000),
    camera_url: `http://192.168.3.${210 + Math.floor(cabinNo / 10)}/capture`,
    last_activity: new Date(Date.now() - Math.random() * 3600000).toISOString()
  };
});

export const mockStats = {
  total_cabins: 50,
  active_cabins: mockCabins.filter(c => c.status === 'active').length,
  idle_cabins: mockCabins.filter(c => c.status === 'idle').length,
  long_break_cabins: mockCabins.filter(c => c.status === 'long_break').length,
  empty_cabins: mockCabins.filter(c => c.status === 'empty').length,
  total_students: mockCabins.filter(c => c.student_id).length,
  avg_daily_hours: 4.5,
  avg_weekly_hours: 22.3
};

export const mockReports = [
  {
    id: 1,
    type: 'daily',
    date: new Date().toISOString().split('T')[0],
    cabin_no: 1,
    student_name: 'Öğrenci 1',
    total_hours: 6.5,
    sessions: 3,
    filename: 'report_daily_cabin1_2025-01-15.pdf'
  },
  {
    id: 2,
    type: 'weekly',
    date: new Date(Date.now() - 7 * 86400000).toISOString().split('T')[0],
    cabin_no: null,
    student_name: 'Tüm Öğrenciler',
    total_hours: 145.2,
    sessions: 78,
    filename: 'report_weekly_all_2025-01-08.pdf'
  },
  {
    id: 3,
    type: 'monthly',
    date: '2025-01-01',
    cabin_no: null,
    student_name: 'Tüm Öğrenciler',
    total_hours: 580.5,
    sessions: 312,
    filename: 'report_monthly_all_2025-01.pdf'
  }
];

export const mockActivityData = {
  daily: [
    { hour: '08:00', active: 12 },
    { hour: '09:00', active: 28 },
    { hour: '10:00', active: 35 },
    { hour: '11:00', active: 42 },
    { hour: '12:00', active: 25 },
    { hour: '13:00', active: 18 },
    { hour: '14:00', active: 38 },
    { hour: '15:00', active: 45 },
    { hour: '16:00', active: 40 },
    { hour: '17:00', active: 32 },
    { hour: '18:00', active: 22 },
    { hour: '19:00', active: 15 }
  ],
  weekly: [
    { day: 'Pzt', hours: 156 },
    { day: 'Sal', hours: 168 },
    { day: 'Çar', hours: 172 },
    { day: 'Per', hours: 165 },
    { day: 'Cum', hours: 158 },
    { day: 'Cmt', hours: 98 },
    { day: 'Paz', hours: 85 }
  ]
};

export const mockAlerts = [
  {
    id: 1,
    type: 'long_break',
    cabin_no: 5,
    student_name: 'Öğrenci 5',
    message: '2 saattir uzun molada',
    timestamp: new Date(Date.now() - 7200000).toISOString(),
    severity: 'warning'
  },
  {
    id: 2,
    type: 'no_data',
    cabin_no: 12,
    student_name: 'Öğrenci 12',
    message: '24 saattir veri yok',
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    severity: 'critical'
  },
  {
    id: 3,
    type: 'camera_offline',
    cabin_no: 23,
    student_name: null,
    message: 'Kamera bağlantısı kesildi',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    severity: 'error'
  }
];

export const mockTelegramConfig = {
  bot_token: '123456789:ABCdefGHIjklMNOpqrsTUVwxyz',
  weekly_recipients: ['123456789', '987654321'],
  cabin_recipients: {
    1: '111111111',
    2: '222222222',
    5: '555555555'
  }
};

// Helper function to format seconds to HH:MM
export const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
};

// Helper function to get status color
export const getStatusColor = (status) => {
  const colors = {
    active: 'text-green-600 bg-green-50',
    idle: 'text-yellow-600 bg-yellow-50',
    long_break: 'text-orange-600 bg-orange-50',
    empty: 'text-gray-600 bg-gray-50'
  };
  return colors[status] || colors.empty;
};

// Helper function to get status label
export const getStatusLabel = (status) => {
  const labels = {
    active: 'Aktif',
    idle: 'Boşta',
    long_break: 'Uzun Mola',
    empty: 'Boş'
  };
  return labels[status] || 'Bilinmiyor';
};