from datetime import date, datetime

from app.database import SessionLocal
from app.models import Employee, TimeLog, Shift, LeaveRequest
from app.schemas import ShiftCreate, LeaveRequestCreate
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
)
from fastapi.params import Query
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return [
        {"employee_id": employee.employee_id, "name": employee.name}
        for employee in employees
    ]


@app.post("/clock_in/")
def clock_in(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    now = datetime.now().time()
    existing_log = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date == today,
        TimeLog.clock_in_time != None
    ).first()
    if existing_log:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already clocked in today.")
    new_log = TimeLog(employee_id=employee_id, date=today, clock_in_time=now)
    db.add(new_log)
    db.commit()
    return {"message": f"Clocked in at {now.strftime('%H:%M:%S')}"}


@app.post("/clock_out/")
def clock_out(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    now = datetime.now().time()
    log = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date == today,
        TimeLog.clock_in_time != None,
        TimeLog.clock_out_time == None
    ).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not clocked in or already clocked out.")
    log.clock_out_time = now
    db.commit()
    return {"message": f"Clocked out at {now.strftime('%H:%M:%S')}"}


@app.post("/start_lunch/")
def start_lunch(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    now = datetime.now().time()
    log = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date == today,
        TimeLog.clock_in_time != None,
        TimeLog.clock_out_time == None,
        TimeLog.lunch_start_time == None
    ).first()
    if not log:
        raise HTTPException(
            status_code=400,
            detail="Cannot start lunch. Ensure you are clocked in and have not already started lunch."
        )
    log.lunch_start_time = now
    db.commit()
    return {"message": f"Lunch started at {now.strftime('%H:%M:%S')}"}


@app.post("/end_lunch/")
def end_lunch(employee_id: int, db: Session = Depends(get_db)):
    today = date.today()
    now = datetime.now().time()
    log = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date == today,
        TimeLog.clock_in_time != None,
        TimeLog.clock_out_time == None,
        TimeLog.lunch_start_time != None,
        TimeLog.lunch_end_time == None
    ).first()
    if not log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot end lunch. Ensure you have started lunch and are still clocked in."
        )
    log.lunch_end_time = now
    db.commit()
    return {"message": f"Lunch ended at {now.strftime('%H:%M:%S')}"}


@app.get("/logs/{employee_id}/{month_year}")
def get_logs(employee_id: int, month_year: str, db: Session = Depends(get_db)):
    try:
        month, year = map(int, month_year.split("-"))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid month-year format. Use MM-YYYY.")
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    logs = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date >= start_date,
        TimeLog.date < end_date
    ).all()
    result = []
    for log in logs:
        result.append({
            "log_id": log.log_id,
            "date": log.date.strftime("%Y-%m-%d"),
            "clock_in_time": log.clock_in_time.strftime("%H:%M:%S") if log.clock_in_time else None,
            "clock_out_time": log.clock_out_time.strftime("%H:%M:%S") if log.clock_out_time else None,
            "lunch_start_time": log.lunch_start_time.strftime("%H:%M:%S") if log.lunch_start_time else None,
            "lunch_end_time": log.lunch_end_time.strftime("%H:%M:%S") if log.lunch_end_time else None,
        })
    return result


@app.get("/logs/")
def get_logs(employee_name: str = None, date_from: str = None, date_to: str = None, db: Session = Depends(get_db)):
    query = db.query(TimeLog).join(Employee)

    if employee_name:
        query = query.filter(Employee.name.ilike(f"%{employee_name}%"))

    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, "%Y-%m-%d").date()
            query = query.filter(TimeLog.date >= date_from_parsed)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date_from format. Use YYYY-MM-DD.")
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d").date()
            query = query.filter(TimeLog.date <= date_to_parsed)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date_to format. Use YYYY-MM-DD.")

    logs = query.order_by(TimeLog.date.desc()).all()

    result = []
    for log in logs:
        result.append({
            "log_id": log.log_id,
            "employee_name": log.employee.name,
            "date": log.date.strftime("%Y-%m-%d"),
            "clock_in_time": log.clock_in_time.strftime("%H:%M:%S") if log.clock_in_time else None,
            "clock_out_time": log.clock_out_time.strftime("%H:%M:%S") if log.clock_out_time else None,
            "lunch_start_time": log.lunch_start_time.strftime("%H:%M:%S") if log.lunch_start_time else None,
            "lunch_end_time": log.lunch_end_time.strftime("%H:%M:%S") if log.lunch_end_time else None,
        })
    return result


