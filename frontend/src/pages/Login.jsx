import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Camera, TrendingUp, Users, BarChart3 } from 'lucide-react';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const sessionToken = localStorage.getItem('session_token');
    if (sessionToken) {
      navigate('/dashboard');
      return;
    }

    // Check for session_id in URL hash (from Google OAuth redirect)
    const hash = location.hash;
    if (hash && hash.includes('session_id=')) {
      processSessionId(hash);
    }
  }, [navigate, location]);

  const processSessionId = async (hash) => {
    setLoading(true);
    try {
      // Extract session_id from hash
      const sessionId = hash.split('session_id=')[1]?.split('&')[0];
      
      if (!sessionId) {
        throw new Error('No session ID found');
      }

      // Process session with backend
      const response = await api.auth.processSession(sessionId);
      const { session_token, ...userData } = response.data;

      // Store session token and user data
      localStorage.setItem('session_token', session_token);
      localStorage.setItem('user', JSON.stringify(userData));

      // Clear hash and redirect to dashboard
      window.location.hash = '';
      navigate('/dashboard');
    } catch (error) {
      console.error('Session processing error:', error);
      alert('Giriş yapılırken bir hata oluştu. Lütfen tekrar deneyin.');
      setLoading(false);
    }
  };

  const handleLogin = () => {
    // Redirect to Emergent Auth with dashboard as redirect URL
    const redirectUrl = `${window.location.origin}/dashboard`;
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-100 via-yellow-100 to-amber-100 flex items-center justify-center p-4">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        {/* Left Side - Branding */}
        <div className="text-center lg:text-left">
          <div className="mb-8">
            <div className="inline-block p-4 bg-gradient-to-r from-orange-500 to-amber-500 rounded-2xl shadow-2xl mb-6">
              <Camera className="h-16 w-16 text-white" />
            </div>
            <h1 className="text-5xl font-bold text-gray-800 mb-4">
              Akıllı Kabin
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-amber-600">
                İzleme Sistemi
              </span>
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Gerçek zamanlı kabin aktivitesi ve öğrenci performans takibi
            </p>
          </div>

          {/* Features */}
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md">
              <div className="p-3 bg-gradient-to-r from-green-400 to-emerald-400 rounded-lg">
                <Camera className="h-6 w-6 text-white" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-800">50 Kabin İzleme</h3>
                <p className="text-sm text-gray-600">Canlı kamera görüntüsü</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md">
              <div className="p-3 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-lg">
                <BarChart3 className="h-6 w-6 text-white" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-800">Detaylı Raporlama</h3>
                <p className="text-sm text-gray-600">Günlük, haftalık, aylık raporlar</p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-white rounded-lg shadow-md">
              <div className="p-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-lg">
                <Users className="h-6 w-6 text-white" />
              </div>
              <div className="text-left">
                <h3 className="font-semibold text-gray-800">Öğrenci Yönetimi</h3>
                <p className="text-sm text-gray-600">Otomatik performans takibi</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Login Card */}
        <div className="flex items-center justify-center">
          <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Hoş Geldiniz</h2>
              <p className="text-gray-600">Sisteme giriş yapmak için Google hesabınızı kullanın</p>
            </div>

            <button
              onClick={handleLogin}
              className="w-full bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 text-white py-4 px-6 rounded-xl font-semibold text-lg shadow-lg hover:from-orange-600 hover:via-amber-600 hover:to-yellow-600 transition-all duration-300 transform hover:scale-105 hover:shadow-xl flex items-center justify-center gap-3"
            >
              <svg className="h-6 w-6" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Google ile Giriş Yap
            </button>

            <div className="mt-8 p-4 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border border-orange-200">
              <p className="text-xs text-gray-600 text-center">
                🔒 Güvenli Google OAuth ile kimlik doğrulama
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;