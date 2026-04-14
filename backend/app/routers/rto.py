# app/routers/rto.py
# All endpoints related to RTO offices
# Base URL: /api/v1/rto

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
import math
from app.db.database import get_db
from app.models.models import RTOOffice, State

router = APIRouter(
    prefix="/api/v1/rto",
    tags=["RTO Offices"]
)


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two GPS coordinates in kilometers
    Uses the Haversine formula — standard formula for GPS distance
    """
    R = 6371  # Earth's radius in kilometers
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c  # distance in km


@router.get("/nearest")
def get_nearest_rto(
    lat: float = Query(..., description="Your latitude e.g. 28.6139"),
    lng: float = Query(..., description="Your longitude e.g. 77.2090"),
    limit: int = Query(5, description="Number of nearest RTOs to return"),
    db: Session = Depends(get_db)
):
    """
    Find nearest RTO offices to a GPS location.
    Uses Haversine formula to calculate distances.
    
    Example: /rto/nearest?lat=28.6139&lng=77.2090&limit=3
    """
    # Get all RTO offices
    offices = db.query(RTOOffice).all()
    
    if not offices:
        raise HTTPException(status_code=404, detail="No RTO offices found")
    
    # Calculate distance for each office
    offices_with_distance = []
    for office in offices:
        distance = haversine_distance(lat, lng, office.latitude, office.longitude)
        offices_with_distance.append({
            "id": office.id,
            "name": office.name,
            "code": office.code,
            "address": office.address,
            "city": office.city,
            "state_id": office.state_id,
            "latitude": office.latitude,
            "longitude": office.longitude,
            "phone": office.phone,
            "working_hours": office.working_hours,
            "distance_km": round(distance, 2)
        })
    
    # Sort by distance (nearest first)
    offices_with_distance.sort(key=lambda x: x["distance_km"])
    
    # Return only the requested number
    nearest = offices_with_distance[:limit]
    
    return {
        "success": True,
        "count": len(nearest),
        "your_location": {"lat": lat, "lng": lng},
        "data": nearest
    }


@router.get("/state/{state_code}")
def get_rto_by_state(
    state_code: str,
    db: Session = Depends(get_db)
):
    """Get all RTO offices in a specific state"""
    state = db.query(State).filter(
        State.code == state_code.upper()
    ).first()
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"State not found: {state_code}"
        )
    
    offices = db.query(RTOOffice).filter(
        RTOOffice.state_id == state.id
    ).all()
    
    result = []
    for office in offices:
        result.append({
            "id": office.id,
            "name": office.name,
            "code": office.code,
            "address": office.address,
            "city": office.city,
            "latitude": office.latitude,
            "longitude": office.longitude,
            "phone": office.phone,
            "working_hours": office.working_hours
        })
    
    return {
        "success": True,
        "state": state.name,
        "count": len(result),
        "data": result
    }


@router.get("/all")
def get_all_rto(db: Session = Depends(get_db)):
    """Get all RTO offices"""
    offices = db.query(RTOOffice).all()
    
    result = []
    for office in offices:
        result.append({
            "id": office.id,
            "name": office.name,
            "code": office.code,
            "city": office.city,
            "state_id": office.state_id,
            "latitude": office.latitude,
            "longitude": office.longitude,
            "phone": office.phone,
            "working_hours": office.working_hours
        })
    
    return {
        "success": True,
        "count": len(result),
        "data": result
    }