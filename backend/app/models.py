from app.database import engine
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class Shift(Base):
    __tablename__ = "shifts"

    shift_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    employee = relationship("Employee", back_populates="shifts")


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=True)
    access_level = Column(Integer, nullable=True)
    session_token = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    last_login = Column(DateTime,)

    time_logs = relationship("TimeLog", back_populates="employee")
    shifts = relationship("Shift", back_populates="employee")
    leave_requests = relationship("LeaveRequest", back_populates="employee")


class AccessLevel(Base):
    __tablename__ = "access_levels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wafer_id_editor = Column(Integer, nullable=False)
    wafer_cassette_editor = Column(Integer, nullable=False)
    create_inventory = Column(Integer, nullable=False)
    view_inventory = Column(Integer, nullable=False)
    user_management = Column(Integer, nullable=False)
    request_manager = Column(Integer, nullable=False)
    automated_inventory = Column(Integer, nullable=False)
    run_selection = Column(Integer, nullable=False)
    osmium_manager = Column(Integer, nullable=False)
    supply_manager = Column(Integer, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.employee_id', ondelete="CASCADE"))

    employee = relationship("Employee", backref="access_levels")


class AccessLevelEnum(Base):
    __tablename__ = "access_level_enum"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)


class TimeLog(Base):
    __tablename__ = "time_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"))
    date = Column(Date)
    clock_in_time = Column(Time)
    clock_out_time = Column(Time)
    lunch_start_time = Column(Time)
    lunch_end_time = Column(Time)

    employee = relationship("Employee", back_populates="time_logs")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.employee_id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String)
    status = Column(String, default="Pending")  # Options: Pending, Approved, Rejected

    employee = relationship("Employee", back_populates="leave_requests")
