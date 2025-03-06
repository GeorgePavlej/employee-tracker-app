from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class LoginData(BaseModel):
    username: str
    password: str


class ResetPassword(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str


class JWTTokenData(BaseModel):
    session_token: str


class EmployeeBase(BaseModel):
    name: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True


class TimeLogBase(BaseModel):
    employee_id: int
    date: date


class TimeLogRead(TimeLogBase):
    log_id: int
    clock_in_time: Optional[time]
    clock_out_time: Optional[time]
    lunch_start_time: Optional[time]
    lunch_end_time: Optional[time]

    class Config:
        orm_mode = True


class ShiftCreate(BaseModel):
    employee_id: int
    date: date
    start_time: time
    end_time: time


class LeaveRequestCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None
