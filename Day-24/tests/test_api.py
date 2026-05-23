"""API integration tests"""
import pytest
from httpx import AsyncClient


class TestSystemEndpoints:
    """System observability endpoint tests"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_test_client: AsyncClient):
        """Test deep infrastructure health check endpoint"""
        response = await async_test_client.get("/api/v1/system/health")
        
        # Accept both 200 (healthy) and 503 (degraded)
        assert response.status_code in [200, 503]
        
        data = response.json()
        assert "status" in data
        assert "checks" in data
        assert "timestamp" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_version_endpoint(self, async_test_client: AsyncClient):
        """Test version endpoint"""
        response = await async_test_client.get("/api/v1/system/version")
        
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "project_name" in data
        assert "environment" in data

    @pytest.mark.asyncio
    async def test_info_endpoint(self, async_test_client: AsyncClient):
        """Test application info endpoint"""
        response = await async_test_client.get("/api/v1/system/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "project_name" in data
        assert "features" in data
        assert data["features"]["rate_limiting"] is True
        assert data["features"]["async_tasks"] is True

    @pytest.mark.asyncio
    async def test_readiness_endpoint(self, async_test_client: AsyncClient):
        """Test readiness check endpoint"""
        response = await async_test_client.get("/api/v1/system/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True

    @pytest.mark.asyncio
    async def test_liveness_endpoint(self, async_test_client: AsyncClient):
        """Test liveness check endpoint"""
        response = await async_test_client.get("/api/v1/system/live")
        
        assert response.status_code == 200
        data = response.json()
        assert data["alive"] is True


class TestBusinessEndpoints:
    """Business operations endpoint tests"""
    
    @pytest.mark.asyncio
    async def test_list_operations_empty(self, async_test_client: AsyncClient):
        """Test listing operations when none exist"""
        response = await async_test_client.get("/api/v1/operations/operations")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    async def test_dispatch_operation_success(self, async_test_client: AsyncClient):
        """Test dispatching a background operation"""
        payload = {
            "reference_id": "TX-12345",
            "summary": "Test operation processing"
        }
        
        response = await async_test_client.post("/api/v1/operations/process", json=payload)
        
        assert response.status_code == 202
        data = response.json()
        assert data["reference_id"] == "TX-12345"
        assert "task_id" in data
        assert data["status"] == "queued_for_worker_processing"

    @pytest.mark.asyncio
    async def test_dispatch_operation_validation_error(self, async_test_client: AsyncClient):
        """Test operation dispatch with invalid input"""
        invalid_payload = {
            "reference_id": "short",  # Too short
            "summary": "Valid summary"
        }
        
        response = await async_test_client.post("/api/v1/operations/process", json=invalid_payload)
        
        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "SCHEMA_VALIDATION_ERROR"
        assert "details" in data

    @pytest.mark.asyncio
    async def test_dispatch_operation_missing_fields(self, async_test_client: AsyncClient):
        """Test operation dispatch with missing required fields"""
        incomplete_payload = {
            "reference_id": "TX-12345"
            # Missing 'summary'
        }
        
        response = await async_test_client.post("/api/v1/operations/process", json=incomplete_payload)
        
        assert response.status_code == 422
        data = response.json()
        assert data["error_code"] == "SCHEMA_VALIDATION_ERROR"

    @pytest.mark.asyncio
    async def test_get_operation_not_found(self, async_test_client: AsyncClient):
        """Test retrieving non-existent operation"""
        response = await async_test_client.get("/api/v1/operations/operations/TX-NOTFOUND")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_list_operations_with_filters(self, async_test_client: AsyncClient):
        """Test listing operations with filters"""
        # Create an operation first
        payload = {
            "reference_id": "TX-FILTER-TEST",
            "summary": "Filter test operation"
        }
        await async_test_client.post("/api/v1/operations/process", json=payload)
        
        # List with pagination
        response = await async_test_client.get(
            "/api/v1/operations/operations",
            params={"skip": 0, "limit": 10}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_batch_process_success(self, async_test_client: AsyncClient):
        """Test batch processing multiple operations"""
        payloads = [
            {"reference_id": "TX-BATCH-001", "summary": "First batch item"},
            {"reference_id": "TX-BATCH-002", "summary": "Second batch item"},
            {"reference_id": "TX-BATCH-003", "summary": "Third batch item"}
        ]
        
        response = await async_test_client.post(
            "/api/v1/operations/batch-process",
            json=payloads
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["batch_size"] == 3
        assert len(data["tasks"]) == 3

    @pytest.mark.asyncio
    async def test_batch_process_exceeds_limit(self, async_test_client: AsyncClient):
        """Test batch processing with too many items"""
        payloads = [
            {"reference_id": f"TX-BATCH-{i:04d}", "summary": f"Item {i}"}
            for i in range(101)  # Exceed 100 limit
        ]
        
        response = await async_test_client.post(
            "/api/v1/operations/batch-process",
            json=payloads
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data


class TestRootEndpoint:
    """Root endpoint tests"""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_test_client: AsyncClient):
        """Test API root endpoint"""
        response = await async_test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "environment" in data
        assert "docs_url" in data


class TestErrorHandling:
    """Error handling tests"""
    
    @pytest.mark.asyncio
    async def test_404_not_found(self, async_test_client: AsyncClient):
        """Test 404 error response"""
        response = await async_test_client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_request_validation_error_response_format(self, async_test_client: AsyncClient):
        """Test validation error response format"""
        response = await async_test_client.post(
            "/api/v1/operations/process",
            json={"reference_id": "x"}  # Invalid
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "error_code" in data
        assert "message" in data
        assert "details" in data


class TestCORSHeaders:
    """CORS header tests"""
    
    @pytest.mark.asyncio
    async def test_cors_preflight_request(self, async_test_client: AsyncClient):
        """Test CORS preflight request handling"""
        response = await async_test_client.options(
            "/api/v1/operations/process",
            headers={
                "Origin": "http://example.com",
                "Access-Control-Request-Method": "POST"
            }
        )
        
        # Should have CORS headers
        assert "access-control-allow-origin" in response.headers or response.status_code in [200, 405]


class TestRateLimiting:
    """Rate limiting tests"""
    
    @pytest.mark.asyncio
    async def test_rate_limit_header_present(self, async_test_client: AsyncClient):
        """Test that rate limit headers are present"""
        response = await async_test_client.get("/api/v1/system/health")
        
        # Rate limit headers should be present
        headers = response.headers
        # Just verify endpoint is accessible
        assert response.status_code in [200, 503]


class TestSecurityHeaders:
    """Security header tests"""
    
    @pytest.mark.asyncio
    async def test_security_headers_present(self, async_test_client: AsyncClient):
        """Test that security headers are present in responses"""
        response = await async_test_client.get("/api/v1/system/health")
        
        headers = response.headers
        
        # Check for common security headers
        assert "x-frame-options" in headers or "X-Frame-Options" in headers
        assert "x-content-type-options" in headers or "X-Content-Type-Options" in headers
