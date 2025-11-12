import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, TrendingUp, Users, BarChart3, LogIn } from 'lucide-react';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is already logged in
    const sessionToken = localStorage.getItem('session_token');
    if (sessionToken) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.auth.login(username, password);
      const { session_token, user } = response.data;

      // Store session token and user data
      localStorage.setItem('session_token', session_token);
      localStorage.setItem('user', JSON.stringify(user));

      // Redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      setError('Kullanıcı adı veya şifre hatalı');
      setLoading(false);
    }
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
                <h3 className="font-semibold text-gray-800">Kabin İzleme</h3>
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
              <p className="text-gray-600">Sisteme giriş yapmak için bilgilerinizi girin</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-6">
              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              <div>
                <Label htmlFor="username" className="text-gray-700 font-medium">
                  Kullanıcı Adı
                </Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="admin"
                  className="mt-2"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <Label htmlFor="password" className="text-gray-700 font-medium">
                  Şifre
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="mt-2"
                  required
                  disabled={loading}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 text-white py-4 px-6 rounded-xl font-semibold text-lg shadow-lg hover:from-orange-600 hover:via-amber-600 hover:to-yellow-600 transition-all duration-300 transform hover:scale-105 hover:shadow-xl flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Giriş Yapılıyor...
                  </>
                ) : (
                  <>
                    <LogIn className="h-6 w-6" />
                    Giriş Yap
                  </>
                )}
              </button>
            </form>

            <div className="mt-8 p-4 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border border-orange-200">
              <p className="text-xs text-gray-600 text-center">
                💡 Varsayılan: <strong>admin</strong> / <strong>admin123</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;