# Day 9: MongoDB with FastAPI

## Overview
Day 9 focuses on building a NoSQL REST API using MongoDB and FastAPI. This project demonstrates how to integrate MongoDB with Python's async web framework to create a scalable, modern API for managing product catalogs.

## Project Objective
Create a complete REST API that allows CRUD operations on a MongoDB database using Motor (async MongoDB driver) and FastAPI framework.

## Key Components

### 1. Architecture
The application follows a layered architecture with clear separation of concerns:
- **API Layer**: Routes and endpoint handlers
- **Database Layer**: MongoDB connection management and async operations
- **Models Layer**: Pydantic schemas for data validation
- **Core Layer**: Configuration management

### 2. Database Integration
The application uses Motor, which is an async Python driver for MongoDB. This enables non-blocking database operations and better performance for handling multiple concurrent requests.

Features:
- Async MongoDB connection management with automatic connection lifecycle
- Automatic index creation on startup for optimized query performance
- Support for MongoDB operators like `$gte` for range queries and `$set` for atomic updates

### 3. REST API Endpoints
The API provides full CRUD functionality for products:

- **Create Product**: POST endpoint to add new products with automatic timestamp and ID generation
- **List Products**: GET endpoint with optional filtering by category and minimum price using MongoDB query operators
- **Get Product**: GET endpoint to retrieve a specific product by its MongoDB ObjectId
- **Update Product**: PUT endpoint for partial updates using Pydantic validation to ensure only valid fields are updated
- **Delete Product**: DELETE endpoint to remove products with proper error handling

### 4. Data Validation
Pydantic models ensure data integrity:
- **Product Model**: Defines the structure for product documents including embedded reviews
- **Review Model**: Represents nested review objects with rating validation (1-5)
- **ProductUpdate Model**: Allows partial updates with optional fields for flexibility

### 5. Query Capabilities
The API supports dynamic filtering:
- **Category Filtering**: Find products by specific category
- **Price Range Filtering**: Find products above a minimum price using MongoDB's `$gte` operator
- **Combined Filtering**: Apply multiple filters simultaneously

## Configuration
The application uses environment variables for configuration:
- MongoDB connection URL (defaults to localhost:27017)
- Database name selection

## Error Handling
Comprehensive error handling for:
- Invalid MongoDB ObjectId formats (400 Bad Request)
- Missing products (404 Not Found)
- Validation errors for incorrect data types or values
- Update operations that don't affect any records

## Data Model
Products are stored as documents in MongoDB with the following structure:
- Unique identifier (MongoDB ObjectId)
- Product name and description
- Price information
- Category for organizing products
- Review collection with nested review objects
- Seller reference ID
- Automatic creation timestamp

## Features Implemented

### Async Operations
All database operations are non-blocking, allowing the API to handle multiple requests concurrently without waiting for database responses.

### Type Safety
Pydantic models provide runtime type validation, ensuring data consistency and providing automatic API documentation.

### MongoDB-Specific Features
- Use of MongoDB query operators for flexible filtering
- Embedded documents for related data (reviews within products)
- Index creation for improved query performance
- Atomic update operations using MongoDB operators

### API Documentation
Automatic interactive API documentation is available through Swagger UI, making it easy to test all endpoints without external tools.

## Testing
The API has been tested for all CRUD operations including:
- Creating new products
- Retrieving all products with optional filters
- Fetching individual products by ID
- Updating product information
- Deleting products
- Proper HTTP status codes (201 for creation, 200 for success, 404 for not found)

## Development Setup
The project includes:
- Virtual environment configuration for isolated dependencies
- Requirements file for easy dependency installation
- Environment variable support for configuration
- Package structure with proper initialization files

## Technologies Used
- **FastAPI**: Modern Python web framework for building APIs
- **Motor**: Async MongoDB driver for Python
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running the FastAPI application
- **MongoDB**: NoSQL database for flexible document storage
