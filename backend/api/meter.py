from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from db.models import MeterReading
from sqlalchemy import desc
from datetime import datetime, timedelta

router = APIRouter(prefix="/meter", tags=["Meter"])


@router.get("/live")
def get_live_meter(db: Session = Depends(get_db)):
    # latest reading
    latest = (
        db.query(MeterReading)
        .order_by(desc(MeterReading.timestamp))
        .first()
    )

    if not latest:
        return {"message": "No readings yet"}

    # last 1 hour usage
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    readings = (
        db.query(MeterReading)
        .filter(MeterReading.timestamp >= one_hour_ago)
        .all()
    )

    total_kwh = sum(r.energy_kwh for r in readings)

    return {
        "current_reading": latest.energy_kwh,
        "timestamp": latest.timestamp,
        "last_hour_consumption": round(total_kwh, 3)
    }
