import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Users, Clock, TrendingUp, AlertTriangle, Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { formatDuration, getStatusColor, getStatusLabel } from '../mock';
import CabinCard from '../components/CabinCard';
import ActivityChart from '../components/ActivityChart';
import AlertsPanel from '../components/AlertsPanel';
import Navbar from '../components/Navbar';
import api from '../services/api';
import wsService from '../services/websocket';

const Dashboard = () => {
  const navigate = useNavigate();
  const [cabins, setCabins] = useState([]);
  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [dailyActivity, setDailyActivity] = useState([]);
  const [weeklyActivity, setWeeklyActivity] = useState([]);
  const [filterStatus, setFilterStatus] = useState('all');
  const [loading, setLoading] = useState(true);

  // Check authentication and setup WebSocket
  useEffect(() => {
    const sessionToken = localStorage.getItem('session_token');
    if (!sessionToken) {
      navigate('/login');
      return;
    }
    
    fetchData();
    
    // Connect WebSocket for real-time updates
    wsService.connect();
    wsService.subscribe('dashboard', handleWebSocketMessage);
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchData, 30000);
    
    return () => {
      clearInterval(interval);
      wsService.unsubscribe('dashboard');
    };
  }, [navigate]);

  const handleWebSocketMessage = (message) => {
    if (message.type === 'cabin_update') {
      const updatedCabin = message.data;
      setCabins(prev => prev.map(cabin => 
        cabin.cabin_no === updatedCabin.cabin_no 
          ? { ...cabin, ...updatedCabin } 
          : cabin
      ));
      
      // Recalculate stats
      fetchStats();
    }
  };

  const fetchStats = async () => {
    try {
      const statsRes = await api.stats.getStats();
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchData = async () => {
    try {
      const [cabinsRes, statsRes, alertsRes, dailyRes, weeklyRes] = await Promise.all([
        api.cabins.getAll(),
        api.stats.getStats(),
        api.stats.getAlerts(),
        api.stats.getDailyActivity(),
        api.stats.getWeeklyActivity()
      ]);

      setCabins(cabinsRes.data);
      setStats(statsRes.data);
      setAlerts(alertsRes.data);
      setDailyActivity(dailyRes.data);
      setWeeklyActivity(weeklyRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // If API fails, use mock data
      import('../mock').then(mockModule => {
        setCabins(mockModule.mockCabins);
        setStats(mockModule.mockStats);
        setAlerts(mockModule.mockAlerts);
        setDailyActivity(mockModule.mockActivityData.daily);
        setWeeklyActivity(mockModule.mockActivityData.weekly);
        setLoading(false);
      });
    }
  };

  const filteredCabins = filterStatus === 'all' 
    ? cabins 
    : cabins.filter(c => c.status === filterStatus);

  if (loading || !stats) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
      <Navbar />

      <div className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white border-l-4 border-l-green-500 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Aktif Kabinler</CardTitle>
              <Activity className="h-5 w-5 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">{stats.active_cabins}</div>
              <p className="text-xs text-gray-500 mt-2">Şu anda çalışıyor / {stats.total_cabins} toplam</p>
              <p className="text-xs text-green-600 mt-1 font-medium">🟢 Gerçek zamanlı</p>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-yellow-500 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Boşta</CardTitle>
              <Clock className="h-5 w-5 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-yellow-600">{stats.idle_cabins}</div>
              <p className="text-xs text-gray-500 mt-2">Kısa mola</p>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-orange-500 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Uzun Mola</CardTitle>
              <AlertTriangle className="h-5 w-5 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">{stats.long_break_cabins}</div>
              <p className="text-xs text-gray-500 mt-2">Dikkat gerekiyor</p>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-blue-500 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Toplam Öğrenci</CardTitle>
              <Users className="h-5 w-5 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">{stats.total_students}</div>
              <p className="text-xs text-gray-500 mt-2">Kayıtlı öğrenci</p>
            </CardContent>
          </Card>
        </div>

        {/* Alerts Panel */}
        {alerts.length > 0 && (
          <div className="mb-8">
            <AlertsPanel alerts={alerts} />
          </div>
        )}

        {/* Activity Chart */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card className="bg-white shadow-md">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-800">Günlük Aktivite</CardTitle>
            </CardHeader>
            <CardContent>
              <ActivityChart data={dailyActivity} type="daily" />
            </CardContent>
          </Card>

          <Card className="bg-white shadow-md">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-800">Haftalık Aktivite</CardTitle>
            </CardHeader>
            <CardContent>
              <ActivityChart data={weeklyActivity} type="weekly" />
            </CardContent>
          </Card>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-3 mb-6 flex-wrap">
          <button
            onClick={() => setFilterStatus('all')}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              filterStatus === 'all'
                ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            Tümü ({stats.total_cabins})
          </button>
          <button
            onClick={() => setFilterStatus('active')}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              filterStatus === 'active'
                ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            Aktif ({stats.active_cabins})
          </button>
          <button
            onClick={() => setFilterStatus('idle')}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              filterStatus === 'idle'
                ? 'bg-gradient-to-r from-yellow-500 to-amber-500 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            Boşta ({stats.idle_cabins})
          </button>
          <button
            onClick={() => setFilterStatus('long_break')}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              filterStatus === 'long_break'
                ? 'bg-gradient-to-r from-orange-600 to-red-500 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            Uzun Mola ({stats.long_break_cabins})
          </button>
          <button
            onClick={() => setFilterStatus('empty')}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              filterStatus === 'empty'
                ? 'bg-gradient-to-r from-gray-500 to-slate-500 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
            }`}
          >
            Boş ({stats.empty_cabins})
          </button>
        </div>

        {/* Cabins Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredCabins.map(cabin => (
            <CabinCard key={cabin.id} cabin={cabin} onUpdate={fetchData} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;