from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime, timedelta, timezone

from models import (
    Cabin, CabinCreate, CabinAssign, Session, Report, ReportGenerate,
    Alert, TelegramConfig, TelegramConfigUpdate, Stats, ActivityData,
    ActivityDataPoint, User, AuthSessionRequest, SessionData, CabinStatus,
    SimpleLoginRequest, SimpleLoginResponse
)
import auth
from auth import process_google_session, get_current_user, logout_user, create_session_cookie, clear_session_cookie, simple_login
import tracker_service as tracker_module
from tracker_service import tracker_service, active_connections

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Set database for auth and tracker modules
auth.set_database(db)
tracker_module.set_database(db)

# Create the main app without a prefix
app = FastAPI(title="Smart Cabin Monitoring API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============= Authentication Endpoints =============

@api_router.post("/auth/login")
async def login(request: SimpleLoginRequest, response: Response):
    """Simple username/password login."""
    result = await simple_login(request.username, request.password)
    
    # Create response and set cookie
    json_response = JSONResponse(content=result)
    create_session_cookie(json_response, result["session_token"])
    
    return json_response

@api_router.post("/auth/session", response_model=SessionData)
async def create_session(request: AuthSessionRequest, response: Response):
    """Process session_id from Google OAuth and create session."""
    session_data = await process_google_session(request.session_id)
    
    # Create response and set cookie
    json_response = JSONResponse(content=session_data.dict())
    create_session_cookie(json_response, session_data.session_token)
    
    return json_response

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return current_user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user and clear session."""
    session_token = request.cookies.get("session_token")
    if session_token:
        await logout_user(session_token)
    
    json_response = JSONResponse(content={"message": "Logged out successfully"})
    clear_session_cookie(json_response)
    
    return json_response

# ============= Stats & Dashboard Endpoints =============

@api_router.get("/stats", response_model=Stats)
async def get_stats(current_user: User = Depends(get_current_user)):
    """Get overall system statistics."""
    cabins = await db.cabins.find().to_list(1000)
    
    total_cabins = len(cabins)
    active_cabins = sum(1 for c in cabins if c.get("status") == "active")
    idle_cabins = sum(1 for c in cabins if c.get("status") == "idle")
    long_break_cabins = sum(1 for c in cabins if c.get("status") == "long_break")
    empty_cabins = sum(1 for c in cabins if c.get("status") == "empty")
    total_students = sum(1 for c in cabins if c.get("student_id"))
    
    # Calculate averages from sessions
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    
    daily_sessions = await db.sessions.find({
        "start_time": {"$gte": today}
    }).to_list(1000)
    
    weekly_sessions = await db.sessions.find({
        "start_time": {"$gte": week_ago}
    }).to_list(1000)
    
    avg_daily_hours = sum(s.get("duration", 0) for s in daily_sessions) / 3600 / max(total_students, 1)
    avg_weekly_hours = sum(s.get("duration", 0) for s in weekly_sessions) / 3600 / max(total_students, 1)
    
    return Stats(
        total_cabins=total_cabins,
        active_cabins=active_cabins,
        idle_cabins=idle_cabins,
        long_break_cabins=long_break_cabins,
        empty_cabins=empty_cabins,
        total_students=total_students,
        avg_daily_hours=round(avg_daily_hours, 1),
        avg_weekly_hours=round(avg_weekly_hours, 1)
    )

@api_router.get("/activity/daily")
async def get_daily_activity(current_user: User = Depends(get_current_user)):
    """Get daily activity chart data."""
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    sessions = await db.sessions.find({
        "start_time": {"$gte": today}
    }).to_list(1000)
    
    # Group by hour
    hourly_counts = {}
    for session in sessions:
        hour = session["start_time"].hour
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
    
    # Create response for 08:00 to 19:00
    data = []
    for hour in range(8, 20):
        data.append({
            "hour": f"{hour:02d}:00",
            "active": hourly_counts.get(hour, 0)
        })
    
    return data

@api_router.get("/activity/weekly")
async def get_weekly_activity(current_user: User = Depends(get_current_user)):
    """Get weekly activity chart data."""
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    
    sessions = await db.sessions.find({
        "start_time": {"$gte": week_ago}
    }).to_list(1000)
    
    # Group by day
    daily_hours = {}
    for session in sessions:
        day = session["start_time"].weekday()
        hours = session.get("duration", 0) / 3600
        daily_hours[day] = daily_hours.get(day, 0) + hours
    
    # Create response
    days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    data = []
    for i, day in enumerate(days):
        data.append({
            "day": day,
            "hours": int(daily_hours.get(i, 0))
        })
    
    return data

@api_router.get("/alerts", response_model=List[Alert])
async def get_alerts(current_user: User = Depends(get_current_user)):
    """Get active alerts."""
    alerts = await db.alerts.find({"resolved": False}).to_list(100)
    return [Alert(**alert) for alert in alerts]

# ============= Cabin Endpoints =============

@api_router.get("/cabins", response_model=List[Cabin])
async def get_cabins(current_user: User = Depends(get_current_user)):
    """Get all cabins with current status."""
    cabins = await db.cabins.find().sort("cabin_no", 1).to_list(1000)
    return [Cabin(**cabin) for cabin in cabins]

@api_router.get("/cabins/{cabin_no}", response_model=Cabin)
async def get_cabin(cabin_no: int, current_user: User = Depends(get_current_user)):
    """Get specific cabin details."""
    cabin = await db.cabins.find_one({"cabin_no": cabin_no})
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    return Cabin(**cabin)

@api_router.post("/cabins/{cabin_no}/assign", response_model=Cabin)
async def assign_student(cabin_no: int, data: CabinAssign, current_user: User = Depends(get_current_user)):
    """Assign student to cabin."""
    cabin = await db.cabins.find_one({"cabin_no": cabin_no})
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    
    update_data = {
        "student_id": data.student_id,
        "student_name": data.student_name,
        "updated_at": datetime.now(timezone.utc)
    }
    
    await db.cabins.update_one(
        {"cabin_no": cabin_no},
        {"$set": update_data}
    )
    
    updated_cabin = await db.cabins.find_one({"cabin_no": cabin_no})
    return Cabin(**updated_cabin)

@api_router.delete("/cabins/{cabin_no}/unassign")
async def unassign_student(cabin_no: int, current_user: User = Depends(get_current_user)):
    """Remove student from cabin."""
    cabin = await db.cabins.find_one({"cabin_no": cabin_no})
    if not cabin:
        raise HTTPException(status_code=404, detail="Cabin not found")
    
    await db.cabins.update_one(
        {"cabin_no": cabin_no},
        {"$set": {
            "student_id": None,
            "student_name": None,
            "status": "empty",
            "updated_at": datetime.now(timezone.utc)
        }}
    )
    
    return {"message": "Student unassigned successfully"}

# ============= Students Endpoints =============

@api_router.get("/students")
async def get_students(current_user: User = Depends(get_current_user)):
    """Get all students with their cabin assignments."""
    cabins = await db.cabins.find({"student_id": {"$ne": None}}).sort("cabin_no", 1).to_list(1000)
    
    students = []
    for cabin in cabins:
        # Get daily and weekly totals
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        
        daily_sessions = await db.sessions.find({
            "cabin_no": cabin["cabin_no"],
            "start_time": {"$gte": today}
        }).to_list(1000)
        
        weekly_sessions = await db.sessions.find({
            "cabin_no": cabin["cabin_no"],
            "start_time": {"$gte": week_ago}
        }).to_list(1000)
        
        daily_total = sum(s.get("duration", 0) for s in daily_sessions)
        weekly_total = sum(s.get("duration", 0) for s in weekly_sessions)
        
        students.append({
            **cabin,
            "daily_total": daily_total,
            "weekly_total": weekly_total
        })
    
    return students

# ============= Reports Endpoints =============

@api_router.get("/reports", response_model=List[Report])
async def get_reports(current_user: User = Depends(get_current_user)):
    """List all generated reports."""
    reports = await db.reports.find().sort("created_at", -1).to_list(100)
    return [Report(**report) for report in reports]

@api_router.post("/reports/generate")
async def generate_report(data: ReportGenerate, current_user: User = Depends(get_current_user)):
    """Generate new report (mock for now)."""
    # This would call the actual report generation logic
    # For now, just create a mock entry
    report = Report(
        id=f"report_{uuid.uuid4().hex}",
        type=data.type,
        date=data.date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        cabin_no=data.cabin_no,
        student_name="Mock Student",
        total_hours=6.5,
        sessions_count=3,
        filename=f"report_{data.type}_{datetime.now().strftime('%Y%m%d')}.pdf",
        file_path="/app/backend/reports/mock.pdf"
    )
    
    await db.reports.insert_one(report.dict(by_alias=True))
    return {"message": "Report generated successfully", "report": report}

# ============= Settings Endpoints =============

@api_router.get("/settings/telegram", response_model=TelegramConfig)
async def get_telegram_config(current_user: User = Depends(get_current_user)):
    """Get Telegram configuration."""
    config = await db.telegram_config.find_one({"_id": "telegram_config"})
    if not config:
        # Return default config
        return TelegramConfig(
            bot_token="",
            weekly_recipients=[],
            cabin_recipients={}
        )
    return TelegramConfig(**config)

@api_router.put("/settings/telegram", response_model=TelegramConfig)
async def update_telegram_config(data: TelegramConfigUpdate, current_user: User = Depends(get_current_user)):
    """Update Telegram configuration."""
    update_dict = {k: v for k, v in data.dict().items() if v is not None}
    update_dict["updated_at"] = datetime.now(timezone.utc)
    
    await db.telegram_config.update_one(
        {"_id": "telegram_config"},
        {"$set": update_dict},
        upsert=True
    )
    
    config = await db.telegram_config.find_one({"_id": "telegram_config"})
    return TelegramConfig(**config)

@api_router.get("/settings/cameras", response_model=List[Cabin])
async def get_camera_configs(current_user: User = Depends(get_current_user)):
    """Get camera configurations."""
    cabins = await db.cabins.find().sort("cabin_no", 1).to_list(1000)
    return [Cabin(**cabin) for cabin in cabins]

@api_router.post("/settings/cameras", response_model=Cabin)
async def add_camera(data: CabinCreate, current_user: User = Depends(get_current_user)):
    """Add new camera."""
    # Check if cabin already exists
    existing = await db.cabins.find_one({"cabin_no": data.cabin_no})
    if existing:
        raise HTTPException(status_code=400, detail="Cabin already exists")
    
    cabin = Cabin(
        id=f"cabin_{uuid.uuid4().hex}",
        cabin_no=data.cabin_no,
        camera_url=data.camera_url,
        status=CabinStatus.empty
    )
    
    await db.cabins.insert_one(cabin.dict(by_alias=True))
    return cabin

@api_router.delete("/settings/cameras/{cabin_no}")
async def remove_camera(cabin_no: int, current_user: User = Depends(get_current_user)):
    """Remove camera."""
    result = await db.cabins.delete_one({"cabin_no": cabin_no})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cabin not found")
    
    return {"message": "Camera removed successfully"}

# ============= WebSocket Endpoint =============

@api_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time cabin updates."""
    await websocket.accept()
    active_connections.add(websocket)
    
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for heartbeat
            await websocket.send_text('{"type":"pong"}')
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

# ============= Tracking Detection Endpoint =============

@api_router.post("/tracking/detection")
async def receive_detection(data: dict):
    """Receive detection data from tracking script."""
    cabin_no = data.get('cabin_no')
    detection_data = data.get('detection', {})
    
    if not cabin_no:
        raise HTTPException(status_code=400, detail="cabin_no required")
    
    await tracker_service.process_detection(cabin_no, detection_data)
    return {"status": "received"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Start tracker service on startup."""
    await tracker_service.start()
    logger.info("Application started - Tracker service running")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Stop tracker service and close database."""
    await tracker_service.stop()
    client.close()
    logger.info("Application shutdown complete")