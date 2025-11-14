import React, { useState, useEffect } from 'react';
import { User, Edit, Trash2, Plus, Search } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Button } from '../components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { formatDuration } from '../mock';
import Navbar from '../components/Navbar';
import api from '../services/api';

const Students = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [selectedCabin, setSelectedCabin] = useState(null);
  const [formData, setFormData] = useState({ student_id: '', student_name: '' });
  const [assignedCabins, setAssignedCabins] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      // Get all cabins (both assigned and unassigned)
      const response = await api.cabins.getAll();
      setAssignedCabins(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching students:', error);
      setLoading(false);
    }
  };
  
  const filteredCabins = assignedCabins.filter(cabin => {
    const searchLower = searchTerm.toLowerCase();
    const studentName = cabin.student_name || '';
    const studentId = cabin.student_id || '';
    
    return studentName.toLowerCase().includes(searchLower) ||
           studentId.toLowerCase().includes(searchLower) ||
           cabin.cabin_no.toString().includes(searchTerm) ||
           (searchTerm === '' && !cabin.student_name); // Show unassigned if no search
  });

  const handleAssign = (cabin) => {
    setSelectedCabin(cabin);
    setFormData({
      student_id: cabin.student_id || '',
      student_name: cabin.student_name || ''
    });
    setShowAddDialog(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.cabins.assign(selectedCabin.cabin_no, formData);
      setShowAddDialog(false);
      fetchStudents();
    } catch (error) {
      console.error('Error assigning student:', error);
      alert('Öğrenci atanamadı. Lütfen tekrar deneyin.');
    }
  };

  const handleUnassign = async (cabinNo) => {
    if (!window.confirm('Öğrenci atamasını kaldırmak istediğinizden emin misiniz?')) {
      return;
    }
    try {
      await api.cabins.unassign(cabinNo);
      fetchStudents();
    } catch (error) {
      console.error('Error unassigning student:', error);
      alert('İşlem başarısız. Lütfen tekrar deneyin.');
    }
  };

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
      <Navbar />
      
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Öğrenci Yönetimi</h1>
          <p className="text-gray-600">Kabinlere atanmış öğrencileri yönetin ve performanslarını takip edin</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-white border-l-4 border-l-blue-500 shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Toplam Kabin</p>
                  <p className="text-3xl font-bold text-blue-600">{assignedCabins.length}</p>
                </div>
                <User className="h-10 w-10 text-blue-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-green-500 shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Atanmış Kabin</p>
                  <p className="text-3xl font-bold text-green-600">
                    {assignedCabins.filter(c => c.student_name).length}
                  </p>
                </div>
                <User className="h-10 w-10 text-green-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-orange-500 shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Boş Kabin</p>
                  <p className="text-3xl font-bold text-orange-600">
                    {assignedCabins.filter(c => !c.student_name).length}
                  </p>
                </div>
                <User className="h-10 w-10 text-orange-500" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-l-4 border-l-purple-500 shadow-md">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Aktif Çalışan</p>
                  <p className="text-3xl font-bold text-purple-600">
                    {assignedCabins.filter(c => c.status === 'active').length}
                  </p>
                </div>
                <User className="h-10 w-10 text-purple-500" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Search and Actions */}
        <div className="flex items-center justify-between mb-6">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <Input
              type="text"
              placeholder="Öğrenci adı, ID veya kabin numarası ara..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-white border-gray-300 focus:border-orange-500 focus:ring-orange-500"
            />
          </div>
        </div>

        {/* Students Table */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl font-bold text-gray-800">Atanmış Öğrenciler</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b-2 border-gray-200">
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Kabin</th>
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Öğrenci ID</th>
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Öğrenci Adı</th>
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Durum</th>
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Günlük Toplam</th>
                    <th className="text-left py-4 px-4 font-semibold text-gray-700">Haftalık Toplam</th>
                    <th className="text-right py-4 px-4 font-semibold text-gray-700">İşlemler</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCabins.map(cabin => {
                    const getStatusBadge = (status) => {
                      const configs = {
                        active: { bg: 'bg-green-100', text: 'text-green-700', label: 'Aktif' },
                        idle: { bg: 'bg-yellow-100', text: 'text-yellow-700', label: 'Boşta' },
                        long_break: { bg: 'bg-orange-100', text: 'text-orange-700', label: 'Uzun Mola' },
                        empty: { bg: 'bg-gray-100', text: 'text-gray-700', label: 'Boş' }
                      };
                      const config = configs[status] || configs.empty;
                      return (
                        <Badge className={`${config.bg} ${config.text} border-0`}>
                          {config.label}
                        </Badge>
                      );
                    };

                    return (
                      <tr key={cabin.id} className="border-b border-gray-100 hover:bg-orange-50 transition-colors duration-150">
                        <td className="py-4 px-4">
                          <span className="font-semibold text-gray-800">Kabin {cabin.cabin_no}</span>
                        </td>
                        <td className="py-4 px-4 text-gray-700">{cabin.student_id}</td>
                        <td className="py-4 px-4">
                          <div className="flex items-center gap-2">
                            <div className="w-8 h-8 bg-gradient-to-r from-orange-400 to-amber-400 rounded-full flex items-center justify-center text-white font-bold text-sm">
                              {cabin.student_name.charAt(0)}
                            </div>
                            <span className="font-medium text-gray-800">{cabin.student_name}</span>
                          </div>
                        </td>
                        <td className="py-4 px-4">{getStatusBadge(cabin.status)}</td>
                        <td className="py-4 px-4 font-semibold text-blue-600">
                          {formatDuration(cabin.daily_total)}
                        </td>
                        <td className="py-4 px-4 font-semibold text-purple-600">
                          {formatDuration(cabin.weekly_total)}
                        </td>
                        <td className="py-4 px-4">
                          <div className="flex items-center justify-end gap-2">
                            <Button
                              onClick={() => handleAssign(cabin)}
                              size="sm"
                              variant="outline"
                              className="border-orange-300 text-orange-600 hover:bg-orange-50"
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              onClick={() => handleUnassign(cabin.cabin_no)}
                              size="sm"
                              variant="outline"
                              className="border-red-300 text-red-600 hover:bg-red-50"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={showAddDialog} onOpenChange={setShowAddDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-xl font-bold text-gray-800">
              Öğrenci Ata - Kabin {selectedCabin?.cabin_no}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 mt-4">
            <div>
              <Label htmlFor="student_id" className="text-gray-700 font-medium">
                Öğrenci ID
              </Label>
              <Input
                id="student_id"
                value={formData.student_id}
                onChange={(e) => setFormData({ ...formData, student_id: e.target.value })}
                placeholder="örn: STU001"
                className="mt-1"
                required
              />
            </div>
            <div>
              <Label htmlFor="student_name" className="text-gray-700 font-medium">
                Öğrenci Adı
              </Label>
              <Input
                id="student_name"
                value={formData.student_name}
                onChange={(e) => setFormData({ ...formData, student_name: e.target.value })}
                placeholder="örn: Ahmet Yılmaz"
                className="mt-1"
                required
              />
            </div>
            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                className="flex-1 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white"
              >
                Kaydet
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowAddDialog(false)}
                className="flex-1"
              >
                İptal
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Students;