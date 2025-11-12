import React, { useState, useEffect } from 'react';
import { FileText, Download, Calendar, Send, Filter } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import Navbar from '../components/Navbar';
import api from '../services/api';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [filterType, setFilterType] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await api.reports.getAll();
      setReports(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setLoading(false);
    }
  };

  const handleGenerateReport = async (type) => {
    try {
      await api.reports.generate({ type });
      fetchReports();
      alert('Rapor oluşturuldu!');
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Rapor oluşturulamadı. Lütfen tekrar deneyin.');
    }
  };

  const filteredReports = filterType === 'all' 
    ? reports 
    : reports.filter(r => r.type === filterType);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="w-16 h-16 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-gray-600">Yükleniyor...</p>
          </div>
        </div>
      </div>
    );
  }

  const getTypeColor = (type) => {
    switch (type) {
      case 'daily':
        return 'bg-green-100 text-green-700';
      case 'weekly':
        return 'bg-blue-100 text-blue-700';
      case 'monthly':
        return 'bg-purple-100 text-purple-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getTypeLabel = (type) => {
    switch (type) {
      case 'daily':
        return 'Günlük';
      case 'weekly':
        return 'Haftalık';
      case 'monthly':
        return 'Aylık';
      default:
        return 'Bilinmiyor';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
      <Navbar />
      
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Raporlar</h1>
          <p className="text-gray-600">Kabin aktivite raporlarını görüntüleyin ve indirin</p>
        </div>

        {/* Generate Report Section */}
        <Card className="bg-white shadow-lg mb-8 border-l-4 border-l-orange-500">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-gray-800">Yeni Rapor Oluştur</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button 
                onClick={() => handleGenerateReport('daily')}
                className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border-2 border-green-200 hover:border-green-400 transition-all duration-200 hover:shadow-md"
              >
                <Calendar className="h-8 w-8 text-green-600 mb-3 mx-auto" />
                <h3 className="font-semibold text-gray-800 mb-2">Günlük Rapor</h3>
                <p className="text-sm text-gray-600">Bugünün aktivitelerini raporla</p>
              </button>

              <button 
                onClick={() => handleGenerateReport('weekly')}
                className="p-6 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg border-2 border-blue-200 hover:border-blue-400 transition-all duration-200 hover:shadow-md"
              >
                <Calendar className="h-8 w-8 text-blue-600 mb-3 mx-auto" />
                <h3 className="font-semibold text-gray-800 mb-2">Haftalık Rapor</h3>
                <p className="text-sm text-gray-600">Bu haftanın özetini oluştur</p>
              </button>

              <button 
                onClick={() => handleGenerateReport('monthly')}
                className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border-2 border-purple-200 hover:border-purple-400 transition-all duration-200 hover:shadow-md"
              >
                <Calendar className="h-8 w-8 text-purple-600 mb-3 mx-auto" />
                <h3 className="font-semibold text-gray-800 mb-2">Aylık Rapor</h3>
                <p className="text-sm text-gray-600">Aylık performans raporu</p>
              </button>
            </div>

            <div className="mt-6 p-4 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border border-orange-200 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Send className="h-5 w-5 text-orange-600" />
                <span className="text-sm font-medium text-gray-700">
                  Otomatik Telegram Gönderimi Aktif
                </span>
              </div>
              <Badge className="bg-green-100 text-green-700 border-0">
                Günlük 21:30 | Haftalık Cmt 21:00
              </Badge>
            </div>
          </CardContent>
        </Card>

        {/* Filter */}
        <div className="flex items-center gap-4 mb-6">
          <Filter className="h-5 w-5 text-gray-600" />
          <div className="flex gap-2 flex-wrap">
            <button
              onClick={() => setFilterType('all')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                filterType === 'all'
                  ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
              }`}
            >
              Tümü
            </button>
            <button
              onClick={() => setFilterType('daily')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                filterType === 'daily'
                  ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
              }`}
            >
              Günlük
            </button>
            <button
              onClick={() => setFilterType('weekly')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                filterType === 'weekly'
                  ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
              }`}
            >
              Haftalık
            </button>
            <button
              onClick={() => setFilterType('monthly')}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                filterType === 'monthly'
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
              }
            >`}
            >
              Aylık
            </button>
          </div>
        </div>

        {/* Reports List */}
        <div className="grid grid-cols-1 gap-4">
          {filteredReports.map(report => (
            <Card key={report.id} className="bg-white shadow-md hover:shadow-lg transition-all duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-r from-orange-100 to-amber-100 rounded-lg">
                      <FileText className="h-6 w-6 text-orange-600" />
                    </div>
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-semibold text-lg text-gray-800">{report.student_name}</h3>
                        <Badge className={getTypeColor(report.type)}>
                          {getTypeLabel(report.type)}
                        </Badge>
                        {report.cabin_no && (
                          <Badge className="bg-gray-100 text-gray-700">
                            Kabin {report.cabin_no}
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">{report.filename}</p>
                      <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                        <span>{report.date}</span>
                        <span>•</span>
                        <span>{report.total_hours} saat</span>
                        <span>•</span>
                        <span>{report.sessions} oturum</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button className="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white">
                      <Download className="h-4 w-4 mr-2" />
                      İndir
                    </Button>
                    <Button variant="outline" className="border-orange-300 text-orange-600 hover:bg-orange-50">
                      <Send className="h-4 w-4 mr-2" />
                      Gönder
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Reports;