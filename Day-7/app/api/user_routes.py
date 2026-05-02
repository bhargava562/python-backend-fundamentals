from fastapi import APIRouter, Depends
from app.schemas import UserResponse
from app.api.deps import get_current_user, get_admin_user, get_moderator_user

router = APIRouter(prefix="/users", tags=["Protected User Routes"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user)):
    """Fetch profile of currently logged-in user."""
    return current_user

@router.get("/moderator-panel")
def read_moderator_panel(current_user: dict = Depends(get_moderator_user)):
    """Endpoint protected by Moderator Role."""
    return {
        "message": f"Welcome Moderator {current_user['username']}!", 
        "moderation_tools": ["ban_user", "delete_post", "flag_content"],
        "permissions": "Can moderate content and manage users"
    }

@router.get("/admin-dashboard")
def read_admin_data(current_user: dict = Depends(get_admin_user)):
    """Endpoint protected by Admin Role."""
    return {
        "message": f"Welcome Admin {current_user['username']}!", 
        "confidential_data": "Top secret financial reports",
        "admin_tools": ["user_management", "system_configuration", "logs"]
    }