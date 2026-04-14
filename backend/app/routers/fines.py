# app/routers/fines.py
# All endpoints related to fines and challan calculator
# Base URL: /api/v1/fines

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.models.models import Fine, Law, State, VehicleType
from app.schemas.schemas import ChallanResponse

router = APIRouter(
    prefix="/api/v1/fines",
    tags=["Challan Calculator"]
)


@router.get("/calculate")
def calculate_challan(
    section: str = Query(..., description="MV Act section e.g. Section 185"),
    state_code: str = Query(..., description="State code e.g. DL, MH, KA"),
    vehicle_type: str = Query(..., description="Vehicle type e.g. two_wheeler"),
    is_repeat: bool = Query(False, description="Is this a repeat offence?"),
    db: Session = Depends(get_db)
):
    """
    Calculate exact challan amount for a violation.
    
    Example: /fines/calculate?section=Section 185&state_code=DL&vehicle_type=two_wheeler&is_repeat=false
    
    Logic:
    1. First look for state-specific fine
    2. If not found, fall back to national fine
    3. Return exact amount with legal reference
    """
    # Step 1 — Find the law
    law = db.query(Law).filter(
        Law.section.ilike(f"%{section}%")
    ).first()
    
    if not law:
        raise HTTPException(
            status_code=404,
            detail=f"Law not found for section: {section}"
        )
    
    # Step 2 — Find the state
    state = db.query(State).filter(
        State.code == state_code.upper()
    ).first()
    
    if not state:
        raise HTTPException(
            status_code=404,
            detail=f"State not found: {state_code}"
        )
    
    # Step 3 — Try to find vehicle type enum
    try:
        vtype = VehicleType(vehicle_type)
    except ValueError:
        vtype = VehicleType.all_vehicles
    
    # Step 4 — Look for state-specific fine first
    fine = db.query(Fine).filter(
        Fine.law_id == law.id,
        Fine.state_id == state.id,
        Fine.vehicle_type.in_([vtype, VehicleType.all_vehicles])
    ).first()
    
    # Step 5 — Fall back to national fine if no state fine
    if not fine:
        fine = db.query(Fine).filter(
            Fine.law_id == law.id,
            Fine.state_id == None,
            Fine.vehicle_type.in_([vtype, VehicleType.all_vehicles])
        ).first()
    
    if not fine:
        raise HTTPException(
            status_code=404,
            detail=f"No fine found for {section} in {state_code} for {vehicle_type}"
        )
    
    # Step 6 — Calculate final amount
    if is_repeat and fine.repeat_offence_amount:
        amount = fine.repeat_offence_amount
    else:
        amount = fine.first_offence_amount
    
    return {
        "success": True,
        "data": {
            "law_section": law.section,
            "law_title": law.title,
            "state_name": state.name,
            "state_code": state.code,
            "vehicle_type": vehicle_type,
            "is_repeat_offence": is_repeat,
            "fine_amount": amount,
            "first_offence_amount": fine.first_offence_amount,
            "repeat_offence_amount": fine.repeat_offence_amount,
            "mv_act_reference": fine.mv_act_reference,
            "imprisonment_days": fine.imprisonment_days,
            "plain_language": law.plain_language
        }
    }


@router.get("/all")
def get_all_fines(
    state_code: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all fines, optionally filtered by state"""
    query = db.query(Fine)
    
    if state_code:
        state = db.query(State).filter(
            State.code == state_code.upper()
        ).first()
        if state:
            query = query.filter(
                (Fine.state_id == state.id) | (Fine.state_id == None)
            )
    
    fines = query.all()
    
    result = []
    for fine in fines:
        result.append({
            "id": fine.id,
            "law_id": fine.law_id,
            "state_id": fine.state_id,
            "vehicle_type": fine.vehicle_type.value,
            "first_offence_amount": fine.first_offence_amount,
            "repeat_offence_amount": fine.repeat_offence_amount,
            "mv_act_reference": fine.mv_act_reference
        })
    
    return {
        "success": True,
        "count": len(result),
        "data": result
    }