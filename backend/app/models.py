from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from app.database import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Shift(Base):
    __tablename__ = "shifts"

    shift_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    employee = relationship("Employee", back_populates="shifts")


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    time_logs = relationship("TimeLog", back_populates="employee")
    shifts = relationship("Shift", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")


class TimeLog(Base):
    __tablename__ = "time_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    date = Column(Date)
    clock_in_time = Column(Time)
    clock_out_time = Column(Time)
    lunch_start_time = Column(Time)
    lunch_end_time = Column(Time)

    employee = relationship("Employee", back_populates="time_logs")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String)
    status = Column(String, default="Pending")  # Options: Pending, Approved, Rejected

    employee = relationship("Employee", back_populates="leave_requests")
