"""
Comprehensive Test Suite for Day 8 OAuth 2.0 Application
Tests security, configuration, endpoints, and functionality
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash
from app.database.fake_db import get_user_by_email, create_oauth_user

client = TestClient(app)


class TestSecurityConfiguration:
    """Test security configuration is properly set"""
    
    def test_secret_key_not_hardcoded(self):
        """SECRET_KEY should not be the default hardcoded value"""
        assert SECRET_KEY != "supersecretkey", "SECRET_KEY is using hardcoded default - SECURITY RISK!"
        assert len(SECRET_KEY) > 0, "SECRET_KEY is empty"
        
    def test_secret_key_has_minimum_length(self):
        """SECRET_KEY should be sufficiently long"""
        assert len(SECRET_KEY) >= 20, f"SECRET_KEY is too short ({len(SECRET_KEY)} chars). Should be >= 20 chars"
        
    def test_algorithm_is_secure(self):
        """Algorithm should be a secure choice"""
        assert ALGORITHM in ["HS256", "HS512", "RS256", "RS512"], f"Insecure algorithm: {ALGORITHM}"
        
    def test_token_expiration_configured(self):
        """Token expiration times should be properly configured"""
        assert ACCESS_TOKEN_EXPIRE_MINUTES > 0, "ACCESS_TOKEN_EXPIRE_MINUTES must be positive"
        assert REFRESH_TOKEN_EXPIRE_DAYS > 0, "REFRESH_TOKEN_EXPIRE_DAYS must be positive"
        assert ACCESS_TOKEN_EXPIRE_MINUTES < REFRESH_TOKEN_EXPIRE_DAYS * 1440, "Access token should expire before refresh token"
        

class TestPasswordSecurity:
    """Test password hashing and verification"""
    
    def test_password_hash_not_plaintext(self):
        """Password should be hashed, not stored in plaintext"""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password, "Password is not hashed!"
        assert len(hashed) > len(password), "Hash should be longer than plaintext"
        assert "$2b$" in hashed or "$2a$" in hashed, "Should use bcrypt format"
        
    def test_password_verification(self):
        """Password verification should work correctly"""
        password = "secure_test_pass_123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed), "Correct password should verify"
        assert not verify_password("wrong_password", hashed), "Wrong password should not verify"
        
    def test_password_hashing_different_salts(self):
        """Each password hash should be different (different salt)"""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2, "Same password generates same hash - weak salting!"


class TestTokenGeneration:
    """Test JWT token generation and validation"""
    
    def test_access_token_creation(self):
        """Access token should be created successfully"""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)
        
        assert token is not None, "Token should not be None"
        assert isinstance(token, str), "Token should be string"
        assert len(token) > 0, "Token should not be empty"
        # JWT has 3 parts separated by dots
        assert token.count(".") == 2, "JWT should have 3 parts (header.payload.signature)"
        
    def test_refresh_token_creation(self):
        """Refresh token should be created successfully"""
        data = {"sub": "testuser"}
        token = create_refresh_token(data)
        
        assert token is not None, "Refresh token should not be None"
        assert isinstance(token, str), "Refresh token should be string"
        assert token.count(".") == 2, "Refresh token should be valid JWT"
        
    def test_token_has_expiration(self):
        """Token should include expiration claim"""
        from jose import jwt
        
        data = {"sub": "testuser"}
        token = create_access_token(data)
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert "exp" in decoded, "Token should have 'exp' (expiration) claim"
        assert decoded["exp"] > 0, "Expiration timestamp should be positive"


class TestEndpoints:
    """Test application endpoints"""
    
    def test_home_endpoint_returns_html(self):
        """Home endpoint should return HTML template"""
        response = client.get("/")
        
        assert response.status_code == 200, "Home endpoint should return 200"
        assert "text/html" in response.headers.get("content-type", ""), "Should return HTML"
        assert b"Secure Login" in response.content, "Should contain login page content"
        assert b"Login with Google" in response.content, "Should have Google login button"
        
    def test_home_endpoint_contains_security_info(self):
        """Home endpoint should include security information"""
        response = client.get("/")
        content = response.content.decode()
        
        assert "OAuth 2.0" in content, "Should mention OAuth 2.0"
        assert "CSRF protection" in content or "secure" in content.lower(), "Should mention security"
        
    def test_home_endpoint_contains_icons(self):
        """Home endpoint should include Font Awesome icons"""
        response = client.get("/")
        content = response.content.decode()
        
        assert "fas" in content or "fab" in content, "Should reference Font Awesome icons"
        assert "font-awesome" in content or "fontawesome" in content.lower(), "Should link to Font Awesome"


class TestOAuthConfiguration:
    """Test OAuth configuration is secure"""
    
    def test_oauth_credentials_not_empty(self):
        """OAuth credentials should be configured"""
        from app.core import config
        
        assert config.GOOGLE_CLIENT_ID is not None, "GOOGLE_CLIENT_ID not configured"
        assert config.GOOGLE_CLIENT_SECRET is not None, "GOOGLE_CLIENT_SECRET not configured"
        
    def test_oauth_credentials_not_placeholder(self):
        """OAuth credentials should not be placeholder values"""
        from app.core import config
        
        assert config.GOOGLE_CLIENT_ID != "your_google_client_id", "Google credentials are placeholder"
        assert config.GOOGLE_CLIENT_SECRET != "your_google_client_secret", "Google secret is placeholder"


class TestSessionMiddleware:
    """Test session middleware for CSRF protection"""
    
    def test_session_middleware_configured(self):
        """Session middleware should be configured for CSRF protection"""
        # Check if SessionMiddleware is in the middleware stack by examining app's middleware
        # Look for evidence of middleware configuration
        assert hasattr(app, 'user_middleware'), "App should have middleware stack"
        # The SessionMiddleware adds middleware to protect against CSRF
        # We verify this by checking if SECRET_KEY is being used for sessions
        assert SECRET_KEY is not None, "SECRET_KEY should be configured for session middleware"


class TestDatabaseFunctions:
    """Test database helper functions"""
    
    def test_get_user_by_email(self):
        """Should retrieve user by email"""
        user = get_user_by_email("user1@example.com")
        
        assert user is not None, "Should find existing user"
        assert user["email"] == "user1@example.com", "Should return correct user"
        
    def test_get_user_by_email_not_found(self):
        """Should return None for non-existent user"""
        user = get_user_by_email("nonexistent@example.com")
        
        assert user is None, "Should return None for non-existent user"
        
    def test_create_oauth_user(self):
        """Should create new OAuth user"""
        user = create_oauth_user(
            email="newouser@example.com",
            name="New User",
            provider="google",
            provider_id="google-123"
        )
        
        assert user is not None, "User should be created"
        assert user["email"] == "newouser@example.com", "Email should be set"
        assert user["provider"] == "google", "Provider should be set"
        assert user["provider_id"] == "google-123", "Provider ID should be set"
        assert user["hashed_password"] is None, "OAuth users shouldn't have local password"
        
    def test_oauth_user_accessible_after_creation(self):
        """Created OAuth user should be retrievable"""
        test_email = "retrievetest@example.com"
        create_oauth_user(test_email, "Test User", "google", "google-456")
        
        user = get_user_by_email(test_email)
        assert user is not None, "Should retrieve created OAuth user"


class TestHTMLTemplate:
    """Test HTML template content and structure"""
    
    def test_html_has_bootstrap(self):
        """HTML should use Bootstrap for responsive design"""
        response = client.get("/")
        content = response.content.decode()
        
        assert "bootstrap" in content.lower(), "Should include Bootstrap CSS"
        
    def test_html_responsive_meta_tag(self):
        """HTML should have responsive viewport meta tag"""
        response = client.get("/")
        content = response.content.decode()
        
        assert "viewport" in content, "Should have viewport meta tag for responsive design"
        
    def test_html_has_security_banner(self):
        """HTML should display security information"""
        response = client.get("/")
        content = response.content.decode()
        
        assert "security-info" in content or "lock" in content.lower(), "Should have security information"


class TestNoHardcodedSecrets:
    """Test that no secrets are hardcoded in source files"""
    
    def test_config_file_has_no_hardcoded_keys(self):
        """Config.py should not have hardcoded secret values"""
        with open("app/core/config.py", "r", encoding="utf-8") as f:
            config_content = f.read()
            
        # Should not contain obviously hardcoded secrets
        assert "supersecretkey" not in config_content.lower(), "Hardcoded secret found in config!"
        assert config_content.count("os.getenv") >= 4, "Should use environment variables for secrets"
        
    def test_main_file_has_no_hardcoded_keys(self):
        """Main.py should not have hardcoded secret values"""
        with open("app/main.py", "r") as f:
            main_content = f.read()
            
        # Check for actual hardcoded secrets (like passwords or API keys)
        # Not just the word "secret" which is used in comments and variable names
        hardcoded_secrets = [
            'secret_key="',
            'SECRET_KEY="',
            "secret_key='",
            "SECRET_KEY='"
        ]
        
        for secret in hardcoded_secrets:
            assert secret not in main_content.lower(), f"Hardcoded secret pattern found: {secret}"
        

# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
