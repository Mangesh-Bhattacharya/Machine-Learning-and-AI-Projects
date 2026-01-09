"""
FastAPI Server for MITRE ATT&CK Technique Prediction

Provides REST API endpoints for real-time attack technique classification.
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import time
from loguru import logger
import joblib
from pathlib import Path

from .schemas import (
    LogEntry,
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    TechniqueInfo,
    HealthResponse
)
from ..data.mitre_mapper import MITREMapper
from ..features.extractor import FeatureExtractor


# Initialize FastAPI app
app = FastAPI(
    title="MITRE ATT&CK Classifier API",
    description="Multi-label classification API for MITRE ATT&CK technique prediction",
    version="1.0.0"
)

# Global variables
model = None
feature_extractor = None
mitre_mapper = None
config = None


def load_model_and_dependencies(config_dict: Dict):
    """Load model and dependencies on startup."""
    global model, feature_extractor, mitre_mapper, config
    
    config = config_dict
    
    # Load MITRE mapper
    mitre_mapper = MITREMapper()
    
    # Load feature extractor
    feature_extractor = FeatureExtractor(config.get('features', {}))
    
    # Load trained model
    model_path = Path(config['models']['model_dir']) / f"{config['models']['default_model']}.pkl"
    model = joblib.load(model_path)
    
    logger.info("Model and dependencies loaded successfully")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Starting MITRE ATT&CK Classifier API")
    # Load config and model here
    # For now, this is a placeholder


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint."""
    return {
        "message": "MITRE ATT&CK Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "techniques": "/techniques",
            "health": "/health"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        timestamp=time.time()
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_techniques(request: PredictionRequest):
    """
    Predict MITRE ATT&CK techniques from a log entry.
    
    Args:
        request: Log entry to classify
        
    Returns:
        Predicted techniques with confidence scores
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    try:
        # Extract features from log entry
        features = feature_extractor.transform_single_log(request.log_entry.dict())
        
        # Predict
        prediction = model.predict([features])[0]
        probabilities = model.predict_proba([features])[0]
        
        # Get technique IDs
        technique_ids = feature_extractor.get_technique_labels()
        
        # Build response
        techniques = []
        confidence_threshold = config.get('mitre', {}).get('confidence_threshold', 0.3)
        
        for i, (pred, prob) in enumerate(zip(prediction, probabilities)):
            if pred == 1 and prob >= confidence_threshold:
                technique_id = technique_ids[i]
                technique_info = mitre_mapper.get_technique(technique_id)
                
                if technique_info:
                    techniques.append(TechniqueInfo(
                        id=technique_id,
                        name=technique_info['name'],
                        tactic=technique_info['tactic'],
                        confidence=float(prob),
                        description=technique_info['description']
                    ))
        
        # Sort by confidence
        techniques.sort(key=lambda x: x.confidence, reverse=True)
        
        # Limit number of techniques
        max_techniques = config.get('mitre', {}).get('max_techniques_per_prediction', 10)
        techniques = techniques[:max_techniques]
        
        prediction_time = time.time() - start_time
        
        return PredictionResponse(
            techniques=techniques,
            prediction_time=prediction_time
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict MITRE ATT&CK techniques for multiple log entries.
    
    Args:
        request: Batch of log entries
        
    Returns:
        Predictions for all log entries
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    try:
        predictions = []
        
        for log_entry in request.log_entries:
            # Reuse single prediction logic
            pred_request = PredictionRequest(log_entry=log_entry)
            pred_response = await predict_techniques(pred_request)
            predictions.append(pred_response)
        
        total_time = time.time() - start_time
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_samples=len(predictions),
            total_time=total_time
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/techniques", response_model=List[TechniqueInfo])
async def list_techniques(tactic: Optional[str] = None):
    """
    List all supported MITRE ATT&CK techniques.
    
    Args:
        tactic: Optional filter by tactic
        
    Returns:
        List of technique information
    """
    if mitre_mapper is None:
        raise HTTPException(status_code=503, detail="MITRE mapper not loaded")
    
    try:
        if tactic:
            techniques = mitre_mapper.get_techniques_by_tactic(tactic)
        else:
            techniques = [
                {"id": tid, **tdata}
                for tid, tdata in mitre_mapper.techniques.items()
            ]
        
        return [
            TechniqueInfo(
                id=t.get('id', ''),
                name=t['name'],
                tactic=t['tactic'],
                confidence=1.0,
                description=t['description']
            )
            for t in techniques
        ]
        
    except Exception as e:
        logger.error(f"Error listing techniques: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/techniques/{technique_id}", response_model=TechniqueInfo)
async def get_technique(technique_id: str):
    """
    Get details for a specific technique.
    
    Args:
        technique_id: MITRE ATT&CK technique ID
        
    Returns:
        Technique information
    """
    if mitre_mapper is None:
        raise HTTPException(status_code=503, detail="MITRE mapper not loaded")
    
    technique = mitre_mapper.get_technique(technique_id)
    
    if not technique:
        raise HTTPException(status_code=404, detail=f"Technique {technique_id} not found")
    
    return TechniqueInfo(
        id=technique_id,
        name=technique['name'],
        tactic=technique['tactic'],
        confidence=1.0,
        description=technique['description']
    )


@app.get("/metrics")
async def get_metrics():
    """Get model performance metrics."""
    # Placeholder for metrics
    return {
        "model": config['models']['default_model'] if config else "unknown",
        "requests_processed": 0,
        "average_latency": 0.0,
        "error_rate": 0.0
    }


def start_server(api_config: Dict):
    """
    Start the FastAPI server.
    
    Args:
        api_config: API configuration dictionary
    """
    import uvicorn
    
    # Load model and dependencies
    load_model_and_dependencies(api_config)
    
    # Start server
    uvicorn.run(
        app,
        host=api_config.get('host', '0.0.0.0'),
        port=api_config.get('port', 8000),
        workers=api_config.get('workers', 1),
        reload=api_config.get('reload', False)
    )


if __name__ == "__main__":
    # For development
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
