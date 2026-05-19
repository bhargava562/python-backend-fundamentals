#!/usr/bin/env python
"""
Comprehensive testing script for Celery and FastAPI integration.

This script tests all major endpoints and Celery functionality to verify
the application is working correctly.

Usage:
    python test_celery_api.py
"""

import requests
import json
import time
from typing import Dict, Any, Optional
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10
VERBOSE = True

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


class CeleryAPITester:
    """Test suite for Celery API endpoints."""
    
    def __init__(self, base_url: str = BASE_URL, verbose: bool = VERBOSE):
        self.base_url = base_url
        self.verbose = verbose
        self.session = requests.Session()
        self.test_results = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with color coding."""
        if not self.verbose:
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "SUCCESS":
            print(f"{GREEN}✓ {RESET}[{timestamp}] {message}")
        elif level == "ERROR":
            print(f"{RED}✗ {RESET}[{timestamp}] {message}")
        elif level == "WARNING":
            print(f"{YELLOW}⚠ {RESET}[{timestamp}] {message}")
        elif level == "INFO":
            print(f"{BLUE}ℹ {RESET}[{timestamp}] {message}")
        else:
            print(f"{RESET}[{timestamp}] {message}")
    
    def print_header(self, text: str):
        """Print section header."""
        print(f"\n{BOLD}{'='*60}")
        print(f"{BLUE}{text:^60}{RESET}")
        print(f"{BOLD}{'='*60}{RESET}\n")
    
    def test_endpoint(
        self,
        name: str,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        expected_status: int = 200
    ) -> Optional[Dict]:
        """Test an API endpoint and return response."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, timeout=TIMEOUT)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=TIMEOUT)
            elif method == "DELETE":
                response = self.session.delete(url, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Check response status
            if response.status_code == expected_status:
                self.log(f"{name}: {method} {endpoint}", "SUCCESS")
                self.test_results.append((name, "PASS"))
                
                try:
                    return response.json()
                except:
                    return None
            else:
                self.log(
                    f"{name}: Expected status {expected_status}, got {response.status_code}",
                    "ERROR"
                )
                self.test_results.append((name, "FAIL"))
                return None
                
        except requests.exceptions.ConnectionError:
            self.log(f"{name}: Failed to connect to {url}", "ERROR")
            self.test_results.append((name, "FAIL"))
            return None
        except Exception as e:
            self.log(f"{name}: {str(e)}", "ERROR")
            self.test_results.append((name, "FAIL"))
            return None
    
    def print_json(self, data: Dict):
        """Pretty print JSON data."""
        print(json.dumps(data, indent=2))
    
    def test_health_endpoints(self):
        """Test health and info endpoints."""
        self.print_header("HEALTH & INFO ENDPOINTS")
        
        # Root endpoint
        response = self.test_endpoint("Root Endpoint", "GET", "/")
        if response:
            self.log(f"Service: {response.get('service')}")
            self.log(f"Version: {response.get('version')}")
        
        # Health check
        response = self.test_endpoint("Health Check", "GET", "/health")
        if response:
            self.log(f"Status: {response.get('status')}")
            self.log(f"Workers: {response.get('workers', {}).get('count')}")
        
        # Worker stats
        response = self.test_endpoint("Worker Statistics", "GET", "/stats/workers")
        if response:
            active_workers = list(response.get('active', {}).keys()) if response.get('active') else []
            self.log(f"Active Workers: {', '.join(active_workers) if active_workers else 'None'}")
        
        # Queue stats
        response = self.test_endpoint("Queue Statistics", "GET", "/stats/queues")
        if response:
            self.log(f"Active Queues Retrieved")
        
        # Active tasks
        response = self.test_endpoint("Active Tasks", "GET", "/tasks/active")
        if response:
            total = response.get('total_active', 0)
            self.log(f"Total Active Tasks: {total}")
        
        # Scheduled tasks
        response = self.test_endpoint("Scheduled Tasks", "GET", "/tasks/scheduled")
        if response:
            total = response.get('total_scheduled', 0)
            self.log(f"Total Scheduled Tasks: {total}")
    
    def test_email_endpoints(self):
        """Test email task endpoints."""
        self.print_header("EMAIL TASK ENDPOINTS")
        
        # Send single email
        email_data = {
            "email": "test@example.com",
            "subject": "Test Email from Celery",
            "body": "This is a test email from the API"
        }
        response = self.test_endpoint("Send Email", "POST", "/api/email/send", email_data)
        task_id = None
        if response:
            task_id = response.get('task_id')
            self.log(f"Task ID: {task_id}")
            
            # Wait for task to complete
            time.sleep(3)
            
            # Check task status
            status_response = self.test_endpoint(
                "Check Email Task Status",
                "GET",
                f"/task/{task_id}"
            )
            if status_response:
                self.log(f"Task Status: {status_response.get('status')}")
                if status_response.get('result'):
                    self.log(f"Result: Email sent to {status_response['result'].get('email')}")
        
        # Send bulk emails
        bulk_data = {
            "emails": ["user1@example.com", "user2@example.com", "user3@example.com"],
            "subject": "Bulk Email Test",
            "body": "This is a bulk email test"
        }
        response = self.test_endpoint("Send Bulk Email", "POST", "/api/email/send-bulk", bulk_data)
        if response:
            self.log(f"Bulk Task ID: {response.get('task_id')}")
            self.log(f"Recipients: {response.get('recipient_count')}")
    
    def test_image_endpoints(self):
        """Test image processing endpoints."""
        self.print_header("IMAGE PROCESSING ENDPOINTS")
        
        image_data = {
            "image_ids": [1, 2, 3, 4, 5],
            "operation": "batch"
        }
        response = self.test_endpoint(
            "Process Images",
            "POST",
            "/api/images/process",
            image_data
        )
        task_id = None
        if response:
            task_id = response.get('task_id')
            self.log(f"Task ID: {task_id}")
            self.log(f"Images to Process: {response.get('image_count')}")
            
            # Wait for processing
            time.sleep(5)
            
            # Check status
            status_response = self.test_endpoint(
                "Check Image Task Status",
                "GET",
                f"/task/{task_id}"
            )
            if status_response:
                self.log(f"Task Status: {status_response.get('status')}")
    
    def test_report_endpoints(self):
        """Test report generation endpoints."""
        self.print_header("REPORT GENERATION ENDPOINTS")
        
        # PDF Report
        pdf_data = {"report_type": "pdf", "data_rows": 1000}
        response = self.test_endpoint("Generate PDF Report", "POST", "/api/reports/generate", pdf_data)
        if response:
            task_id = response.get('task_id')
            self.log(f"PDF Task ID: {task_id}")
            
            # Wait for report generation
            time.sleep(5)
            
            # Check status
            status_response = self.test_endpoint(
                "Check PDF Report Status",
                "GET",
                f"/task/{task_id}"
            )
            if status_response:
                self.log(f"Task Status: {status_response.get('status')}")
        
        # CSV Report
        csv_data = {"report_type": "csv", "data_rows": 5000}
        response = self.test_endpoint("Generate CSV Report", "POST", "/api/reports/generate", csv_data)
        if response:
            self.log(f"CSV Task ID: {response.get('task_id')}")
    
    def test_data_endpoints(self):
        """Test data import/export endpoints."""
        self.print_header("DATA IMPORT/EXPORT ENDPOINTS")
        
        # Import data
        import_data = {
            "data_source": "external_api",
            "num_records": 10000
        }
        response = self.test_endpoint(
            "Import Data",
            "POST",
            "/api/data/import",
            import_data
        )
        if response:
            self.log(f"Import Task ID: {response.get('task_id')}")
            self.log(f"Records: {response.get('num_records')}")
        
        # Export data
        export_data = {
            "export_format": "csv",
            "table_name": "users"
        }
        response = self.test_endpoint(
            "Export Data",
            "POST",
            "/api/data/export",
            export_data
        )
        if response:
            self.log(f"Export Task ID: {response.get('task_id')}")
    
    def test_system_endpoints(self):
        """Test system maintenance endpoints."""
        self.print_header("SYSTEM MAINTENANCE ENDPOINTS")
        
        # Manual cleanup
        response = self.test_endpoint("Trigger Cleanup", "POST", "/system/cleanup")
        if response:
            self.log(f"Cleanup Task ID: {response.get('task_id')}")
        
        # Health check
        response = self.test_endpoint("Trigger Health Check", "POST", "/system/health-check")
        if response:
            self.log(f"Health Check Task ID: {response.get('task_id')}")
        
        # Worker info
        response = self.test_endpoint("Get Worker Info", "GET", "/system/worker-info")
        if response:
            worker_count = response.get('total_workers', 0)
            self.log(f"Total Workers: {worker_count}")
            workers = response.get('workers', {})
            for worker_name in workers.keys():
                self.log(f"  - {worker_name}")
    
    def test_task_management(self):
        """Test task management endpoints."""
        self.print_header("TASK MANAGEMENT")
        
        # Send a test task
        test_data = {
            "email": "cancel_test@example.com",
            "subject": "Test for cancellation",
            "body": "This task will be cancelled"
        }
        response = self.test_endpoint("Send Test Email", "POST", "/api/email/send", test_data)
        task_id = None
        if response:
            task_id = response.get('task_id')
            self.log(f"Test Task ID: {task_id}")
            
            # Try to cancel (may or may not succeed depending on execution state)
            if task_id:
                cancel_response = self.test_endpoint(
                    "Cancel Task",
                    "DELETE",
                    f"/task/{task_id}",
                    expected_status=200
                )
                if cancel_response:
                    self.log(f"Cancellation Message: {cancel_response.get('message')}")
    
    def print_summary(self):
        """Print test summary."""
        self.print_header("TEST SUMMARY")
        
        total = len(self.test_results)
        passed = sum(1 for _, result in self.test_results if result == "PASS")
        failed = total - passed
        
        print(f"{BOLD}Total Tests: {total}{RESET}")
        print(f"{GREEN}{BOLD}Passed: {passed}{RESET}")
        if failed > 0:
            print(f"{RED}{BOLD}Failed: {failed}{RESET}")
        
        print(f"\n{BOLD}Test Results:{RESET}")
        for test_name, result in self.test_results:
            status_color = GREEN if result == "PASS" else RED
            status_symbol = "✓" if result == "PASS" else "✗"
            print(f"{status_color}{status_symbol}{RESET} {test_name}")
        
        # Success rate
        success_rate = (passed / total * 100) if total > 0 else 0
        rate_color = GREEN if success_rate >= 80 else YELLOW if success_rate >= 60 else RED
        print(f"\n{rate_color}{BOLD}Success Rate: {success_rate:.1f}%{RESET}")
    
    def run_all_tests(self):
        """Run all tests."""
        try:
            self.test_health_endpoints()
            self.test_email_endpoints()
            self.test_image_endpoints()
            self.test_report_endpoints()
            self.test_data_endpoints()
            self.test_system_endpoints()
            self.test_task_management()
            self.print_summary()
        except Exception as e:
            self.log(f"Test suite error: {str(e)}", "ERROR")
            raise


def main():
    """Main entry point."""
    print(f"\n{BOLD}{BLUE}{'='*60}")
    print(f"{'Celery & FastAPI Integration Test Suite':^60}")
    print(f"{'='*60}{RESET}\n")
    
    tester = CeleryAPITester()
    
    print(f"{YELLOW}Starting tests...{RESET}")
    print(f"{YELLOW}Base URL: {BASE_URL}{RESET}")
    print(f"{YELLOW}Timeout: {TIMEOUT}s{RESET}\n")
    
    tester.run_all_tests()
    
    print(f"\n{BOLD}{BLUE}{'='*60}")
    print(f"{'Test Suite Complete':^60}")
    print(f"{'='*60}{RESET}\n")


if __name__ == "__main__":
    main()
