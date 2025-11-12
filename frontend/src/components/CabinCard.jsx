import React, { useState } from 'react';
import { Camera, User, Clock, Calendar, Edit } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { formatDuration, getStatusColor, getStatusLabel } from '../mock';
import api from '../services/api';

const CabinCard = ({ cabin, onUpdate }) => {
  const [showCamera, setShowCamera] = useState(false);
  const [showAssignDialog, setShowAssignDialog] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [formData, setFormData] = useState({ student_id: '', student_name: '' });
  const [loading, setLoading] = useState(false);

  const getStatusBorderColor = (status) => {
    const colors = {
      active: 'border-l-green-500',
      idle: 'border-l-yellow-500',
      long_break: 'border-l-orange-500',
      empty: 'border-l-gray-400'
    };
    return colors[status] || colors.empty;
  };

  return (
    <>
      <Card className={`bg-white border-l-4 ${getStatusBorderColor(cabin.status)} shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1`}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg font-bold text-gray-800">
              Kabin {cabin.cabin_no}
            </CardTitle>
            <Badge className={`${getStatusColor(cabin.status)} border-0 font-medium`}>
              {getStatusLabel(cabin.status)}
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          {/* Student Info */}
          {cabin.student_id ? (
            <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg relative group">
              <div className="flex items-center gap-2 mb-1">
                <User className="h-4 w-4 text-orange-600" />
                <span className="font-semibold text-gray-800">{cabin.student_name}</span>
                <button
                  onClick={() => {
                    setFormData({ student_id: cabin.student_id, student_name: cabin.student_name });
                    setShowAssignDialog(true);
                  }}
                  className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-orange-200 rounded"
                >
                  <Edit className="h-3 w-3 text-orange-600" />
                </button>
              </div>
              <p className="text-xs text-gray-600 ml-6">{cabin.student_id}</p>
            </div>
          ) : (
            <button 
              onClick={() => {
                setFormData({ student_id: '', student_name: '' });
                setShowAssignDialog(true);
              }}
              className="mb-4 p-3 w-full bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border-2 border-dashed border-green-300 hover:border-green-500 transition-all"
            >
              <p className="text-sm text-green-600 font-medium text-center">+ Öğrenci Ata</p>
            </button>
          )}

          {/* Session Info */}
          {cabin.status === 'active' && cabin.current_session_duration > 0 && (
            <div className="mb-3 p-2 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-2 text-sm mb-1">
                <Clock className="h-4 w-4 text-green-600" />
                <span className="text-gray-700 font-medium">Şu Anki Çalışma Süresi:</span>
              </div>
              <div className="flex items-center justify-between ml-6">
                <span className="text-2xl font-bold text-green-600">{formatDuration(cabin.current_session_duration)}</span>
                <span className="text-xs text-green-600">⏱️ Aktif</span>
              </div>
            </div>
          )}

          {/* Daily Total */}
          {cabin.daily_total > 0 && (
            <div className="mb-3 flex items-center gap-2 text-sm">
              <Calendar className="h-4 w-4 text-blue-600" />
              <span className="text-gray-700">Bugün:</span>
              <span className="font-bold text-blue-600">{formatDuration(cabin.daily_total)}</span>
            </div>
          )}

          {/* Camera Button */}
          <button
            onClick={() => setShowCamera(true)}
            className="w-full mt-4 px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg hover:from-orange-600 hover:to-amber-600 transition-all duration-200 flex items-center justify-center gap-2 font-medium shadow-md hover:shadow-lg"
          >
            <Camera className="h-4 w-4" />
            Kamera Görüntüsü
          </button>
        </CardContent>
      </Card>

      {/* Assign Student Dialog */}
      <Dialog open={showAssignDialog} onOpenChange={setShowAssignDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-xl font-bold text-gray-800">
              Öğrenci Ata - Kabin {cabin.cabin_no}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={async (e) => {
            e.preventDefault();
            setLoading(true);
            try {
              await api.cabins.assign(cabin.cabin_no, formData);
              setShowAssignDialog(false);
              if (onUpdate) onUpdate();
              alert('Öğrenci başarıyla atandı!');
            } catch (error) {
              console.error('Error assigning student:', error);
              alert('Öğrenci atanamadı. Lütfen tekrar deneyin.');
            } finally {
              setLoading(false);
            }
          }} className="space-y-4 mt-4">
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
                disabled={loading}
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
                disabled={loading}
              />
            </div>
            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                disabled={loading}
                className="flex-1 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white"
              >
                {loading ? 'Kaydediliyor...' : 'Kaydet'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowAssignDialog(false)}
                className="flex-1"
                disabled={loading}
              >
                İptal
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Camera Modal */}
      <Dialog open={showCamera} onOpenChange={(open) => {
        setShowCamera(open);
        if (!open) setImageError(false);
      }}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold text-gray-800">
              Kabin {cabin.cabin_no} - Canlı Görüntü
            </DialogTitle>
          </DialogHeader>
          <div className="mt-4">
            {cabin.student_id && (
              <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg">
                <p className="font-semibold text-gray-800">{cabin.student_name}</p>
                <p className="text-sm text-gray-600">{cabin.student_id}</p>
              </div>
            )}
            <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
              {!imageError ? (
                <>
                  <img
                    key={cabin.camera_url + Date.now()}
                    src={`${cabin.camera_url}?t=${Date.now()}`}
                    alt={`Kabin ${cabin.cabin_no} kamera görüntüsü`}
                    className="w-full h-full object-cover"
                    onError={() => setImageError(true)}
                    onLoad={() => console.log('Kamera görüntüsü yüklendi')}
                  />
                  <div className="absolute top-4 right-4">
                    <div className="flex items-center gap-2 bg-black bg-opacity-70 px-3 py-2 rounded-full">
                      <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                      <span className="text-white text-sm font-medium">CANLI</span>
                    </div>
                  </div>
                </>
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-white p-6">
                  <Camera className="h-16 w-16 mb-4 text-gray-500" />
                  <p className="text-gray-400 mb-2">Kamera görüntüsü alınamadı</p>
                  <p className="text-sm text-gray-500 mt-2 text-center break-all">{cabin.camera_url}</p>
                  <p className="text-xs text-gray-600 mt-3">
                    ⚠️ ESP32-CAM cihazının açık ve ağa bağlı olduğundan emin olun
                  </p>
                </div>
              )}
            </div>
            <div className="mt-4 flex justify-between items-center">
              <p className="text-sm text-gray-600">
                {cabin.last_activity ? 
                  `Son güncelleme: ${new Date(cabin.last_activity).toLocaleString('tr-TR')}` : 
                  'Henüz aktivite yok'
                }
              </p>
              <button
                onClick={() => {
                  setImageError(false);
                  // Force image reload
                  const img = document.querySelector(`img[alt*="Kabin ${cabin.cabin_no}"]`);
                  if (img) img.src = `${cabin.camera_url}?t=${Date.now()}`;
                }}
                className="px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg hover:from-orange-600 hover:to-amber-600 transition-all duration-200 font-medium flex items-center gap-2"
              >
                <Camera className="h-4 w-4" />
                Yenile
              </button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default CabinCard;