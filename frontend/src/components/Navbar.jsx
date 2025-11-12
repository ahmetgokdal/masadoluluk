import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, FileText, Users, Settings, LogOut, Camera } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('session_token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/reports', label: 'Raporlar', icon: FileText },
    { path: '/students', label: 'Öğrenciler', icon: Users },
    { path: '/settings', label: 'Ayarlar', icon: Settings }
  ];

  return (
    <nav className="bg-white shadow-md border-b-4 border-b-orange-400">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center gap-3 group">
            <div className="p-2 bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg group-hover:shadow-lg transition-all duration-200">
              <Camera className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-800 hidden md:block">
              Akıllı Kabin Sistemi
            </span>
          </Link>

          {/* Nav Items */}
          <div className="flex items-center gap-2">
            {navItems.map(item => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md'
                      : 'text-gray-700 hover:bg-orange-50'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span className="hidden md:inline">{item.label}</span>
                </Link>
              );
            })}
            
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-gray-700 hover:bg-red-50 hover:text-red-600 transition-all duration-200 ml-2"
            >
              <LogOut className="h-5 w-5" />
              <span className="hidden md:inline">Çıkış</span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;