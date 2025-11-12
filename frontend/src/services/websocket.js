// WebSocket service for real-time cabin updates

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.reconnectDelay = 3000;
    this.listeners = new Map();
  }

  connect() {
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
    const wsUrl = BACKEND_URL.replace('https://', 'wss://').replace('http://', 'ws://');
    
    try {
      this.ws = new WebSocket(`${wsUrl}/api/ws`);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        
        // Send heartbeat every 30 seconds
        this.heartbeatInterval = setInterval(() => {
          if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ type: 'ping' }));
          }
        }, 30000);
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          // Notify all listeners
          this.listeners.forEach((callback) => {
            callback(data);
          });
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        if (this.heartbeatInterval) {
          clearInterval(this.heartbeatInterval);
        }
        this.reconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Error creating WebSocket:', error);
      this.reconnect();
    }
  }

  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);

    setTimeout(() => {
      this.connect();
    }, this.reconnectDelay);
  }

  disconnect() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.listeners.clear();
  }

  subscribe(id, callback) {
    this.listeners.set(id, callback);
  }

  unsubscribe(id) {
    this.listeners.delete(id);
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
}

// Singleton instance
const wsService = new WebSocketService();

export default wsService;
