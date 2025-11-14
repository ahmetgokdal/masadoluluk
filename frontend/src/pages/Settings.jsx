import React, { useState, useEffect } from 'react';
import { Camera, Send, Plus, Trash2, Save, Key } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Badge } from '../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import Navbar from '../components/Navbar';
import api from '../services/api';

const Settings = () => {
  const [telegramConfig, setTelegramConfig] = useState({ bot_token: '', weekly_recipients: [], cabin_recipients: {} });
  const [cameras, setCameras] = useState([]);
  const [newCamera, setNewCamera] = useState({ cabin_no: '', camera_url: '' });
  const [showAddCamera, setShowAddCamera] = useState(false);
  const [loading, setLoading] = useState(true);
  const [newChatId, setNewChatId] = useState('');
  const [testCamera, setTestCamera] = useState(null);
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const [telegramRes, camerasRes] = await Promise.all([
        api.settings.getTelegramConfig(),
        api.settings.getCameraConfigs()
      ]);
      setTelegramConfig(telegramRes.data);
      setCameras(camerasRes.data.slice(0, 10)); // Show first 10
      setLoading(false);
    } catch (error) {
      console.error('Error fetching settings:', error);
      setLoading(false);
    }
  };

  const handleSaveTelegram = async (e) => {
    e.preventDefault();
    try {
      await api.settings.updateTelegramConfig(telegramConfig);
      alert('Telegram ayarları kaydedildi!');
    } catch (error) {
      console.error('Error saving telegram config:', error);
      alert('Kaydetme başarısız. Lütfen tekrar deneyin.');
    }
  };

  const handleAddChatId = () => {
    const chatId = prompt('Chat ID girin:');
    if (chatId && chatId.trim()) {
      setTelegramConfig(prev => ({
        ...prev,
        weekly_recipients: [...prev.weekly_recipients, chatId.trim()]
      }));
    }
  };

  const handleRemoveChatId = (index) => {
    setTelegramConfig(prev => ({
      ...prev,
      weekly_recipients: prev.weekly_recipients.filter((_, i) => i !== index)
    }));
  };

  const handleAddCamera = async (e) => {
    e.preventDefault();
    try {
      await api.settings.addCamera({
        cabin_no: parseInt(newCamera.cabin_no),
        camera_url: newCamera.camera_url
      });
      setNewCamera({ cabin_no: '', camera_url: '' });
      setShowAddCamera(false);
      fetchSettings();
      alert('Kamera eklendi!');
    } catch (error) {
      console.error('Error adding camera:', error);
      alert('Kamera eklenemedi. Bu kabin numarası zaten kullanılıyor olabilir.');
    }
  };

  const handleUpdateCamera = async (cabinNo, newUrl) => {
    try {
      await api.put(`/settings/cameras/${cabinNo}`, {
        cabin_no: cabinNo,
        camera_url: newUrl
      });
      fetchSettings();
      alert('Kamera güncellendi!');
    } catch (error) {
      console.error('Error updating camera:', error);
      alert('Güncelleme başarısız.');
    }
  };

  const handleRemoveCamera = async (cabinNo) => {
    if (!window.confirm(`Kabin ${cabinNo} kamerasını kaldırmak istediğinizden emin misiniz?\n\nDikkat: Kabin ve tüm ilişkili veriler silinecektir.`)) {
      return;
    }
    try {
      await api.settings.removeCamera(cabinNo);
      fetchSettings();
      alert('Kamera kaldırıldı!');
    } catch (error) {
      console.error('Error removing camera:', error);
      alert('İşlem başarısız.');
    }
  };

  const handleResetAllCabins = async () => {
    const confirmText = 'TÜM KABİNLERİ SİL';
    const userInput = prompt(
      `⚠️ UYARI: Bu işlem TÜM kabinleri, oturumları ve uyarıları silecektir!\n\n` +
      `Bu işlem GERİ ALINAMAZ!\n\n` +
      `Devam etmek için "${confirmText}" yazın:`
    );
    
    if (userInput !== confirmText) {
      alert('İşlem iptal edildi.');
      return;
    }
    
    try {
      const response = await api.post('/settings/reset-all-cabins');
      alert(`✅ ${response.data.deleted.cabins} kabin ve ${response.data.deleted.sessions} oturum silindi!`);
      fetchSettings();
    } catch (error) {
      console.error('Error resetting cabins:', error);
      alert('İşlem başarısız: ' + (error.response?.data?.detail || error.message));
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
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Ayarlar</h1>
          <p className="text-gray-600">Sistem ayarlarını yapılandırın</p>
        </div>

        {/* Telegram Settings */}
        <Card className="bg-white shadow-lg mb-8">
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg">
                <Send className="h-6 w-6 text-white" />
              </div>
              <CardTitle className="text-xl font-bold text-gray-800">Telegram Ayarları</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSaveTelegram} className="space-y-6">
              {/* Bot Token */}
              <div>
                <Label htmlFor="bot_token" className="text-gray-700 font-medium flex items-center gap-2">
                  <Key className="h-4 w-4" />
                  Bot Token
                </Label>
                <Input
                  id="bot_token"
                  type="password"
                  value={telegramConfig.bot_token}
                  onChange={(e) => setTelegramConfig({ ...telegramConfig, bot_token: e.target.value })}
                  className="mt-2"
                  placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
                />
                <p className="text-xs text-gray-500 mt-1">
                  @BotFather'dan alınan bot token'ınızı girin
                </p>
              </div>

              {/* Weekly Recipients */}
              <div>
                <Label className="text-gray-700 font-medium">Haftalık Rapor Alıcıları</Label>
                <div className="mt-2 space-y-2">
                  {telegramConfig.weekly_recipients && telegramConfig.weekly_recipients.map((chatId, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <Input value={chatId} readOnly className="flex-1" />
                      <Button
                        type="button"
                        size="sm"
                        variant="outline"
                        onClick={() => handleRemoveChatId(index)}
                        className="border-red-300 text-red-600 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleAddChatId}
                    className="w-full border-orange-300 text-orange-600 hover:bg-orange-50"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Yeni Chat ID Ekle
                  </Button>
                </div>
              </div>

              {/* Cabin Recipients (Veli Bildirimleri) */}
              <div>
                <Label className="text-gray-700 font-medium">Kabin Bazlı Bildirimler (Veli)</Label>
                <p className="text-xs text-gray-500 mt-1 mb-3">Her kabin için özel Chat ID ekleyin. Veli sadece kendi çocuğunun raporlarını alır.</p>
                <div className="space-y-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      const cabinNo = prompt('Kabin Numarası:');
                      const chatId = prompt('Veli Chat ID:');
                      if (cabinNo && chatId) {
                        setTelegramConfig(prev => ({
                          ...prev,
                          cabin_recipients: {
                            ...prev.cabin_recipients,
                            [cabinNo]: chatId.trim()
                          }
                        }));
                      }
                    }}
                    className="w-full border-green-300 text-green-600 hover:bg-green-50"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Veli Chat ID Ekle
                  </Button>
                  
                  {telegramConfig.cabin_recipients && Object.keys(telegramConfig.cabin_recipients).length > 0 && (
                    <div className="mt-3 p-3 bg-gray-50 rounded-lg space-y-2">
                      {Object.entries(telegramConfig.cabin_recipients).map(([cabinNo, chatId]) => (
                        <div key={cabinNo} className="flex items-center justify-between p-2 bg-white rounded border">
                          <span className="text-sm">
                            <strong>Kabin {cabinNo}:</strong> {chatId}
                          </span>
                          <Button
                            type="button"
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setTelegramConfig(prev => {
                                const newRecipients = { ...prev.cabin_recipients };
                                delete newRecipients[cabinNo];
                                return { ...prev, cabin_recipients: newRecipients };
                              });
                            }}
                            className="border-red-300 text-red-600 hover:bg-red-50"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Schedule Info */}
              <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border border-blue-200">
                <h4 className="font-semibold text-gray-800 mb-2">Otomatik Gönderim Zamanları</h4>
                <div className="space-y-1 text-sm text-gray-700">
                  <p>📅 Günlük Raporlar: Her gün 21:30</p>
                  <p>📅 Haftalık Raporlar: Cumartesi 21:00</p>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white"
              >
                <Save className="h-4 w-4 mr-2" />
                Telegram Ayarlarını Kaydet
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Camera Settings */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg">
                  <Camera className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-800">Kamera Yapılandırması</CardTitle>
              </div>
              <Button
                onClick={() => setShowAddCamera(!showAddCamera)}
                className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white"
              >
                <Plus className="h-4 w-4 mr-2" />
                Kamera Ekle
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {/* Add Camera Form */}
            {showAddCamera && (
              <form onSubmit={handleAddCamera} className="mb-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
                <h4 className="font-semibold text-gray-800 mb-4">Yeni Kamera Ekle</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="cabin_no" className="text-gray-700 font-medium">
                      Kabin Numarası
                    </Label>
                    <Input
                      id="cabin_no"
                      type="number"
                      value={newCamera.cabin_no}
                      onChange={(e) => setNewCamera({ ...newCamera, cabin_no: e.target.value })}
                      placeholder="1"
                      className="mt-1"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="camera_url" className="text-gray-700 font-medium">
                      Kamera URL
                    </Label>
                    <Input
                      id="camera_url"
                      type="url"
                      value={newCamera.camera_url}
                      onChange={(e) => setNewCamera({ ...newCamera, camera_url: e.target.value })}
                      placeholder="http://192.168.3.210/capture"
                      className="mt-1"
                      required
                    />
                  </div>
                </div>
                <div className="flex gap-2 mt-4">
                  <Button type="submit" className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white">
                    <Save className="h-4 w-4 mr-2" />
                    Kaydet
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowAddCamera(false)}>
                    İptal
                  </Button>
                </div>
              </form>
            )}

            {/* Camera List */}
            <div className="space-y-3">
              {cameras.map(camera => (
                <div key={camera.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:border-orange-300 transition-colors duration-200">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-r from-orange-100 to-amber-100 rounded-lg">
                      <Camera className="h-6 w-6 text-orange-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800">Kabin {camera.cabin_no}</h4>
                      <p className="text-sm text-gray-600">{camera.camera_url}</p>
                      {camera.student_name && (
                        <Badge className="mt-1 bg-blue-100 text-blue-700 border-0 text-xs">
                          {camera.student_name}
                        </Badge>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button 
                      onClick={() => {
                        setTestCamera(camera);
                        setImageError(false);
                      }}
                      size="sm" 
                      variant="outline" 
                      className="border-orange-300 text-orange-600 hover:bg-orange-50"
                    >
                      <Camera className="h-3 w-3 mr-1" />
                      Test
                    </Button>
                    <Button 
                      onClick={() => {
                        const newUrl = prompt('Yeni kamera URL girin:', camera.camera_url);
                        if (newUrl && newUrl.trim() && newUrl !== camera.camera_url) {
                          handleUpdateCamera(camera.cabin_no, newUrl.trim());
                        }
                      }}
                      size="sm" 
                      variant="outline" 
                      className="border-blue-300 text-blue-600 hover:bg-blue-50"
                    >
                      <Save className="h-4 w-4" />
                    </Button>
                    <Button 
                      onClick={() => handleRemoveCamera(camera.cabin_no)}
                      size="sm" 
                      variant="outline" 
                      className="border-red-300 text-red-600 hover:bg-red-50"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg border border-orange-200">
              <p className="text-sm text-gray-700">
                💡 <strong>Not:</strong> Kamera URL'leri ESP32-CAM veya benzeri cihazlardan /capture endpoint'i olmalıdır.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Camera Test Dialog */}
      <Dialog open={testCamera !== null} onOpenChange={(open) => {
        if (!open) {
          setTestCamera(null);
          setImageError(false);
        }
      }}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle className="text-xl font-bold text-gray-800">
              Kamera Test - Kabin {testCamera?.cabin_no}
            </DialogTitle>
          </DialogHeader>
          {testCamera && (
            <div className="mt-4">
              <div className="mb-4 p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-lg">
                <p className="text-sm text-gray-600"><strong>URL:</strong> {testCamera.camera_url}</p>
                {testCamera.student_name && (
                  <p className="text-sm text-gray-600 mt-1"><strong>Öğrenci:</strong> {testCamera.student_name}</p>
                )}
              </div>
              
              <div className="relative bg-gray-900 rounded-lg overflow-hidden" style={{ aspectRatio: '16/9' }}>
                {!imageError ? (
                  <>
                    <img
                      key={testCamera.camera_url + Date.now()}
                      src={`${testCamera.camera_url}?t=${Date.now()}`}
                      alt={`Kabin ${testCamera.cabin_no} test görüntüsü`}
                      className="w-full h-full object-cover"
                      onError={() => setImageError(true)}
                      onLoad={() => console.log('✅ Kamera test başarılı')}
                    />
                    <div className="absolute top-4 right-4">
                      <div className="flex items-center gap-2 bg-green-600 bg-opacity-90 px-3 py-2 rounded-full">
                        <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                        <span className="text-white text-sm font-medium">TEST BAŞARILI</span>
                      </div>
                    </div>
                  </>
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center text-white p-8">
                    <div className="mb-6 p-4 bg-red-600 rounded-full">
                      <Camera className="h-12 w-12 text-white" />
                    </div>
                    <p className="text-xl font-bold text-red-400 mb-2">❌ TEST BAŞARISIZ</p>
                    <p className="text-gray-400 mb-4 text-center">Kamera görüntüsü alınamadı</p>
                    <div className="p-4 bg-gray-800 rounded-lg max-w-md text-left space-y-2">
                      <p className="text-sm text-yellow-400">⚠️ Kontrol Listesi:</p>
                      <ul className="text-xs text-gray-300 space-y-1 ml-4">
                        <li>• ESP32-CAM açık mı?</li>
                        <li>• WiFi bağlantısı var mı?</li>
                        <li>• URL doğru mu? <span className="text-orange-400">{testCamera.camera_url}</span></li>
                        <li>• Tarayıcıda URL'i test edin</li>
                        <li>• IP adresi değişmiş olabilir</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-4 flex justify-between items-center">
                <div className="flex gap-2">
                  {imageError ? (
                    <Badge className="bg-red-100 text-red-700 border-0">
                      Bağlantı Başarısız
                    </Badge>
                  ) : (
                    <Badge className="bg-green-100 text-green-700 border-0">
                      Bağlantı Başarılı
                    </Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <Button
                    onClick={() => {
                      setImageError(false);
                      // Force reload
                      const img = document.querySelector(`img[alt*="Kabin ${testCamera.cabin_no} test"]`);
                      if (img) img.src = `${testCamera.camera_url}?t=${Date.now()}`;
                    }}
                    className="bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-white"
                  >
                    <Camera className="h-4 w-4 mr-2" />
                    Tekrar Test Et
                  </Button>
                  <Button
                    onClick={() => {
                      window.open(testCamera.camera_url, '_blank');
                    }}
                    variant="outline"
                    className="border-blue-300 text-blue-600 hover:bg-blue-50"
                  >
                    Tarayıcıda Aç
                  </Button>
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Settings;