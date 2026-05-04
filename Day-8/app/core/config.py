import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# SECURITY VALIDATION FUNCTIONS
# ============================================

def validate_secret_key(key: str) -> bool:
    """Validate SECRET_KEY meets security requirements."""
    if not key:
        return False
    if len(key) < 32:
        return False
    # Check it's not a placeholder or test value
    test_patterns = [
        "your_",
        "generate_",
        "replace_",
        "test_",
        "supersecret",
        "changeme",
        "12345",
        "password",
    ]
    return not any(pattern in key.lower() for pattern in test_patterns)


def validate_oauth_credentials(client_id: str, client_secret: str, allow_placeholders: bool = False) -> bool:
    """Validate OAuth credentials are not completely invalid."""
    if not client_id or not client_secret:
        return False
    
    # For testing/development, allow placeholder values if explicitly allowed
    if allow_placeholders:
        return True
    
    # For production, check they're not obviously invalid placeholders
    extremely_invalid_patterns = [
        "your_",
        "actual_",
        "replace_",
        "here",
        "123456",
    ]
    
    client_id_invalid = any(
        pattern in client_id.lower() 
        for pattern in extremely_invalid_patterns
    )
    client_secret_invalid = any(
        pattern in client_secret.lower() 
        for pattern in extremely_invalid_patterns
    )
    
    return not (client_id_invalid or client_secret_invalid)


# Determine if we're in test/development mode
IS_DEVELOPMENT = os.getenv("ENV", "development").lower() in ["development", "dev", "test"]


# ============================================
# SECURITY CONFIGURATION
# ============================================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "⚠️  CRITICAL: SECRET_KEY environment variable is not set!\n"
        "Please generate and set it in your .env file.\n"
        "Generate using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    )

# Validate SECRET_KEY strength
if not validate_secret_key(SECRET_KEY):
    raise ValueError(
        "⚠️  SECURITY ERROR: SECRET_KEY is invalid or too weak!\n"
        "Requirements:\n"
        "  - Minimum 32 characters\n"
        "  - Should be cryptographically random\n"
        "  - Not a placeholder or test value\n"
        "Generate using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
if ALGORITHM not in ["HS256", "HS512", "RS256", "RS512"]:
    raise ValueError(f"Invalid ALGORITHM: {ALGORITHM}. Must be one of: HS256, HS512, RS256, RS512")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
if REFRESH_TOKEN_EXPIRE_DAYS <= 0:
    raise ValueError("REFRESH_TOKEN_EXPIRE_DAYS must be positive")
if ACCESS_TOKEN_EXPIRE_MINUTES >= (REFRESH_TOKEN_EXPIRE_DAYS * 1440):
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be less than REFRESH_TOKEN_EXPIRE_DAYS")

# ============================================
# APPLICATION URL CONFIGURATION
# ============================================

APP_BASE_URL = os.getenv("APP_BASE_URL")
if not APP_BASE_URL:
    raise ValueError(
        "APP_BASE_URL environment variable is not set.\n"
        "Set it in .env file. Examples:\n"
        "  - Local: http://localhost:8000\n"
        "  - Production: https://yourdomain.com"
    )

# Validate APP_BASE_URL format
if not (APP_BASE_URL.startswith("http://") or APP_BASE_URL.startswith("https://")):
    raise ValueError("APP_BASE_URL must start with http:// or https://")

if "localhost" in APP_BASE_URL.lower() and APP_BASE_URL.startswith("https://"):
    raise ValueError("Localhost should use http://, not https://")

# ============================================
# OAUTH CONFIGURATION
# ============================================

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError(
        "⚠️  CRITICAL: Google OAuth credentials not configured!\n"
        "Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env file.\n"
        "Get credentials from: https://console.cloud.google.com/apis/credentials"
    )

# Validate OAuth credentials are not invalid placeholders (more lenient for dev/test)
if not validate_oauth_credentials(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, allow_placeholders=IS_DEVELOPMENT):
    raise ValueError(
        "⚠️  SECURITY ERROR: Google OAuth credentials appear to be invalid placeholders!\n"
        "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be actual credentials.\n"
        "Get them from: https://console.cloud.google.com/apis/credentials"
    )

# For production, validate Google Client ID format
if not IS_DEVELOPMENT:
    if not any(char.isdigit() for char in GOOGLE_CLIENT_ID):
        raise ValueError(
            "⚠️  SECURITY WARNING: GOOGLE_CLIENT_ID looks invalid (contains no digits).\n"
            "A valid Google Client ID typically contains numbers.\n"
            "Verify you copied the correct credentials from Google Cloud Console."
        )

# ============================================
# SECURITY SUMMARY
# ============================================
# Log that security validation passed (without showing secrets)
print("✓ Configuration validation passed")
print("✓ All required security variables are set")
print("✓ All credentials appear to be configured correctly")
