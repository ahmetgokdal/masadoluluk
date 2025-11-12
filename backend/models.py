from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum

# Enums
class CabinStatus(str, Enum):
    active = "active"
    idle = "idle"
    long_break = "long_break"
    empty = "empty"

class AlertSeverity(str, Enum):
    warning = "warning"
    error = "error"
    critical = "critical"

class ReportType(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

# User Models
class User(BaseModel):
    id: str = Field(alias="_id")
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True

class UserSession(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True

# Cabin Models
class Cabin(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    cabin_no: int
    camera_url: str
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    status: CabinStatus = CabinStatus.empty
    current_session_start: Optional[datetime] = None
    current_session_duration: int = 0  # seconds
    last_activity: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True
        use_enum_values = True

class CabinCreate(BaseModel):
    cabin_no: int
    camera_url: str

class CabinAssign(BaseModel):
    student_id: str
    student_name: str

# Session Models
class Session(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    cabin_no: int
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: int = 0  # seconds
    detection_method: str = "manual"
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True

# Report Models
class Report(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    type: ReportType
    date: str
    cabin_no: Optional[int] = None
    student_name: Optional[str] = None
    total_hours: float
    sessions_count: int
    filename: str
    file_path: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True
        use_enum_values = True

class ReportGenerate(BaseModel):
    type: ReportType
    cabin_no: Optional[int] = None
    date: Optional[str] = None

# Alert Models
class Alert(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    type: str
    cabin_no: int
    student_name: Optional[str] = None
    message: str
    severity: AlertSeverity
    resolved: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True
        use_enum_values = True

# Settings Models
class TelegramConfig(BaseModel):
    id: str = Field(default="telegram_config", alias="_id")
    bot_token: str
    weekly_recipients: List[str] = []
    cabin_recipients: Dict[str, str] = {}
    updated_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    
    class Config:
        populate_by_name = True

class TelegramConfigUpdate(BaseModel):
    bot_token: Optional[str] = None
    weekly_recipients: Optional[List[str]] = None
    cabin_recipients: Optional[Dict[str, str]] = None

# Response Models
class Stats(BaseModel):
    total_cabins: int
    active_cabins: int
    idle_cabins: int
    long_break_cabins: int
    empty_cabins: int
    total_students: int
    avg_daily_hours: float
    avg_weekly_hours: float

class ActivityDataPoint(BaseModel):
    label: str  # hour for daily, day for weekly
    value: int  # active count or hours

class ActivityData(BaseModel):
    daily: List[ActivityDataPoint]
    weekly: List[ActivityDataPoint]

# Auth Response
class SessionData(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None
    session_token: str

class AuthSessionRequest(BaseModel):
    session_id: str
