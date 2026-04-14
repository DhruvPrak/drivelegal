# app/models/models.py
# This file defines ALL database tables as Python classes
# Each class = one table in PostgreSQL

from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, Enum, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.db.database import Base
import enum


# ─── ENUMS ────────────────────────────────────────────────────────────────────
# Enums are fixed lists of allowed values

class VehicleType(str, enum.Enum):
    """Types of vehicles for fine calculation"""
    two_wheeler = "two_wheeler"
    three_wheeler = "three_wheeler"
    four_wheeler = "four_wheeler"
    commercial = "commercial"
    heavy_vehicle = "heavy_vehicle"
    all_vehicles = "all_vehicles"


class OffenceType(str, enum.Enum):
    """Whether it's first or repeat offence"""
    first = "first"
    repeat = "repeat"


# ─── STATES TABLE ─────────────────────────────────────────────────────────────

class State(Base):
    """
    Stores all Indian states and Union Territories
    Example row: id=1, name="Delhi", code="DL", has_amendments=True
    """
    __tablename__ = "states"

    id = Column(Integer, primary_key=True, index=True)
    
    # Full name: "Maharashtra", "Tamil Nadu"
    name = Column(String(100), nullable=False, unique=True)
    
    # 2-letter code: "MH", "TN", "DL"
    code = Column(String(5), nullable=False, unique=True)
    
    # Whether this state has its own amendments to MV Act
    has_amendments = Column(Boolean, default=False)
    
    # Capital city name
    capital = Column(String(100))
    
    # Timestamps — automatically set
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships — one state has many jurisdictions, laws, fines
    jurisdictions = relationship("Jurisdiction", back_populates="state")
    fines = relationship("Fine", back_populates="state")

    def __repr__(self):
        return f"<State {self.name} ({self.code})>"


# ─── JURISDICTIONS TABLE ──────────────────────────────────────────────────────

class Jurisdiction(Base):
    """
    Stores cities/districts with their GPS boundaries
    PostGIS geometry column stores the actual boundary polygon
    Example: Delhi boundary = polygon of GPS coordinates
    """
    __tablename__ = "jurisdictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # City/district name: "Mumbai", "Chennai"
    name = Column(String(100), nullable=False)
    
    # Type: "city", "district", "state"
    jurisdiction_type = Column(String(50), default="city")
    
    # Foreign key — which state this jurisdiction belongs to
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    
    # PostGIS geometry — stores the GPS boundary polygon
    # MULTIPOLYGON type handles complex boundaries
    # SRID 4326 = standard GPS coordinate system (WGS84)
    boundary = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    
    # Center point for map display
    center_lat = Column(Float)
    center_lng = Column(Float)
    
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    state = relationship("State", back_populates="jurisdictions")
    rto_offices = relationship("RTOOffice", back_populates="jurisdiction")

    def __repr__(self):
        return f"<Jurisdiction {self.name}>"


# ─── LAWS TABLE ───────────────────────────────────────────────────────────────

class Law(Base):
    """
    Stores all traffic laws from Motor Vehicles Act + state amendments
    Each row is one law/section
    """
    __tablename__ = "laws"

    id = Column(Integer, primary_key=True, index=True)
    
    # MV Act section: "Section 112", "Section 177"
    section = Column(String(50), nullable=False)
    
    # Short title: "Over Speeding", "Drunk Driving"
    title = Column(String(200), nullable=False)
    
    # Full legal text (original)
    description = Column(Text, nullable=False)
    
    # AI-simplified plain English version (added in Day 11)
    plain_language = Column(Text)
    
    # Category for filtering
    category = Column(String(100))
    # Examples: "Speed", "Documents", "Safety", "Drunk Driving"
    
    # Is this a national law or state-specific?
    is_national = Column(Boolean, default=True)
    
    # If state-specific, which state?
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    
    # AI embedding vector for RAG chat (added in Day 22)
    # 1536 dimensions for Claude embeddings
    embedding = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    fines = relationship("Fine", back_populates="law")

    def __repr__(self):
        return f"<Law {self.section}: {self.title}>"


# ─── FINES TABLE ──────────────────────────────────────────────────────────────

class Fine(Base):
    """
    Stores fine amounts for each violation by state and vehicle type
    This powers the Challan Calculator feature
    
    Example row:
    - law: Section 112 (Speeding)
    - state: Delhi
    - vehicle: two_wheeler
    - first offence: ₹1000
    - repeat offence: ₹2000
    """
    __tablename__ = "fines"

    id = Column(Integer, primary_key=True, index=True)
    
    # Which law this fine is for
    law_id = Column(Integer, ForeignKey("laws.id"), nullable=False)
    
    # Which state this fine applies in
    # NULL = applies to all states (national default)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    
    # Which vehicle type
    vehicle_type = Column(
        Enum(VehicleType),
        default=VehicleType.all_vehicles,
        nullable=False
    )
    
    # Fine amounts in Indian Rupees
    first_offence_amount = Column(Integer, nullable=False)   # ₹ first time
    repeat_offence_amount = Column(Integer, nullable=True)   # ₹ repeat
    
    # Some fines have imprisonment too
    imprisonment_days = Column(Integer, nullable=True)
    
    # MV Act reference for legal accuracy
    mv_act_reference = Column(String(100))
    
    # Additional notes
    notes = Column(Text)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    law = relationship("Law", back_populates="fines")
    state = relationship("State", back_populates="fines")

    def __repr__(self):
        return f"<Fine law={self.law_id} state={self.state_id} ₹{self.first_offence_amount}>"


# ─── RTO OFFICES TABLE ────────────────────────────────────────────────────────

class RTOOffice(Base):
    """
    Stores RTO office information with GPS coordinates
    Powers the "Find Nearest RTO" feature
    """
    __tablename__ = "rto_offices"

    id = Column(Integer, primary_key=True, index=True)
    
    # Office name: "RTO Delhi Central", "RTO Mumbai West"
    name = Column(String(200), nullable=False)
    
    # RTO code: "DL-01", "MH-02"
    code = Column(String(20))
    
    # Full address
    address = Column(Text)
    
    # City and state
    city = Column(String(100))
    state_id = Column(Integer, ForeignKey("states.id"))
    
    # GPS coordinates for distance calculation
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # PostGIS point — for advanced geo queries
    location = Column(Geometry(geometry_type='POINT', srid=4326))
    
    # Contact information
    phone = Column(String(20))
    email = Column(String(100))
    website = Column(String(200))
    
    # Office hours
    working_hours = Column(String(100), default="Mon-Sat 10AM-5PM")
    
    # Which jurisdiction this RTO serves
    jurisdiction_id = Column(Integer, ForeignKey("jurisdictions.id"), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    jurisdiction = relationship("Jurisdiction", back_populates="rto_offices")

    def __repr__(self):
        return f"<RTOOffice {self.code}: {self.name}>"