@app.post("/shifts/")
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    on_leave = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == shift.employee_id,
        LeaveRequest.status == "Approved",
        LeaveRequest.start_date <= shift.date,
        LeaveRequest.end_date >= shift.date
    ).first()

    if on_leave:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot schedule shift: The employee is on approved leave for this date."
        )

    new_shift = Shift(**shift.dict())
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift


@app.get("/shifts/")
def get_shifts(employee_id: int = None, date_from: date = None, date_to: date = None, db: Session = Depends(get_db)):
    query = db.query(Shift, Employee.name).join(Employee)
    if employee_id:
        query = query.filter(Shift.employee_id == employee_id)
    if date_from:
        query = query.filter(Shift.date >= date_from)
    if date_to:
        query = query.filter(Shift.date <= date_to)
    results = query.all()

    shifts = []
    for shift, employee_name in results:
        shifts.append({
            "shift_id": shift.shift_id,
            "employee_id": shift.employee_id,
            "employee_name": employee_name,
            "date": shift.date.strftime("%Y-%m-%d"),
            "start_time": shift.start_time.strftime("%H:%M:%S"),
            "end_time": shift.end_time.strftime("%H:%M:%S"),
        })
    return shifts


@app.get("/reports/attendance/")
def attendance_report(
        employee_id: int = Query(...),
        date_from: date = Query(...),
        date_to: date = Query(...),
        db: Session = Depends(get_db)
):
    time_logs = db.query(TimeLog).filter(
        TimeLog.employee_id == employee_id,
        TimeLog.date >= date_from,
        TimeLog.date <= date_to
    ).all()

    total_hours_worked = 0
    for log in time_logs:
        if log.clock_in_time and log.clock_out_time:
            work_duration = datetime.combine(log.date, log.clock_out_time) - datetime.combine(log.date,
                                                                                              log.clock_in_time)
            if log.lunch_start_time and log.lunch_end_time:
                lunch_duration = datetime.combine(log.date, log.lunch_end_time) - datetime.combine(log.date,
                                                                                                   log.lunch_start_time)
                work_duration -= lunch_duration
            total_hours_worked += work_duration.total_seconds() / 3600

    return {
        "employee_id": employee_id,
        "total_hours_worked": total_hours_worked,
        "date_range": f"{date_from} to {date_to}"
    }


@app.post("/leave_requests/")
def submit_leave_request(leave_request: LeaveRequestCreate, db: Session = Depends(get_db)):
    overlapping_leave = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == leave_request.employee_id,
        LeaveRequest.status == "Approved",
        LeaveRequest.start_date <= leave_request.end_date,
        LeaveRequest.end_date >= leave_request.start_date
    ).first()
    if overlapping_leave:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Leave request overlaps with existing approved leave.")

    new_leave_request = LeaveRequest(**leave_request.dict())
    db.add(new_leave_request)
    db.commit()
    db.refresh(new_leave_request)
    return new_leave_request


@app.get("/leave_requests/")
def get_leave_requests(db: Session = Depends(get_db)):
    leave_requests = db.query(LeaveRequest).join(Employee).all()
    result = []
    for request in leave_requests:
        result.append({
            "leave_id": request.leave_id,
            "employee_id": request.employee_id,
            "employee_name": request.employee.name,
            "start_date": request.start_date.strftime("%Y-%m-%d"),
            "end_date": request.end_date.strftime("%Y-%m-%d"),
            "reason": request.reason,
            "status": request.status
        })
    return result


@app.put("/leave_requests/{leave_id}/")
def update_leave_request_status(leave_id: int, status: str = Query(...), db: Session = Depends(get_db)):
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.leave_id == leave_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if status not in ["Approved", "Rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    leave_request.status = status
    db.commit()
    return leave_request


@app.get("/health")
def health_check():
    return {"status": "ok"}
