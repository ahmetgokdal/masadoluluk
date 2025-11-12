"""
Real-time cabin tracking service
Integrates smart_cabin_tracker_v4.py with the backend
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

# MongoDB database instance (will be set from server.py)
db = None

def set_database(database):
    """Set the database instance from server.py"""
    global db
    db = database

# WebSocket connections storage
active_connections: Set = set()

class TrackerService:
    """Service to manage cabin tracking and real-time updates"""
    
    def __init__(self):
        self.running = False
        self.tracking_task = None
        
    async def start(self):
        """Start the tracking service"""
        if self.running:
            return
        
        self.running = True
        self.tracking_task = asyncio.create_task(self._tracking_loop())
        logger.info("Tracker service started")
        
    async def stop(self):
        """Stop the tracking service"""
        self.running = False
        if self.tracking_task:
            self.tracking_task.cancel()
            try:
                await self.tracking_task
            except asyncio.CancelledError:
                pass
        logger.info("Tracker service stopped")
    
    async def _tracking_loop(self):
        """Main tracking loop - uses real camera detection"""
        from camera_detector import detector
        import asyncio
        
        while self.running:
            try:
                # Get all cabins
                cabins = await db.cabins.find().to_list(1000)
                
                # Update cabin statuses using REAL camera detection
                for cabin in cabins:
                    # Skip if no student assigned
                    if not cabin.get('student_id'):
                        continue
                    
                    # Analyze camera feed
                    camera_url = cabin.get('camera_url')
                    if not camera_url:
                        continue
                    
                    # Run detection in thread pool to avoid blocking
                    try:
                        result = await asyncio.get_event_loop().run_in_executor(
                            None, 
                            detector.analyze_cabin,
                            cabin['cabin_no'],
                            camera_url
                        )
                        
                        # Determine status based on detection
                        if result.get('error'):
                            # Camera offline
                            new_status = 'empty'
                        elif result['is_active']:
                            new_status = 'active'
                        elif result['brightness'] > 0.3:
                            # Lights on but no motion - idle
                            new_status = 'idle'
                        else:
                            # Lights off, no motion - long break or empty
                            new_status = 'long_break'
                        
                    except Exception as e:
                        logger.error(f"Detection error for cabin {cabin['cabin_no']}: {e}")
                        new_status = cabin.get('status', 'idle')  # Keep current status on error
                        
                        update_data = {
                            'status': new_status,
                            'last_activity': datetime.now(timezone.utc),
                            'updated_at': datetime.now(timezone.utc)
                        }
                        
                        if new_status == 'active':
                            if not cabin.get('current_session_start'):
                                update_data['current_session_start'] = datetime.now(timezone.utc)
                                update_data['current_session_duration'] = 0
                            else:
                                # Increment duration
                                duration = cabin.get('current_session_duration', 0)
                                update_data['current_session_duration'] = duration + 10
                        else:
                            # End session if moving from active to other
                            if cabin.get('status') == 'active' and cabin.get('current_session_start'):
                                duration = cabin.get('current_session_duration', 0)
                                if duration > 60:  # Minimum 1 minute
                                    # Create session record
                                    session = {
                                        'cabin_no': cabin['cabin_no'],
                                        'student_id': cabin.get('student_id'),
                                        'student_name': cabin.get('student_name'),
                                        'start_time': cabin.get('current_session_start'),
                                        'end_time': datetime.now(timezone.utc),
                                        'duration': duration,
                                        'detection_method': 'tracking',
                                        'created_at': datetime.now(timezone.utc)
                                    }
                                    await db.sessions.insert_one(session)
                            
                            update_data['current_session_start'] = None
                            update_data['current_session_duration'] = 0
                        
                        await db.cabins.update_one(
                            {'_id': cabin['_id']},
                            {'$set': update_data}
                        )
                        
                        # Broadcast update via WebSocket
                        await self.broadcast_cabin_update(cabin['cabin_no'])
                
                # Wait 5 seconds before next update (faster response)
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in tracking loop: {e}")
                await asyncio.sleep(5)
    
    async def broadcast_cabin_update(self, cabin_no: int):
        """Broadcast cabin update to all WebSocket connections"""
        try:
            cabin = await db.cabins.find_one({'cabin_no': cabin_no})
            if cabin:
                # Convert MongoDB document to dict
                cabin_data = {
                    'cabin_no': cabin['cabin_no'],
                    'status': cabin.get('status'),
                    'student_id': cabin.get('student_id'),
                    'student_name': cabin.get('student_name'),
                    'current_session_duration': cabin.get('current_session_duration', 0),
                    'last_activity': cabin.get('last_activity').isoformat() if cabin.get('last_activity') else None
                }
                
                # Send to all connected WebSocket clients
                import json
                message = json.dumps({
                    'type': 'cabin_update',
                    'data': cabin_data
                })
                
                # Remove disconnected clients
                disconnected = set()
                for connection in active_connections:
                    try:
                        await connection.send_text(message)
                    except:
                        disconnected.add(connection)
                
                active_connections.difference_update(disconnected)
        except Exception as e:
            logger.error(f"Error broadcasting update: {e}")
    
    async def process_detection(self, cabin_no: int, detection_data: Dict):
        """Process detection data from tracking script"""
        try:
            cabin = await db.cabins.find_one({'cabin_no': cabin_no})
            if not cabin:
                logger.warning(f"Cabin {cabin_no} not found")
                return
            
            # Update cabin status based on detection
            is_active = detection_data.get('is_active', False)
            detection_method = detection_data.get('method', 'unknown')
            
            status = 'active' if is_active else 'idle'
            
            update_data = {
                'status': status,
                'last_activity': datetime.now(timezone.utc),
                'updated_at': datetime.now(timezone.utc)
            }
            
            if is_active:
                if not cabin.get('current_session_start'):
                    update_data['current_session_start'] = datetime.now(timezone.utc)
                    update_data['current_session_duration'] = 0
                else:
                    # Calculate duration
                    start = cabin.get('current_session_start')
                    if start.tzinfo is None:
                        start = start.replace(tzinfo=timezone.utc)
                    duration = int((datetime.now(timezone.utc) - start).total_seconds())
                    update_data['current_session_duration'] = duration
            
            await db.cabins.update_one(
                {'cabin_no': cabin_no},
                {'$set': update_data}
            )
            
            # Broadcast update
            await self.broadcast_cabin_update(cabin_no)
            
        except Exception as e:
            logger.error(f"Error processing detection: {e}")

# Global tracker service instance
tracker_service = TrackerService()
