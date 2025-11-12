import React from 'react';
import { AlertTriangle, XCircle, AlertCircle } from 'lucide-react';
import { Card, CardContent } from './ui/card';

const AlertsPanel = ({ alerts }) => {
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <XCircle className="h-5 w-5 text-red-600" />;
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-orange-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200';
      case 'error':
        return 'bg-red-50 border-red-200';
      case 'warning':
        return 'bg-orange-50 border-orange-200';
      default:
        return 'bg-yellow-50 border-yellow-200';
    }
  };

  return (
    <Card className="bg-white shadow-md">
      <CardContent className="pt-6">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="h-5 w-5 text-orange-600" />
          <h3 className="text-lg font-semibold text-gray-800">Uyarılar ve Bildirimler</h3>
        </div>
        <div className="space-y-3">
          {alerts.map(alert => (
            <div
              key={alert.id}
              className={`p-4 rounded-lg border-2 ${getSeverityColor(alert.severity)} transition-all duration-200 hover:shadow-md`}
            >
              <div className="flex items-start gap-3">
                {getSeverityIcon(alert.severity)}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-semibold text-gray-800">
                      Kabin {alert.cabin_no} {alert.student_name && `- ${alert.student_name}`}
                    </h4>
                    <span className="text-xs text-gray-500">
                      {alert.created_at ? new Date(alert.created_at).toLocaleString('tr-TR', {
                        day: '2-digit',
                        month: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                      }) : 'Bilinmiyor'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-700">{alert.message}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default AlertsPanel;