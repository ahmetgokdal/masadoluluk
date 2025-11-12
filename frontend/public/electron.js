const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('child_process');

let mainWindow;
let backendProcess;

// Backend'i başlat
function startBackend() {
  const backendPath = isDev 
    ? path.join(__dirname, '../../backend')
    : path.join(process.resourcesPath, 'backend');
  
  const pythonExe = isDev ? 'python3' : 'python';
  
  backendProcess = spawn(pythonExe, [
    '-m', 'uvicorn', 
    'server:app',
    '--host', '127.0.0.1',
    '--port', '8001'
  ], {
    cwd: backendPath,
    env: {
      ...process.env,
      MONGO_URL: 'mongodb://localhost:27017/',
      DB_NAME: 'cabin_system_db'
    }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
}

function createWindow() {
  // Pencereyi oluştur
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true
    },
    icon: path.join(__dirname, 'logo192.png'),
    title: 'Akıllı Kabin İzleme Sistemi',
    backgroundColor: '#fff5eb'
  });

  // Menu'yü kaldır (production için)
  if (!isDev) {
    Menu.setApplicationMenu(null);
  }

  // URL'i yükle
  const startURL = isDev
    ? 'http://localhost:3000'
    : `file://${path.join(__dirname, '../build/index.html')}`;

  mainWindow.loadURL(startURL);

  // DevTools (sadece development)
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Pencere başlığını güncelle
  mainWindow.on('page-title-updated', (event) => {
    event.preventDefault();
  });
}

// Uygulama hazır olduğunda
app.whenReady().then(() => {
  // Backend'i başlat
  startBackend();
  
  // Pencereyi oluştur
  setTimeout(createWindow, 3000); // Backend'in başlaması için bekle

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Tüm pencereler kapatıldığında
app.on('window-all-closed', () => {
  // macOS dışında uygulamayı kapat
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Uygulama kapanmadan önce
app.on('before-quit', () => {
  // Backend process'i durdur
  if (backendProcess) {
    backendProcess.kill();
  }
});

// Hata yönetimi
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
});

process.on('unhandledRejection', (error) => {
  console.error('Unhandled Rejection:', error);
});
