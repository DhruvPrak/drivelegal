# app/routers/laws.py
# All endpoints related to traffic laws
# Base URL: /api/v1/laws

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import Law, State, Fine
from app.schemas.schemas import LawResponse, LawsListResponse

# Create router — all routes here will be prefixed with /api/v1/laws
router = APIRouter(
    prefix="/api/v1/laws",
    tags=["Traffic Laws"]  # groups endpoints in /docs
)


@router.get("/", response_model=LawsListResponse)
def get_all_laws(
    category: Optional[str] = Query(None, description="Filter by category e.g. Speed, Safety"),
    state_code: Optional[str] = Query(None, description="Filter by state code e.g. DL, MH"),
    search: Optional[str] = Query(None, description="Search by title or section"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(50, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all traffic laws with optional filters.
    
    - Filter by category: /laws/?category=Speed
    - Filter by state: /laws/?state_code=DL
    - Search: /laws/?search=helmet
    - Pagination: /laws/?skip=0&limit=20
    """
    # Start with base query
    query = db.query(Law)
    
    # Apply category filter if provided
    if category:
        query = query.filter(Law.category == category)
    
    # Apply state filter if provided
    if state_code:
        state = db.query(State).filter(State.code == state_code.upper()).first()
        if state:
            # Get laws that are national OR specific to this state
            query = query.filter(
                (Law.is_national == True) | (Law.state_id == state.id)
            )
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Law.title.ilike(search_term)) |
            (Law.section.ilike(search_term)) |
            (Law.description.ilike(search_term))
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    laws = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "count": total,
        "data": laws
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all unique law categories"""
    # Get distinct categories from database
    categories = db.query(Law.category).distinct().filter(
        Law.category != None
    ).all()
    
    # Extract just the category names from tuples
    category_list = [c[0] for c in categories]
    
    return {
        "success": True,
        "data": sorted(category_list)
    }


@router.get("/{law_id}", response_model=LawResponse)
def get_law_by_id(
    law_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific law by its ID"""
    law = db.query(Law).filter(Law.id == law_id).first()
    
    # If law not found, return 404 error
    if not law:
        raise HTTPException(
            status_code=404,
            detail=f"Law with id {law_id} not found"
        )
    
    return law


@router.get("/section/{section}")
def get_law_by_section(
    section: str,
    db: Session = Depends(get_db)
):
    """
    Get a law by its MV Act section number
    Example: /laws/section/Section%20185
    """
    law = db.query(Law).filter(
        Law.section.ilike(f"%{section}%")
    ).first()
    
    if not law:
        raise HTTPException(
            status_code=404,
            detail=f"Law for section '{section}' not found"
        )
    
    return {
        "success": True,
        "data": {
            "id": law.id,
            "section": law.section,
            "title": law.title,
            "description": law.description,
            "plain_language": law.plain_language,
            "category": law.category,
            "is_national": law.is_national
        }
    }