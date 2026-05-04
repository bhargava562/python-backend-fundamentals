from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from app.api import auth_routes
from app.core.config import SECRET_KEY

app = FastAPI(title="Day 8: OAuth 2.0 Integration")

# CRITICAL: OAuth requires SessionMiddleware to store the 'state' parameter securely
# This prevents Cross-Site Request Forgery (CSRF) attacks.
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Include our API routes
app.include_router(auth_routes.router)

# Setup templates for our simple frontend
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home/Login page - redirects to dashboard if already logged in"""
    # If user is already logged in, redirect to dashboard
    if "user_id" in request.session:
        return RedirectResponse(url="/dashboard", status_code=302)
    
    return templates.TemplateResponse(request=request, name="login.html")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - displays after successful login"""
    # Check if user is logged in
    if "user_id" not in request.session:
        return RedirectResponse(url="/", status_code=302)
    
    # Extract user info from session
    user_data = {
        "request": request,
        "username": request.session.get("username", "User"),
        "email": request.session.get("email", "N/A"),
        "role": request.session.get("role", "user"),
        "provider": request.session.get("provider", "unknown").upper(),
        "access_token": request.session.get("access_token", ""),
        "login_time": request.session.get("login_time", "N/A")
    }
    
    return templates.TemplateResponse("dashboard.html", user_data)


@app.post("/logout")
async def logout(request: Request):
    """Logout route - clears session and redirects to home"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)