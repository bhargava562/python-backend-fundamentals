from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.core.oauth import oauth
from app.core.security import create_access_token
from app.core.config import APP_BASE_URL
from app.database.fake_db import get_user_by_email, create_oauth_user
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["OAuth"])

@router.get("/login/{provider}")
async def login_via_oauth(provider: str, request: Request):
    """Step 1: Redirect user to the OAuth provider (e.g., Google)"""
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail=f"Provider {provider} not supported")
    
    # Explicitly construct the redirect_uri to match what's registered in OAuth provider
    # This must match EXACTLY what's configured in Google Cloud Console
    redirect_uri = f"{APP_BASE_URL}/auth/callback/{provider}"
    
    # State parameter is automatically handled by Authlib to prevent CSRF
    return await client.authorize_redirect(request, redirect_uri)


@router.get("/callback/{provider}", name="auth_callback")
async def auth_callback(provider: str, request: Request):
    """Step 2: Handle callback, exchange code for token, and issue our own JWT"""
    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=404, detail="Provider not found")

    try:
        # Exchange authorization code for access token from Google
        token = await client.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth authorization failed: {str(e)}")

    # Fetch user profile using the token
    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Could not fetch user info")

    email = user_info.get("email")
    name = user_info.get("name")
    provider_id = user_info.get("sub") # Google's unique ID for the user

    # Step 3: Database Integration (Link or Create User)
    user = get_user_by_email(email)
    if not user:
        # First time login: Create new account linked to Google
        user = create_oauth_user(email=email, name=name, provider=provider, provider_id=provider_id)
    
    # Step 4: Generate OUR app's JWT (so they can access our RBAC protected routes from Day 7)
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})

    # Step 5: Store user info in session for dashboard display
    request.session["user_id"] = user["username"]
    request.session["email"] = email
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]
    request.session["provider"] = provider
    request.session["access_token"] = access_token
    request.session["login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Step 6: Redirect to dashboard instead of returning JSON
    return RedirectResponse(url="/dashboard", status_code=302)