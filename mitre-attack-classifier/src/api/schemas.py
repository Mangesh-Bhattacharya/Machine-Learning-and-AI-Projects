"""
Pydantic Schemas for API

Defines request and response models for the FastAPI endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class LogEntry(BaseModel):
    """Log entry input model."""
    action: Optional[str] = Field(None, description="Action performed")
    command: Optional[str] = Field(None, description="Command executed")
    process: Optional[str] = Field(None, description="Process name")
    source_ip: Optional[str] = Field(None, description="Source IP address")
    destination_ip: Optional[str] = Field(None, description="Destination IP address")
    user: Optional[str] = Field(None, description="Username")
    port: Optional[int] = Field(None, description="Port number")
    protocol: Optional[str] = Field(None, description="Network protocol")
    bytes_transferred: Optional[int] = Field(None, description="Bytes transferred")
    connection_count: Optional[int] = Field(None, description="Number of connections")
    failed_attempts: Optional[int] = Field(None, description="Failed attempt count")
    file_path: Optional[str] = Field(None, description="File path accessed")
    
    class Config:
        schema_extra = {
            "example": {
                "action": "command_execution",
                "command": "powershell.exe -enc SQBuAHYAbwBrAGUALQBNAGkAbQBpAGsAYQB0AHoA",
                "process": "powershell.exe",
                "source_ip": "192.168.1.100",
                "user": "admin",
                "port": 0,
                "protocol": "TCP"
            }
        }


class TechniqueInfo(BaseModel):
    """MITRE ATT&CK technique information."""
    id: str = Field(..., description="Technique ID (e.g., T1003)")
    name: str = Field(..., description="Technique name")
    tactic: str = Field(..., description="MITRE ATT&CK tactic")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    description: str = Field(..., description="Technique description")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "T1003",
                "name": "OS Credential Dumping",
                "tactic": "credential-access",
                "confidence": 0.95,
                "description": "Adversaries may attempt to dump credentials to obtain account login information."
            }
        }


class PredictionRequest(BaseModel):
    """Single prediction request."""
    log_entry: LogEntry = Field(..., description="Log entry to classify")
    
    class Config:
        schema_extra = {
            "example": {
                "log_entry": {
                    "action": "credential_dump",
                    "command": "mimikatz.exe sekurlsa::logonpasswords",
                    "process": "mimikatz.exe",
                    "source_ip": "192.168.1.50",
                    "user": "admin"
                }
            }
        }


class PredictionResponse(BaseModel):
    """Single prediction response."""
    techniques: List[TechniqueInfo] = Field(..., description="Predicted techniques")
    prediction_time: float = Field(..., description="Prediction time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "techniques": [
                    {
                        "id": "T1003",
                        "name": "OS Credential Dumping",
                        "tactic": "credential-access",
                        "confidence": 0.95,
                        "description": "Adversaries may attempt to dump credentials..."
                    }
                ],
                "prediction_time": 0.023
            }
        }


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    log_entries: List[LogEntry] = Field(..., description="List of log entries to classify")
    
    class Config:
        schema_extra = {
            "example": {
                "log_entries": [
                    {
                        "action": "command_execution",
                        "command": "powershell.exe",
                        "user": "admin"
                    },
                    {
                        "action": "lateral_movement",
                        "protocol": "SMB",
                        "port": 445
                    }
                ]
            }
        }


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    predictions: List[PredictionResponse] = Field(..., description="Predictions for each log entry")
    total_samples: int = Field(..., description="Total number of samples processed")
    total_time: float = Field(..., description="Total processing time in seconds")
    
    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "techniques": [{"id": "T1059", "name": "Command and Scripting Interpreter", "tactic": "execution", "confidence": 0.92, "description": "..."}],
                        "prediction_time": 0.015
                    }
                ],
                "total_samples": 2,
                "total_time": 0.035
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    timestamp: float = Field(..., description="Current timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "model_loaded": True,
                "timestamp": 1704758400.0
            }
        }


class ErrorResponse(BaseModel):
    """Error response."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        schema_extra = {
            "example": {
                "error": "Prediction failed",
                "detail": "Invalid input format"
            }
        }
