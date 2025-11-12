import React, { useState } from 'react';
import { Camera, User, Clock, Calendar } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { formatDuration, getStatusColor, getStatusLabel } from '../mock';

const CabinCard = ({ cabin }) => {
  const [showCamera, setShowCamera] = useState(false);
  const [imageError, setImageError] = useState(false);

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
            <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg">
              <div className="flex items-center gap-2 mb-1">
                <User className="h-4 w-4 text-orange-600" />
                <span className="font-semibold text-gray-800">{cabin.student_name}</span>
              </div>
              <p className="text-xs text-gray-600 ml-6">{cabin.student_id}</p>
            </div>
          ) : (
            <div className="mb-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 text-center">Öğrenci atanmamış</p>
            </div>
          )}

          {/* Session Info */}
          {cabin.status === 'active' && cabin.current_session_duration > 0 && (
            <div className="mb-3 flex items-center gap-2 text-sm">
              <Clock className="h-4 w-4 text-green-600" />
              <span className="text-gray-700">Oturum:</span>
              <span className="font-bold text-green-600">{formatDuration(cabin.current_session_duration)}</span>
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

      {/* Camera Modal */}
      <Dialog open={showCamera} onOpenChange={setShowCamera}>
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
                <img
                  src={cabin.camera_url}
                  alt={`Kabin ${cabin.cabin_no} kamera görüntüsü`}
                  className="w-full h-full object-cover"
                  onError={() => setImageError(true)}
                />
              ) : (
                <div className="w-full h-full flex flex-col items-center justify-center text-white">
                  <Camera className="h-16 w-16 mb-4 text-gray-500" />
                  <p className="text-gray-400">Kamera görüntüsü alınamadı</p>
                  <p className="text-sm text-gray-500 mt-2">{cabin.camera_url}</p>
                </div>
              )}
              {!imageError && (
                <div className="absolute top-4 right-4">
                  <div className="flex items-center gap-2 bg-black bg-opacity-70 px-3 py-2 rounded-full">
                    <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-white text-sm font-medium">CANLI</span>
                  </div>
                </div>
              )}
            </div>
            <div className="mt-4 flex justify-between items-center">
              <p className="text-sm text-gray-600">Son güncelleme: {new Date(cabin.last_activity).toLocaleString('tr-TR')}</p>
              <button
                onClick={() => setImageError(false)}
                className="px-4 py-2 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-lg hover:from-orange-600 hover:to-amber-600 transition-all duration-200 font-medium"
              >
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