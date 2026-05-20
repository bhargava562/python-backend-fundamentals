"""
FastAPI Endpoints - Async Implementation
Includes concurrent requests, error handling, and WebSocket
"""

from fastapi import HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import asyncio
import httpx
import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

# This will be populated when imported in main.py
app = None
database = None


def setup_endpoints(fastapi_app, db):
    """Setup endpoints with app and database references"""
    global app, database
    app = fastapi_app
    database = db
    register_endpoints()


def register_endpoints():
    """Register all endpoints with the app"""
    
    # ========================================================================
    # DELIVERABLE 1 & 4: ASYNC ENDPOINTS AND CONCURRENT HANDLING
    # ========================================================================
    
    @app.get("/documents/{doc_id}")
    async def get_document(doc_id: int):
        """
        Simple async endpoint - Deliverable 1 & 4
        Demonstrates basic async database query
        """
        document = await database.fetch_document(doc_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "document": document,
            "fetched_at": datetime.now().isoformat()
        }
    
    
    @app.get("/documents/{doc_id}/enriched")
    async def get_and_enrich_document(doc_id: int):
        """
        Concurrent request handling - Deliverable 1 & 4
        
        Demonstrates:
        1. Async database query
        2. Concurrent external API calls using asyncio.gather()
        3. Error handling with exceptions
        """
        # Step 1: Fetch document from database
        document = await database.fetch_document(doc_id)
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Step 2: Make concurrent external API calls
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Create multiple API requests that will run concurrently
                tasks = [
                    fetch_external_data(
                        client,
                        f"https://jsonplaceholder.typicode.com/posts/{doc_id}"
                    ),
                    fetch_external_data(
                        client,
                        f"https://jsonplaceholder.typicode.com/users/{doc_id}"
                    ),
                    fetch_external_data(
                        client,
                        f"https://jsonplaceholder.typicode.com/comments/{doc_id}"
                    ),
                ]
                
                # All requests happen concurrently!
                enrichments = await asyncio.gather(*tasks, return_exceptions=True)
        
        except Exception as e:
            logger.error(f"Error fetching enrichments: {e}")
            enrichments = [{"error": str(e)}] * 3
        
        # Step 3: Combine and return results
        return {
            "document": document,
            "enrichments": {
                "posts": enrichments[0],
                "users": enrichments[1],
                "comments": enrichments[2]
            },
            "fetched_at": datetime.now().isoformat()
        }
    
    
    # ========================================================================
    # DELIVERABLE 2: ASYNC DATABASE OPERATIONS
    # ========================================================================
    
    @app.get("/batch/documents")
    async def get_all_documents():
        """
        Async database operations - Deliverable 2
        Fetches all documents from database asynchronously
        """
        documents = await database.fetch_all_documents()
        
        return {
            "count": len(documents),
            "documents": documents,
            "fetched_at": datetime.now().isoformat()
        }
    
    
    @app.get("/batch/users")
    async def get_all_users():
        """
        Async database operations - Deliverable 2
        Demonstrates concurrent user fetching
        """
        users = await database.fetch_all_users()
        
        return {
            "count": len(users),
            "users": users,
            "fetched_at": datetime.now().isoformat()
        }
    
    
    @app.get("/batch/mixed")
    async def get_mixed_data():
        """
        Async database operations - Deliverable 2
        Demonstrates concurrent fetching of different data types
        """
        documents, users = await asyncio.gather(
            database.fetch_all_documents(),
            database.fetch_all_users()
        )
        
        return {
            "documents": {
                "count": len(documents),
                "items": documents
            },
            "users": {
                "count": len(users),
                "items": users
            },
            "fetched_at": datetime.now().isoformat()
        }
    
    
    # ========================================================================
    # DELIVERABLE 4: CONCURRENT REQUEST HANDLING
    # ========================================================================
    
    @app.get("/concurrent-batch/{count}")
    async def concurrent_batch_fetch(count: int = 3):
        """
        Concurrent request handling - Deliverable 4
        Fetches multiple documents concurrently
        """
        if count > 10:
            raise HTTPException(status_code=400, detail="Maximum count is 10")
        
        # Create tasks for fetching multiple documents
        tasks = [
            database.fetch_document(i) 
            for i in range(1, min(count + 1, 4))
        ]
        
        documents = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "requested_count": count,
            "documents": documents,
            "success_count": sum(1 for d in documents if not isinstance(d, Exception)),
            "fetched_at": datetime.now().isoformat()
        }
    
    
    # ========================================================================
    # DELIVERABLE 5: ASYNC ERROR HANDLING
    # ========================================================================
    
    @app.get("/error-handling-demo")
    async def error_handling_demo():
        """
        Async error handling - Deliverable 5
        Demonstrates graceful error handling with gather
        """
        async def failing_task(task_id: int):
            await asyncio.sleep(0.1)
            if task_id == 2:
                raise ValueError(f"Task {task_id} intentional error")
            return f"Success from task {task_id}"
        
        # Use return_exceptions=True to capture errors as values
        results = await asyncio.gather(
            failing_task(1),
            failing_task(2),  # This will fail
            failing_task(3),
            return_exceptions=True
        )
        
        processed = []
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                processed.append({
                    "task_id": i,
                    "status": "failed",
                    "error": str(result)
                })
            else:
                processed.append({
                    "task_id": i,
                    "status": "success",
                    "result": result
                })
        
        return {
            "description": "Error handling with return_exceptions=True",
            "tasks": processed,
            "total": len(results),
            "success_count": sum(1 for p in processed if p["status"] == "success"),
            "failure_count": sum(1 for p in processed if p["status"] == "failed")
        }
    
    
    # ========================================================================
    # DELIVERABLE 6: WEBSOCKET IMPLEMENTATION
    # ========================================================================
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """
        WebSocket implementation - Deliverable 6
        Demonstrates real-time communication with async handling
        """
        await websocket.accept()
        logger.info("WebSocket connection established")
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                logger.info(f"Received: {data}")
                
                # Process message and send response
                if data.lower() == "ping":
                    await websocket.send_text("pong")
                elif data.lower().startswith("fetch"):
                    # Extract document ID from message
                    try:
                        doc_id = int(data.split()[-1])
                        document = await database.fetch_document(doc_id)
                        if document:
                            await websocket.send_json({"type": "document", "data": document})
                        else:
                            await websocket.send_json({"type": "error", "message": "Document not found"})
                    except (ValueError, IndexError):
                        await websocket.send_text("Usage: fetch <doc_id>")
                else:
                    await websocket.send_text(f"Echo: {data}")
        
        except WebSocketDisconnect:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
    
    
    # ========================================================================
    # EXTERNAL DATA ENDPOINT
    # ========================================================================
    
    @app.get("/external-data")
    async def fetch_external_data_endpoint():
        """
        Fetch data from multiple external APIs concurrently
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                tasks = [
                    fetch_external_data(
                        client,
                        "https://jsonplaceholder.typicode.com/posts/1"
                    ),
                    fetch_external_data(
                        client,
                        "https://jsonplaceholder.typicode.com/users/1"
                    ),
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                "posts": results[0],
                "users": results[1],
                "fetched_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to fetch external data"
            }


async def fetch_external_data(client: httpx.AsyncClient, url: str) -> dict:
    """
    Helper function to fetch data from external API
    """
    try:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {e}")
        return {"error": str(e), "url": url}
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return {"error": str(e), "url": url}
