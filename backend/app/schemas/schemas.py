# app/schemas/schemas.py
# Pydantic schemas define the shape of request and response data
# They automatically validate data and generate API documentation

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ─── ENUMS ────────────────────────────────────────────────────────────────────

class VehicleTypeSchema(str, Enum):
    two_wheeler = "two_wheeler"
    three_wheeler = "three_wheeler"
    four_wheeler = "four_wheeler"
    commercial = "commercial"
    heavy_vehicle = "heavy_vehicle"
    all_vehicles = "all_vehicles"


# ─── STATE SCHEMAS ────────────────────────────────────────────────────────────

class StateBase(BaseModel):
    name: str
    code: str
    has_amendments: bool = False
    capital: Optional[str] = None

class StateResponse(StateBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # allows reading from SQLAlchemy objects


# ─── LAW SCHEMAS ──────────────────────────────────────────────────────────────

class LawBase(BaseModel):
    section: str
    title: str
    description: str
    category: Optional[str] = None
    is_national: bool = True

class LawResponse(LawBase):
    id: int
    plain_language: Optional[str] = None
    state_id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── FINE SCHEMAS ─────────────────────────────────────────────────────────────

class FineResponse(BaseModel):
    id: int
    law_id: int
    state_id: Optional[int] = None
    vehicle_type: VehicleTypeSchema
    first_offence_amount: int
    repeat_offence_amount: Optional[int] = None
    imprisonment_days: Optional[int] = None
    mv_act_reference: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# ─── CHALLAN CALCULATOR SCHEMAS ───────────────────────────────────────────────

class ChalllanRequest(BaseModel):
    """Request body for challan calculation"""
    law_section: str          # e.g. "Section 185"
    state_code: str           # e.g. "DL"
    vehicle_type: VehicleTypeSchema
    is_repeat_offence: bool = False

class ChallanResponse(BaseModel):
    """Response from challan calculator"""
    law_section: str
    law_title: str
    state_name: str
    vehicle_type: str
    is_repeat_offence: bool
    fine_amount: int
    mv_act_reference: Optional[str] = None
    notes: Optional[str] = None


# ─── RTO SCHEMAS ──────────────────────────────────────────────────────────────

class RTOResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state_id: Optional[int] = None
    latitude: float
    longitude: float
    phone: Optional[str] = None
    email: Optional[str] = None
    working_hours: Optional[str] = None
    distance_km: Optional[float] = None  # calculated field

    class Config:
        from_attributes = True


# ─── API RESPONSE WRAPPERS ────────────────────────────────────────────────────

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = True
    message: str = "OK"
    data: Optional[dict] = None

class LawsListResponse(BaseModel):
    """Response for list of laws"""
    success: bool = True
    count: int
    data: List[LawResponse]

class RTOListResponse(BaseModel):
    """Response for list of RTO offices"""
    success: bool = True
    count: int
    data: List[RTOResponse]