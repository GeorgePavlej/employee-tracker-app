import logging
from datetime import datetime
from os import path, environ
from random import choice
from string import ascii_letters, digits

import jwt
from fastapi import APIRouter, HTTPException, Form, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Employee
from .database import SessionLocal
from .schemas import LoginData

logger = logging.getLogger(__name__)
employee_auth_router = APIRouter(prefix="/employee/auth")


def generate_session_key():
    letters = ascii_letters + digits
    return "".join(choice(letters) for _ in range(20))


def generate_image_key():
    letters = ascii_letters + digits
    return "".join(choice(letters) for _ in range(15))


def allowed_image_names(filename: str) -> bool:
    allowed_extensions = ['jpeg', 'jpg', 'png']
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def validate_jwt_token(authorization: str = Header(default=None)):
    try:
        jwt_token = authorization.split(" ")[1]
    except IndexError:
        logger.error('Invalid authorization header.')
        raise HTTPException(status_code=401, detail='Invalid authorization header.')
    try:
        jwt_decoded = jwt.decode(jwt_token, environ['SECRET_KEY'], algorithms=['HS256'])
    except jwt.DecodeError:
        logger.error('Invalid token.')
        raise HTTPException(status_code=401, detail='Invalid token.')
    except jwt.ExpiredSignatureError:
        logger.error('Token has expired.')
        raise HTTPException(status_code=401, detail='Token has expired.')
    except jwt.InvalidTokenError:
        logger.error('Invalid token.')
        raise HTTPException(status_code=401, detail='Invalid token.')

    session_token = jwt_decoded.get('session_token')
    if not session_token:
        logger.error('Invalid token payload.')
        raise HTTPException(status_code=403, detail='Invalid token.')
    return session_token


# Login endpoint
@employee_auth_router.post("/login")
def login(request_data: LoginData):
    username = request_data.username
    password = request_data.password
    with SessionLocal() as session:
        stmt = select(Employee).where(Employee.username == username)
        employee = session.execute(stmt).scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail='Invalid username or password.')

        if not check_password_hash(employee.password, password):
            raise HTTPException(status_code=404, detail='Invalid username or password.')

        session_token = generate_session_key()
        employee.session_token = session_token
        employee.last_login = datetime.utcnow()
        session.commit()

        # Generate the JWT token without requiring access levels
        jwt_token = jwt.encode({
            'session_token': session_token,
            'username': username
        }, environ['SECRET_KEY'], algorithm="HS256")

        # Try to get access levels, but don't fail if they don't exist
        try:
            # Query the access levels record for this employee
            # from .models import AccessLevel
            # stmt2 = select(AccessLevel).where(AccessLevel.employee_id == employee.employee_id)
            # access_record = session.execute(stmt2).scalar_one_or_none()
            #
            # if access_record:
            #     access_levels = {
            #     }
                
                data = {
                    'jwt_token': jwt_token,
                    # 'access_levels': access_levels
                }
                return JSONResponse(status_code=200, content=data)
        except Exception as e:
            print(f"Error getting access levels: {e}")
        
        data = {
            'jwt_token': jwt_token
        }
        return JSONResponse(status_code=200, content=data)


# Register endpoint
@employee_auth_router.post("/register")
async def register_employee(
        name: str = Form(...),
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        access_level: int = Form(...),
):
    with SessionLocal() as session:
        try:
            password_hash = generate_password_hash(password)

            new_employee = Employee(
                name=name,
                username=username,
                email=email,
                password=password_hash,
                access_level=access_level,
                active=True,
                last_login=datetime.utcnow()
            )
            session.add(new_employee)
            session.commit()
        except IntegrityError as e:
            error_info = str(e.orig)
            if 'unique_email' in error_info:
                error_message = 'This email is already in use.'
            elif 'unique_username' in error_info:
                error_message = 'This username is already in use.'
            elif 'unique_avatar' in error_info:
                error_message = 'There was an error uploading the avatar. Please contact Admin.'
            else:
                error_message = 'An unknown error occurred, please contact Admin.'
            logger.error(f'Error registering employee: {e}')
            raise HTTPException(status_code=403, detail=error_message)
        except SQLAlchemyError as e:
            logger.error(f'Error registering employee: {e}')
            raise HTTPException(status_code=500, detail='Internal server error during registration.')

    return JSONResponse(status_code=201, content='Employee successfully registered!')


@employee_auth_router.get("/employees")
def get_employees():
    try:
        with SessionLocal() as session:
            stmt = select(Employee)
            results = session.execute(stmt).scalars().all()
            employees = []
            for emp in results:
                employees.append({
                    "employee_id": emp.employee_id,
                    "name": emp.name,
                    "username": emp.username,
                    "email": emp.email,
                    "access_level": emp.access_level,
                    "active": emp.active,
                    "last_login": emp.last_login.isoformat() if emp.last_login else None
                })
    except SQLAlchemyError as e:
        logger.error(f'Error fetching employees: {e}')
        raise HTTPException(status_code=500, detail="Internal server error while fetching employee details.")

    return employees


@employee_auth_router.put("/reset-password")
def reset_password(
        current_password: str = Form(...),
        new_password: str = Form(...),
        confirm_new_password: str = Form(...),
        session_token: str = Depends(validate_jwt_token)
):
    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail='The new passwords do not match.')

    with SessionLocal() as session:
        stmt = select(Employee).where(Employee.session_token == session_token)
        employee = session.execute(stmt).scalar_one_or_none()
        if not employee:
            raise HTTPException(status_code=404, detail='Employee not found.')

        if not check_password_hash(employee.password, current_password):
            raise HTTPException(status_code=400, detail='Your current password is incorrect.')

        if check_password_hash(employee.password, new_password):
            raise HTTPException(status_code=400, detail='The new password cannot be the same as the current password.')

        employee.password = generate_password_hash(new_password)
        session.commit()

    return JSONResponse(status_code=200, content='Password successfully updated!')
