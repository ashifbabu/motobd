from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from app.services.auth_service import AuthService
from app.models.schemas import User, UserCreate, UserUpdate

router = APIRouter()
security = HTTPBearer()

def get_auth_service(request: Request) -> AuthService:
    instance_id = getattr(request.app.state, "firebase_instance_id", "default")
    return AuthService(instance_id)

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, response: Response, request: Request):
    try:
        auth_service = get_auth_service(request)
        response.status_code = status.HTTP_201_CREATED
        return await auth_service.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    try:
        auth_service = get_auth_service(request)
        return await auth_service.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), request: Request = None):
    try:
        auth_service = get_auth_service(request)
        return await auth_service.get_current_user(credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.put("/me", response_model=User)
async def update_current_user(
    user: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
):
    try:
        auth_service = get_auth_service(request)
        return await auth_service.update_current_user(user, credentials.credentials)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security), request: Request = None):
    try:
        auth_service = get_auth_service(request)
        await auth_service.logout(credentials.credentials)
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(email: str, request: Request = None):
    try:
        auth_service = get_auth_service(request)
        await auth_service.reset_password(email)
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 