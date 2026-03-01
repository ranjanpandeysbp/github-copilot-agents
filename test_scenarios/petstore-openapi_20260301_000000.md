# Test Scenarios Report: Petstore OpenAPI 3.0
**Date:** March 1, 2026  
**API:** Swagger Petstore - OpenAPI 3.0  
**Base URL:** https://petstore3.swagger.io/api/v3  

---

## Overview
This comprehensive test scenarios document covers all API endpoints in the Petstore OpenAPI 3.0 specification. Test cases are organized by operation type (Positive, Negative, Boundary, Regression) for each endpoint.

---

# 1. PET ENDPOINTS

## 1.1 POST /pet - Add a New Pet

### Test Case 1.1.1: Positive Test - Add Valid Pet

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1001,
  "name": "Fluffy",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "https://example.com/photo1.jpg"
  ],
  "tags": [
    {
      "id": 1,
      "name": "friendly"
    }
  ],
  "status": "available"
}
```

**Test Case Explanation:**  
Tests successful creation of a pet with all mandatory and optional fields properly populated. Validates that the API accepts a complete pet object with valid data types and enum values.

**Expected Result:**
- HTTP Status Code: 200
- Response contains created pet object with ID 1001
- All fields are returned as submitted
- Response format: JSON/XML

---

### Test Case 1.1.2: Positive Test - Add Pet with Minimal Data

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "name": "Buddy",
  "photoUrls": [
    "https://example.com/buddy.jpg"
  ]
}
```

**Test Case Explanation:**  
Tests that API accepts pet creation with only mandatory fields (name, photoUrls). Validates minimal valid request processing.

**Expected Result:**
- HTTP Status Code: 200
- Response includes the created pet with auto-generated ID
- Status defaults to appropriate value
- API operations work with minimal data

---

### Test Case 1.1.3: Negative Test - Missing Required Fields

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1002,
  "category": {
    "id": 1,
    "name": "Dogs"
  }
}
```

**Test Case Explanation:**  
Tests API validation by omitting required field "name". Should reject the request with validation error.

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) or 422 (Validation exception)
- Error message clearly indicates missing required field "name"
- Pet is not created in the system

---

### Test Case 1.1.4: Negative Test - Invalid Status Enum

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1003,
  "name": "Max",
  "photoUrls": [
    "https://example.com/max.jpg"
  ],
  "status": "invalid_status"
}
```

**Test Case Explanation:**  
Tests enum validation on status field. Should reject because "invalid_status" is not in enum list: [available, pending, sold].

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) or 422 (Validation exception)
- Error indicates invalid enum value for status
- Pet is not created

---

### Test Case 1.1.5: Boundary Test - Empty Pet Name

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1004,
  "name": "",
  "photoUrls": [
    "https://example.com/photo.jpg"
  ]
}
```

**Test Case Explanation:**  
Tests boundary condition with empty string for required name field. Validates whether API treats empty string as missing required field.

**Expected Result:**
- HTTP Status Code: 400 or 422 (should reject empty required field)
- Error message indicates empty name not acceptable
- OR HTTP Status Code: 200 if API accepts and generates default name

---

### Test Case 1.1.6: Boundary Test - Maximum ID Value

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 9223372036854775807,
  "name": "BigID",
  "photoUrls": [
    "https://example.com/photo.jpg"
  ]
}
```

**Test Case Explanation:**  
Tests boundary with maximum int64 value. Edge case for database integer field limits.

**Expected Result:**
- HTTP Status Code: 200
- Pet created with maximum ID value
- No overflow errors occur

---

### Test Case 1.1.7: Regression Test - Duplicate Pet ID

**Scenario Type:** Regression  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet`  
**Test Data (First Call):**
```json
{
  "id": 1005,
  "name": "First Pet",
  "photoUrls": ["https://example.com/photo1.jpg"]
}
```
**Test Data (Second Call with same ID):**
```json
{
  "id": 1005,
  "name": "Duplicate Pet",
  "photoUrls": ["https://example.com/photo2.jpg"]
}
```

**Test Case Explanation:**  
Tests system behavior when attempting to create a pet with ID that already exists. Validates duplicate ID handling.

**Expected Result:**
- First call: HTTP Status Code 200 (success)
- Second call: HTTP Status Code 400 or existing pet is updated/replaced
- System handles duplicate ID appropriately
- NO data corruption occurs

---

## 1.2 PUT /pet - Update an Existing Pet

### Test Case 1.2.1: Positive Test - Update Existing Pet

**Scenario Type:** Positive  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1001,
  "name": "Fluffy Updated",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": [
    "https://example.com/photo-new.jpg"
  ],
  "tags": [
    {
      "id": 1,
      "name": "friendly"
    }
  ],
  "status": "sold"
}
```

**Test Case Explanation:**  
Tests successful update of an existing pet. Validates that all pet attributes can be modified and changes are persisted.

**Expected Result:**
- HTTP Status Code: 200
- Response contains updated pet with all new values
- Previous values are replaced
- ID remains unchanged

---

### Test Case 1.2.2: Negative Test - Update Non-Existent Pet

**Scenario Type:** Negative  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 99999,
  "name": "Non-Existent Pet",
  "photoUrls": [
    "https://example.com/photo.jpg"
  ],
  "status": "available"
}
```

**Test Case Explanation:**  
Tests update of pet ID that doesn't exist in the system. Should return error indicating pet not found.

**Expected Result:**
- HTTP Status Code: 404 (Pet not found)
- Error message indicates the pet ID doesn't exist
- No new pet is created

---

### Test Case 1.2.3: Negative Test - Missing Required Fields in Update

**Scenario Type:** Negative  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1001,
  "status": "sold"
}
```

**Test Case Explanation:**  
Tests update with missing required field "name". Validates that update validations are enforced.

**Expected Result:**
- HTTP Status Code: 400 or 422
- Error indicates missing required field
- Pet is not updated in database

---

### Test Case 1.2.4: Boundary Test - Update with Empty PhotoUrls Array

**Scenario Type:** Boundary  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/pet`  
**Test Data:**
```json
{
  "id": 1001,
  "name": "Updated Pet",
  "photoUrls": []
}
```

**Test Case Explanation:**  
Tests boundary condition with empty photoUrls array for required field. Validates whether API requires at least one photo URL.

**Expected Result:**
- HTTP Status Code: 400/422 (if photoUrls required) OR
- HTTP Status Code: 200 (if empty array is allowed)
- Clear error message if invalid

---

### Test Case 1.2.5: Regression Test - Update and Verify Consistency

**Scenario Type:** Regression  
**Test URL (Update):** `PUT https://petstore3.swagger.io/api/v3/pet`  
**Test URL (Verify):** `GET https://petstore3.swagger.io/api/v3/pet/1001`  
**Test Data:**
```json
{
  "id": 1001,
  "name": "Consistency Test",
  "photoUrls": ["https://example.com/updated.jpg"],
  "status": "pending"
}
```

**Test Case Explanation:**  
Tests that updated data is correctly persisted and retrievable. After update, retrieve the pet to verify all changes were saved.

**Expected Result:**
- Update returns HTTP Status Code: 200
- GET request returns same data that was updated
- All fields match the update request
- Data consistency across operations

---

## 1.3 GET /pet/findByStatus - Find Pets by Status

### Test Case 1.3.1: Positive Test - Find Available Pets

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=available`  
**Test Data:** Query parameter `status=available`  

**Test Case Explanation:**  
Tests retrieval of all pets with "available" status. Basic filtering functionality.

**Expected Result:**
- HTTP Status Code: 200
- Response is JSON/XML array of Pet objects
- All returned pets have status = "available"
- Array may be empty if no available pets exist

---

### Test Case 1.3.2: Positive Test - Find Sold Pets

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=sold`  
**Test Data:** Query parameter `status=sold`  

**Test Case Explanation:**  
Tests retrieval of pets with "sold" status.

**Expected Result:**
- HTTP Status Code: 200
- Response array contains only pets with status = "sold"
- Consistent filtering behavior

---

### Test Case 1.3.3: Positive Test - Find Pending Pets

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=pending`  
**Test Data:** Query parameter `status=pending`  

**Test Case Explanation:**  
Tests filtering for "pending" status.

**Expected Result:**
- HTTP Status Code: 200
- Only pets with pending status returned
- Proper filtering applied

---

### Test Case 1.3.4: Negative Test - Invalid Status Value

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=invalid`  
**Test Data:** Query parameter `status=invalid`  

**Test Case Explanation:**  
Tests API behavior with invalid enum value. "invalid" is not in [available, pending, sold].

**Expected Result:**
- HTTP Status Code: 400 (Invalid status value)
- Error message indicates invalid status
- Empty array OR error response

---

### Test Case 1.3.5: Boundary Test - Case Sensitivity of Status

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=AVAILABLE`  
**Test Data:** Query parameter `status=AVAILABLE` (uppercase)  

**Test Case Explanation:**  
Tests whether status filtering is case-sensitive or case-insensitive.

**Expected Result:**
- HTTP Status Code: 400 (if case-sensitive) OR
- HTTP Status Code: 200 (if case-insensitive)
- Behavior clearly documented

---

### Test Case 1.3.6: Boundary Test - Special Characters in Status

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=available%20%20` (with trailing spaces)  
**Test Data:** Query parameter with URL-encoded spaces  

**Test Case Explanation:**  
Tests parameter parsing with special characters and whitespace.

**Expected Result:**
- HTTP Status Code: 400 or 200 with appropriate handling
- API properly trims or rejects malformed input

---

### Test Case 1.3.7: Regression Test - Consistency Across Multiple Queries

**Scenario Type:** Regression  
**Test URLs:** 
- `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=available` (First call)
- `GET https://petstore3.swagger.io/api/v3/pet/findByStatus?status=available` (Second call after waiting)

**Test Case Explanation:**  
Tests that repeated queries return consistent results. Validates no race conditions or timing issues.

**Expected Result:**
- Both calls return HTTP Status Code: 200
- Same pets are returned in both queries
- Consistent ordering (if pagination used)
- No data corruption between calls

---

## 1.4 GET /pet/findByTags - Find Pets by Tags

### Test Case 1.4.1: Positive Test - Find by Single Tag

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=friendly`  
**Test Data:** Query parameter `tags=friendly`  

**Test Case Explanation:**  
Tests retrieval of pets with specific tag. Basic tag filtering.

**Expected Result:**
- HTTP Status Code: 200
- Response array contains pets with "friendly" tag
- Correct pets returned

---

### Test Case 1.4.2: Positive Test - Find by Multiple Tags (Comma-Separated)

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=friendly,cute`  
**Test Data:** Query parameter `tags=friendly,cute`  

**Test Case Explanation:**  
Tests retrieval with multiple tags. Per API description: "Use tag1, tag2, tag3 for testing". Should return pets matching ANY of the tags.

**Expected Result:**
- HTTP Status Code: 200
- Response array contains pets with "friendly" OR "cute" tags
- Multiple tag filtering works correctly

---

### Test Case 1.4.3: Positive Test - Find with Tag1, Tag2, Tag3

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=tag1,tag2,tag3`  
**Test Data:** Query parameter `tags=tag1,tag2,tag3`  

**Test Case Explanation:**  
Uses the API-recommended test values for tag filtering.

**Expected Result:**
- HTTP Status Code: 200
- Pets with these tags are returned
- API designed to work with these specific test values

---

### Test Case 1.4.4: Negative Test - Invalid Tag Value

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=nonexistent%20tag`  
**Test Data:** Query parameter `tags=nonexistent tag`  

**Test Case Explanation:**  
Tests with non-existent tag that has no matching pets.

**Expected Result:**
- HTTP Status Code: 200 with empty array OR
- HTTP Status Code: 400 if tag validation fails
- No error for valid but non-matching tags

---

### Test Case 1.4.5: Boundary Test - Empty Tags Parameter

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=`  
**Test Data:** Query parameter `tags=` (empty)  

**Test Case Explanation:**  
Tests API behavior with empty tag parameter. Tags is required parameter.

**Expected Result:**
- HTTP Status Code: 400 (Invalid tag value) OR
- HTTP Status Code: 200 (returns all pets if parameter ignored)
- Clear documentation of behavior

---

### Test Case 1.4.6: Boundary Test - Special Characters in Tags

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=tag%40with%40special`  
**Test Data:** Query parameter with special characters (@ symbols)  

**Test Case Explanation:**  
Tests tag parsing with special characters that might need URL encoding.

**Expected Result:**
- HTTP Status Code: 400 or 200 with proper handling
- Parser correctly decodes URL-encoded values
- No injection vulnerabilities

---

### Test Case 1.4.7: Regression Test - Tag Filtering Excludes Non-Matching Pets

**Scenario Type:** Regression  
**Test Steps:**
1. Create pet with tag "friendly"
2. Create pet with tag "aggressive"
3. Query with tags=friendly
4. Verify aggressive pet is NOT returned

**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/findByTags?tags=friendly`  

**Test Case Explanation:**  
Tests that filtering correctly excludes pets without the specified tag.

**Expected Result:**
- HTTP Status Code: 200
- Response contains friendly pets ONLY
- Aggressive pet excluded
- Filtering logic works correctly

---

## 1.5 GET /pet/{petId} - Find Pet by ID

### Test Case 1.5.1: Positive Test - Get Existing Pet by ID

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/1001`  
**Test Data:** Path parameter `petId=1001`  

**Test Case Explanation:**  
Tests retrieval of pet by valid ID that exists in system.

**Expected Result:**
- HTTP Status Code: 200
- Response contains Pet object with ID 1001
- All pet details returned correctly
- Response format: JSON/XML based on Accept header

---

### Test Case 1.5.2: Negative Test - Get Non-Existent Pet

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/99999`  
**Test Data:** Path parameter `petId=99999`  

**Test Case Explanation:**  
Tests retrieval of pet ID that doesn't exist. Should return 404.

**Expected Result:**
- HTTP Status Code: 404 (Pet not found)
- Clear error message indicating pet not found
- No default or null object returned

---

### Test Case 1.5.3: Negative Test - Invalid Pet ID Format

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/invalid`  
**Test Data:** Path parameter `petId=invalid` (not a number)  

**Test Case Explanation:**  
Tests API parsing of non-numeric pet ID. Expected type is int64.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied)
- Error message indicates invalid ID format
- Type validation enforced

---

### Test Case 1.5.4: Negative Test - Negative Pet ID

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/-1`  
**Test Data:** Path parameter `petId=-1`  

**Test Case Explanation:**  
Tests boundary with negative ID value. Typically IDs should be positive.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied) OR
- HTTP Status Code: 404 (if system treats negatives as non-existent)
- Documented behavior

---

### Test Case 1.5.5: Boundary Test - Zero Pet ID

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/0`  
**Test Data:** Path parameter `petId=0`  

**Test Case Explanation:**  
Tests with ID value of zero. Edge case for numerical input.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied) OR
- HTTP Status Code: 404 (Pet not found)
- Consistent with API design

---

### Test Case 1.5.6: Boundary Test - Maximum Pet ID

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/9223372036854775807`  
**Test Data:** Path parameter `petId=9223372036854775807` (max int64)  

**Test Case Explanation:**  
Tests with maximum int64 value.

**Expected Result:**
- HTTP Status Code: 200 (if pet exists) OR
- HTTP Status Code: 404 (if pet not found)
- No overflow errors
- Proper int64 handling

---

### Test Case 1.5.7: Regression Test - Get Same Pet Multiple Times

**Scenario Type:** Regression  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/pet/1001` (multiple times)  

**Test Case Explanation:**  
Tests consistency of GET operations. Same pet retrieved multiple times should return identical data.

**Expected Result:**
- All requests return HTTP Status Code: 200
- Identical pet data returned each time
- No data modification between requests
- No concurrency issues

---

## 1.6 POST /pet/{petId} - Update Pet with Form Data

### Test Case 1.6.1: Positive Test - Update Pet Name and Status

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001?name=UpdatedName&status=sold`  
**Test Data:** 
- Path parameter: `petId=1001`
- Query parameters: `name=UpdatedName`, `status=sold`

**Test Case Explanation:**  
Tests partial update using form data (query parameters). Updates name and status without full pet object.

**Expected Result:**
- HTTP Status Code: 200
- Pet with ID 1001 has updated name "UpdatedName"
- Status changed to "sold"
- Other fields remain unchanged

---

### Test Case 1.6.2: Positive Test - Update Only Pet Name

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001?name=OnlyName`  
**Test Data:** 
- Path parameter: `petId=1001`
- Query parameter: `name=OnlyName`

**Test Case Explanation:**  
Tests partial update with only name parameter. Status parameter omitted.

**Expected Result:**
- HTTP Status Code: 200
- Pet name updated to "OnlyName"
- Status remains as previous value
- No required field validation for form-based update

---

### Test Case 1.6.3: Positive Test - Update Only Pet Status

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001?status=pending`  
**Test Data:** 
- Path parameter: `petId=1001`
- Query parameter: `status=pending`

**Test Case Explanation:**  
Tests partial update with status only.

**Expected Result:**
- HTTP Status Code: 200
- Pet status updated to "pending"
- Name remains unchanged

---

### Test Case 1.6.4: Negative Test - Update Non-Existent Pet

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/99999?name=Test&status=available`  
**Test Data:** 
- Path parameter: `petId=99999`
- Query parameters: `name=Test`, `status=available`

**Test Case Explanation:**  
Tests form update on non-existent pet ID.

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) OR
- HTTP Status Code: 404 (Pet not found)
- Pet is not created
- Clear error message

---

### Test Case 1.6.5: Negative Test - Invalid Status Value in Form Update

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001?status=unknown`  
**Test Data:** 
- Path parameter: `petId=1001`
- Query parameter: `status=unknown` (invalid enum)

**Test Case Explanation:**  
Tests validation of enum field in form update.

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) OR
- HTTP Status Code: 422 (Validation exception)
- Pet not updated
- Error indicates invalid status value

---

### Test Case 1.6.6: Boundary Test - Empty Name in Form Update

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001?name=`  
**Test Data:** 
- Path parameter: `petId=1001`
- Query parameter: `name=` (empty value)

**Test Case Explanation:**  
Tests update with empty name parameter.

**Expected Result:**
- HTTP Status Code: 400 (invalid input) or 200
- If accepted: pet name becomes empty or maintains previous value
- Behavior should be documented

---

### Test Case 1.6.7: Regression Test - Form Update Consistency with Full Update

**Scenario Type:** Regression  
**Test URLs:**
- `POST https://petstore3.swagger.io/api/v3/pet/1001?name=FormUpdate&status=sold` (form update)
- `GET https://petstore3.swagger.io/api/v3/pet/1001` (verify)

**Test Case Explanation:**  
Tests that form-based update produces same result as full PUT update. Ensures consistency between update methods.

**Expected Result:**
- Form update returns HTTP Status Code: 200
- GET request returns pet with name "FormUpdate" and status "sold"
- Form update and PUT method produce identical results

---

## 1.7 DELETE /pet/{petId} - Delete a Pet

### Test Case 1.7.1: Positive Test - Delete Existing Pet

**Scenario Type:** Positive  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/pet/1001`  
**Test Data:** Path parameter `petId=1001`  

**Test Case Explanation:**  
Tests successful deletion of existing pet.

**Expected Result:**
- HTTP Status Code: 200 (Pet deleted)
- Pet with ID 1001 removed from system
- Subsequent GET /pet/1001 returns 404

---

### Test Case 1.7.2: Positive Test - Delete with API Key Header

**Scenario Type:** Positive  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/pet/1001` with header `api_key: test-api-key`  
**Test Data:** 
- Path parameter: `petId=1001`
- Optional header: `api_key: test-api-key`

**Test Case Explanation:**  
Tests deletion with optional api_key header parameter. API allows both authenticated and unauthenticated delete.

**Expected Result:**
- HTTP Status Code: 200
- Pet successfully deleted
- API key validation passed

---

### Test Case 1.7.3: Negative Test - Delete Non-Existent Pet

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/pet/99999`  
**Test Data:** Path parameter `petId=99999`  

**Test Case Explanation:**  
Tests deletion of pet ID that doesn't exist.

**Expected Result:**
- HTTP Status Code: 404 (Pet not found) OR
- HTTP Status Code: 200 (idempotent delete acknowledges non-existence)
- No error if pet doesn't exist or proper 404 if required

---

### Test Case 1.7.4: Negative Test - Invalid Pet ID

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/pet/invalid`  
**Test Data:** Path parameter `petId=invalid`  

**Test Case Explanation:**  
Tests deletion with non-numeric pet ID.

**Expected Result:**
- HTTP Status Code: 400 (Invalid pet value)
- Error message indicates invalid ID format
- Type validation enforced

---

### Test Case 1.7.5: Boundary Test - Negative Pet ID for Delete

**Scenario Type:** Boundary  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/pet/-100`  
**Test Data:** Path parameter `petId=-100`  

**Test Case Explanation:**  
Tests deletion with negative ID.

**Expected Result:**
- HTTP Status Code: 400 (Invalid pet value) OR
- HTTP Status Code: 404 (Pet not found)
- Consistent with GET behavior

---

### Test Case 1.7.6: Regression Test - Double Delete Idempotency

**Scenario Type:** Regression  
**Test URLs (Sequential):**
1. `DELETE https://petstore3.swagger.io/api/v3/pet/1001` (first delete)
2. `DELETE https://petstore3.swagger.io/api/v3/pet/1001` (second delete)

**Test Case Explanation:**  
Tests idempotency of DELETE operation. Multiple deletes of same resource should be safe.

**Expected Result:**
- First delete: HTTP Status Code: 200
- Second delete: HTTP Status Code: 200 (if idempotent) OR 404 (if strict)
- No error side effects
- Documented idempotency behavior

---

### Test Case 1.7.7: Regression Test - Delete and Verify Non-Existence

**Scenario Type:** Regression  
**Test URLs:**
1. `DELETE https://petstore3.swagger.io/api/v3/pet/1001` (delete)
2. `GET https://petstore3.swagger.io/api/v3/pet/1001` (verify deletion)

**Test Case Explanation:**  
Tests that DELETE actually removes pet and subsequent GET cannot retrieve it.

**Expected Result:**
- Delete returns HTTP Status Code: 200
- GET returns HTTP Status Code: 404
- Pet completely removed from system

---

## 1.8 POST /pet/{petId}/uploadImage - Upload Pet Image

### Test Case 1.8.1: Positive Test - Upload Valid Image File

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage`  
**Test Data:**
- Path parameter: `petId=1001`
- File content: Binary image file (e.g., sample.jpg)
- Content-Type: `application/octet-stream`

**Test Case Explanation:**  
Tests successful image file upload for existing pet. Validates file upload functionality.

**Expected Result:**
- HTTP Status Code: 200
- Response contains ApiResponse object
- Response includes confirmation message
- File uploaded and associated with pet

---

### Test Case 1.8.2: Positive Test - Upload Image with Additional Metadata

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage?additionalMetadata=PetPhoto`  
**Test Data:**
- Path parameter: `petId=1001`
- Query parameter: `additionalMetadata=PetPhoto`
- File content: Binary image file
- Content-Type: `application/octet-stream`

**Test Case Explanation:**  
Tests image upload with optional metadata parameter. Metadata should be stored with image.

**Expected Result:**
- HTTP Status Code: 200
- ApiResponse indicates successful upload
- Metadata "PetPhoto" stored with image

---

### Test Case 1.8.3: Negative Test - Upload for Non-Existent Pet

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/99999/uploadImage`  
**Test Data:**
- Path parameter: `petId=99999`
- File content: Binary image file

**Test Case Explanation:**  
Tests image upload attempt for pet that doesn't exist.

**Expected Result:**
- HTTP Status Code: 404 (Pet not found)
- Error message indicates pet not found
- File is not uploaded

---

### Test Case 1.8.4: Negative Test - No File Uploaded

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage`  
**Test Data:**
- Path parameter: `petId=1001`
- File content: Empty/No file

**Test Case Explanation:**  
Tests upload endpoint with no file provided. Should validate file presence.

**Expected Result:**
- HTTP Status Code: 400 (No file uploaded)
- Error message indicates file is required
- No empty file entry created

---

### Test Case 1.8.5: Boundary Test - Invalid Pet ID for Upload

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/invalid/uploadImage`  
**Test Data:**
- Path parameter: `petId=invalid`
- File content: Binary image file

**Test Case Explanation:**  
Tests upload with non-numeric pet ID.

**Expected Result:**
- HTTP Status Code: 400
- Error message indicates invalid ID format

---

### Test Case 1.8.6: Boundary Test - Large Image File Upload

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage`  
**Test Data:**
- Path parameter: `petId=1001`
- File: Large image file (50+ MB)

**Test Case Explanation:**  
Tests system's handling of large file uploads. May hit server size limits.

**Expected Result:**
- HTTP Status Code: 200 (if supported) OR
- HTTP Status Code: 413 (if request too large)
- Clear error for oversized uploads
- No partial upload corruption

---

### Test Case 1.8.7: Regression Test - Multiple Image Uploads

**Scenario Type:** Regression  
**Test URLs:**
1. `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage` (first upload)
2. `POST https://petstore3.swagger.io/api/v3/pet/1001/uploadImage` (second upload)

**Test Case Explanation:**  
Tests whether multiple uploads overwrite previous image or store both.

**Expected Result:**
- Both uploads return HTTP Status Code: 200
- Either: Multiple images stored, OR
- Latest image replaces previous one
- Behavior clearly documented

---

---

# 2. STORE ENDPOINTS

## 2.1 GET /store/inventory - Get Inventory

### Test Case 2.1.1: Positive Test - Get Store Inventory

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/inventory`  
**Test Data:** No parameters required  

**Test Case Explanation:**  
Tests successful retrieval of store pet inventory by status. Should return map of status to quantity counts.

**Expected Result:**
- HTTP Status Code: 200
- Response is JSON object with status as keys and integer counts as values
- Contains entries like: `{ "available": 10, "pending": 5, "sold": 3 }`
- API key authentication works

---

### Test Case 2.1.2: Positive Test - Verify Inventory Counts

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/inventory`  

**Test Case Explanation:**  
Tests that inventory counts match actual pet statuses in system. Validates inventory accuracy.

**Expected Result:**
- All status counts are non-negative integers
- Total count matches sum of all pets
- Counts update when pets are added/modified/deleted

---

### Test Case 2.1.3: Boundary Test - Empty Inventory

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/inventory`  

**Test Case Explanation:**  
Tests inventory response when all pets have been deleted (if possible).

**Expected Result:**
- HTTP Status Code: 200
- Empty object `{}` OR all status values are 0
- No error for empty inventory

---

### Test Case 2.1.4: Regression Test - Inventory Consistency

**Scenario Type:** Regression  
**Test Steps:**
1. Get initial inventory
2. Create pet with status "available"
3. Get inventory again
4. Verify "available" count increased by 1

**Test Case Explanation:**  
Tests that inventory updates correctly when new pets are added.

**Expected Result:**
- Initial inventory retrieved successfully
- After adding pet, inventory "available" count increases by exactly 1
- Other counts remain unchanged

---

## 2.2 POST /store/order - Place an Order

### Test Case 2.2.1: Positive Test - Place Valid Order

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "id": 2001,
  "petId": 1001,
  "quantity": 1,
  "shipDate": "2026-03-15T10:00:00Z",
  "status": "approved",
  "complete": false
}
```

**Test Case Explanation:**  
Tests successful order placement with valid data.

**Expected Result:**
- HTTP Status Code: 200
- Response contains Order object with provided ID
- Order status is "approved"
- complete field is false
- Order persisted in system

---

### Test Case 2.2.2: Positive Test - Place Order with Minimal Data

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "petId": 1001,
  "quantity": 2
}
```

**Test Case Explanation:**  
Tests order creation with only required fields (petId, quantity).

**Expected Result:**
- HTTP Status Code: 200
- Order created with auto-generated ID
- Default status assigned
- complete defaults to false

---

### Test Case 2.2.3: Positive Test - Order with Different Status Values

**Scenario Type:** Positive  
**Test URLs and Data:**

**For status "placed":**
```json
{
  "id": 2002,
  "petId": 1001,
  "quantity": 1,
  "status": "placed"
}
```

**For status "approved":**
```json
{
  "id": 2003,
  "petId": 1002,
  "quantity": 2,
  "status": "approved"
}
```

**For status "delivered":**
```json
{
  "id": 2004,
  "petId": 1003,
  "quantity": 1,
  "status": "delivered"
}
```

**Test Case Explanation:**  
Tests all valid status enum values for orders.

**Expected Result:**
- All orders created successfully with HTTP Status Code: 200
- Each order retains its specified status
- Status values from [placed, approved, delivered] all accepted

---

### Test Case 2.2.4: Negative Test - Negative Quantity

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "petId": 1001,
  "quantity": -5
}
```

**Test Case Explanation:**  
Tests order with negative quantity. Should be invalid.

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) or 422 (Validation exception)
- Error message indicates quantity must be positive
- Order not created

---

### Test Case 2.2.5: Negative Test - Invalid Status Value

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "petId": 1001,
  "quantity": 1,
  "status": "invalid_status"
}
```

**Test Case Explanation:**  
Tests enum validation for status field.

**Expected Result:**
- HTTP Status Code: 400 or 422
- Error indicates invalid status
- Order not created

---

### Test Case 2.2.6: Boundary Test - Zero Quantity

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "petId": 1001,
  "quantity": 0
}
```

**Test Case Explanation:**  
Tests order with zero quantity. Boundary between negative and positive.

**Expected Result:**
- HTTP Status Code: 400 or 422 (if quantity must be >= 1) OR
- HTTP Status Code: 200 (if zero is allowed)
- Behavior documented

---

### Test Case 2.2.7: Boundary Test - Large Quantity

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/store/order`  
**Test Data:**
```json
{
  "petId": 1001,
  "quantity": 999999
}
```

**Test Case Explanation:**  
Tests with very large quantity value. Tests int32 limits.

**Expected Result:**
- HTTP Status Code: 200 or 400 (if has max limit)
- Order created if no maximum
- Clear error if exceeds limits

---

### Test Case 2.2.8: Regression Test - Create Order and Retrieve It

**Scenario Type:** Regression  
**Test URLs:**
1. POST order: `POST https://petstore3.swagger.io/api/v3/store/order` with ID 2005
2. Verify: `GET https://petstore3.swagger.io/api/v3/store/order/2005`

**Test Case Explanation:**  
Tests that created order can be retrieved with exact same data.

**Expected Result:**
- POST returns HTTP Status Code: 200
- GET returns HTTP Status Code: 200
- Retrieved order matches submitted data
- All fields persist correctly

---

## 2.3 GET /store/order/{orderId} - Get Order by ID

### Test Case 2.3.1: Positive Test - Get Existing Order

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/1` (or valid order ID)  
**Test Data:** Path parameter `orderId=1`  

**Test Case Explanation:**  
Tests retrieval of order by valid ID. Per API docs: "For valid response try integer IDs with value <= 5 or > 10".

**Expected Result:**
- HTTP Status Code: 200
- Response contains Order object with ID 1
- All order fields returned

---

### Test Case 2.3.2: Positive Test - Get Order with ID <= 5

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/5`  
**Test Data:** Path parameter `orderId=5`  

**Test Case Explanation:**  
Tests with ID at upper boundary of "valid" range (<=5).

**Expected Result:**
- HTTP Status Code: 200
- Order retrieved successfully
- Valid test case per API documentation

---

### Test Case 2.3.3: Positive Test - Get Order with ID > 10

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/11`  
**Test Data:** Path parameter `orderId=11`  

**Test Case Explanation:**  
Tests with ID in valid range (>10) per API documentation.

**Expected Result:**
- HTTP Status Code: 200 (if order exists) OR 404 (if no order with this ID)
- Valid test case per API documentation

---

### Test Case 2.3.4: Negative Test - Order Not Found (ID 6-10 Boundary)

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/7`  
**Test Data:** Path parameter `orderId=7`  

**Test Case Explanation:**  
Tests with ID in exclusion range (6-10). API docs indicate these IDs generate exceptions/not found.

**Expected Result:**
- HTTP Status Code: 404 (Order not found)
- Error message indicates order not in system
- Per API documentation for ID range 6-10

---

### Test Case 2.3.5: Negative Test - Invalid Order ID Format

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/invalid`  
**Test Data:** Path parameter `orderId=invalid`  

**Test Case Explanation:**  
Tests with non-numeric order ID.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied)
- Error message indicates invalid format

---

### Test Case 2.3.6: Boundary Test - Negative Order ID

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/-1`  
**Test Data:** Path parameter `orderId=-1`  

**Test Case Explanation:**  
Tests with negative order ID.

**Expected Result:**
- HTTP Status Code: 400 or 404
- Consistent with API error handling

---

### Test Case 2.3.7: Boundary Test - Maximum Order ID

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/store/order/9223372036854775807`  
**Test Data:** Path parameter `orderId=9223372036854775807` (max int64)  

**Test Case Explanation:**  
Tests with maximum int64 value.

**Expected Result:**
- HTTP Status Code: 200 or 404 (if order doesn't exist)
- No overflow errors
- Proper int64 handling

---

## 2.4 DELETE /store/order/{orderId} - Delete Order

### Test Case 2.4.1: Positive Test - Delete Existing Order (Valid ID)

**Scenario Type:** Positive  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/1`  
**Test Data:** Path parameter `orderId=1`  

**Test Case Explanation:**  
Tests successful deletion of order. Per API docs: "For valid response try integer IDs with value < 1000".

**Expected Result:**
- HTTP Status Code: 200 (order deleted)
- Order removed from system
- Cannot retrieve order after deletion

---

### Test Case 2.4.2: Positive Test - Delete Order with ID < 1000

**Scenario Type:** Positive  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/999`  
**Test Data:** Path parameter `orderId=999`  

**Test Case Explanation:**  
Tests deletion with ID at valid boundary (<1000).

**Expected Result:**
- HTTP Status Code: 200 (order deleted) (if exists)
- Deletion succeeds or 404 if not found

---

### Test Case 2.4.3: Negative Test - Delete Order ID >= 1000

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/1000`  
**Test Data:** Path parameter `orderId=1000`  

**Test Case Explanation:**  
Tests deletion with ID at or above 1000. Per API docs: "Anything above 1000 or non-integers will generate API errors".

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied)
- Error message indicates invalid ID for deletion
- Order not deleted

---

### Test Case 2.4.4: Negative Test - Delete Non-Existent Order

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/99999` (assuming > 1000)  
**Test Data:** Path parameter `orderId=99999`  

**Test Case Explanation:**  
Tests deletion of order that doesn't exist.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied) OR
- HTTP Status Code: 404 (Order not found)
- Error message appropriate to condition

---

### Test Case 2.4.5: Negative Test - Invalid Order ID Format

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/abc`  
**Test Data:** Path parameter `orderId=abc`  

**Test Case Explanation:**  
Tests with non-integer value. API docs indicate non-integers generate errors.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied)
- Error message indicates invalid format

---

### Test Case 2.4.6: Boundary Test - Negative Order ID for Deletion

**Scenario Type:** Boundary  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/store/order/-1`  
**Test Data:** Path parameter `orderId=-1`  

**Test Case Explanation:**  
Tests deletion with negative ID.

**Expected Result:**
- HTTP Status Code: 400 (Invalid ID supplied)
- Consistent error handling

---

### Test Case 2.4.7: Regression Test - Double Delete Idempotency

**Scenario Type:** Regression  
**Test URLs (Sequential):**
1. `DELETE https://petstore3.swagger.io/api/v3/store/order/2` (first delete)
2. `DELETE https://petstore3.swagger.io/api/v3/store/order/2` (second delete)

**Test Case Explanation:**  
Tests DELETE idempotency. Multiple deletes should be safe.

**Expected Result:**
- First delete: HTTP Status Code: 200 (if order exists)
- Second delete: HTTP Status Code: 200 (if idempotent) OR 404 (if strict)
- No side effects from double delete

---

---

# 3. USER ENDPOINTS

## 3.1 POST /user - Create User

### Test Case 3.1.1: Positive Test - Create Valid User

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user`  
**Test Data:**
```json
{
  "id": 1,
  "username": "user123",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "5551234567",
  "userStatus": 1
}
```

**Test Case Explanation:**  
Tests successful creation of user with all fields populated.

**Expected Result:**
- HTTP Status Code: 200
- Response contains User object
- User persisted in system with provided ID

---

### Test Case 3.1.2: Positive Test - Create User with Minimal Data

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user`  
**Test Data:**
```json
{
  "username": "minimaluser",
  "firstName": "Jane"
}
```

**Test Case Explanation:**  
Tests user creation with minimal required fields only.

**Expected Result:**
- HTTP Status Code: 200
- User created with auto-generated ID
- Optional fields default to empty/null

---

### Test Case 3.1.3: Positive Test - Create User without Email

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user`  
**Test Data:**
```json
{
  "username": "noemail",
  "firstName": "Bob",
  "lastName": "Smith",
  "password": "pass123"
}
```

**Test Case Explanation:**  
Tests creation without email field.

**Expected Result:**
- HTTP Status Code: 200
- User created
- Email field remains empty/null

---

### Test Case 3.1.4: Negative Test - Duplicate Username

**Scenario Type:** Negative  
**Test Data (First):**
```json
{
  "username": "duplicateuser",
  "firstName": "User1"
}
```
**Test Data (Second):**
```json
{
  "username": "duplicateuser",
  "firstName": "User2"
}
```

**Test Case Explanation:**  
Tests creation of user with username that already exists. Should reject duplicate.

**Expected Result:**
- First POST: HTTP Status Code: 200
- Second POST: HTTP Status Code: 400 (Invalid input) or system updates existing user
- Duplicate username handling documented

---

### Test Case 3.1.5: Boundary Test - Empty Username

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user`  
**Test Data:**
```json
{
  "username": "",
  "firstName": "Test"
}
```

**Test Case Explanation:**  
Tests user creation with empty username string.

**Expected Result:**
- HTTP Status Code: 400/422 (if username required) OR
- HTTP Status Code: 200 (if empty allowed)
- Behavior documented

---

### Test Case 3.1.6: Boundary Test - Very Long Username

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user`  
**Test Data:**
```json
{
  "username": "verylonguserentamewithhundredsofcharactersthatshouldnotbeallowedbutmaybeitdoes12345678901234567890",
  "firstName": "Test"
}
```

**Test Case Explanation:**  
Tests with extremely long username string. May hit length limits.

**Expected Result:**
- HTTP Status Code: 200 (if accepted) OR
- HTTP Status Code: 400/422 (if length validated)
- Clear error if too long

---

### Test Case 3.1.7: Regression Test - Create User and Login

**Scenario Type:** Regression  
**Step 1 - Create User:**
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```
**Step 2 - Login:** `GET /user/login?username=testuser&password=testpass123`

**Test Case Explanation:**  
Tests end-to-end: create user then validate login works.

**Expected Result:**
- User creation: HTTP Status Code: 200
- Login: HTTP Status Code: 200
- User can authenticate after creation

---

## 3.2 POST /user/createWithList - Create Multiple Users

### Test Case 3.2.1: Positive Test - Create List of Valid Users

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user/createWithList`  
**Test Data:**
```json
[
  {
    "username": "user1",
    "firstName": "User",
    "lastName": "One"
  },
  {
    "username": "user2",
    "firstName": "User",
    "lastName": "Two"
  },
  {
    "username": "user3",
    "firstName": "User",
    "lastName": "Three"
  }
]
```

**Test Case Explanation:**  
Tests batch creation of multiple users in single request.

**Expected Result:**
- HTTP Status Code: 200
- All three users created
- Each user has unique ID
- Can retrieve each user individually

---

### Test Case 3.2.2: Positive Test - Create Single User in List

**Scenario Type:** Positive  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user/createWithList`  
**Test Data:**
```json
[
  {
    "username": "singleuser",
    "firstName": "Single"
  }
]
```

**Test Case Explanation:**  
Tests batch endpoint with one-element list.

**Expected Result:**
- HTTP Status Code: 200
- Single user created successfully
- Batch operation works with single item

---

### Test Case 3.2.3: Negative Test - Empty User List

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user/createWithList`  
**Test Data:** `[]`

**Test Case Explanation:**  
Tests batch creation with empty array.

**Expected Result:**
- HTTP Status Code: 200 (accepted but no-op) OR
- HTTP Status Code: 400 (Invalid input - empty list)
- Behavior documented

---

### Test Case 3.2.4: Negative Test - List with Duplicate Usernames

**Scenario Type:** Negative  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user/createWithList`  
**Test Data:**
```json
[
  {
    "username": "sameuser",
    "firstName": "User1"
  },
  {
    "username": "sameuser",
    "firstName": "User2"
  }
]
```

**Test Case Explanation:**  
Tests batch with duplicate usernames in same request.

**Expected Result:**
- HTTP Status Code: 400 (Invalid input) OR
- System creates one and rejects second OR
- Both created (overwrites)
- Duplicate handling clear

---

### Test Case 3.2.5: Boundary Test - Large List of Users

**Scenario Type:** Boundary  
**Test URL:** `POST https://petstore3.swagger.io/api/v3/user/createWithList`  
**Test Data:** Array with 1000 users

**Test Case Explanation:**  
Tests batch operation with large list. Tests performance and limits.

**Expected Result:**
- HTTP Status Code: 200 (if accepted) OR
- HTTP Status Code: 413 (if too large) OR
- HTTP Status Code: 400 (if has max limit)
- Clear error for oversized requests

---

### Test Case 3.2.6: Regression Test - Batch Create and Individual Retrieval

**Scenario Type:** Regression  
**Step 1 - Batch Create**
```json
[
  {"username": "batch1", "firstName": "B1"},
  {"username": "batch2", "firstName": "B2"}
]
```
**Step 2 - Get batch1:** `GET /user/batch1`  
**Step 3 - Get batch2:** `GET /user/batch2`

**Test Case Explanation:**  
Tests that batch-created users can be individually retrieved.

**Expected Result:**
- Batch create: HTTP Status Code: 200
- GET batch1: HTTP Status Code: 200, data returned
- GET batch2: HTTP Status Code: 200, data returned
- All users individually accessible

---

## 3.3 GET /user/login - Login User

### Test Case 3.3.1: Positive Test - Login with Valid Credentials

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=theUser&password=12345`  
**Test Data:**
- Query parameter: `username=theUser`
- Query parameter: `password=12345`

**Test Case Explanation:**  
Tests successful login with valid username and password.

**Expected Result:**
- HTTP Status Code: 200
- Response contains authentication token/session info
- Response headers include X-Rate-Limit and X-Expires-After
- Response format: JSON or XML string (token/session)

---

### Test Case 3.3.2: Positive Test - Login Case Sensitivity

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=theuser&password=12345`  
**Test Data:**
- Query parameter: `username=theuser` (lowercase)
- Query parameter: `password=12345`

**Test Case Explanation:**  
Tests whether login is case-sensitive for usernames.

**Expected Result:**
- HTTP Status Code: 200 (if case-insensitive) OR
- HTTP Status Code: 400 (if case-sensitive and no lowercase user exists)
- Behavior documented

---

### Test Case 3.3.3: Negative Test - Invalid Password

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=theUser&password=wrongpassword`  
**Test Data:**
- Query parameter: `username=theUser`
- Query parameter: `password=wrongpassword`

**Test Case Explanation:**  
Tests login with incorrect password for existing user.

**Expected Result:**
- HTTP Status Code: 400 (Invalid username/password supplied)
- No authentication token provided
- Error message indicates login failed

---

### Test Case 3.3.4: Negative Test - Non-Existent User Login

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=nonexistentuser&password=anypass`  
**Test Data:**
- Query parameter: `username=nonexistentuser`
- Query parameter: `password=anypass`

**Test Case Explanation:**  
Tests login attempt with username that doesn't exist.

**Expected Result:**
- HTTP Status Code: 400 (Invalid username/password supplied)
- No token issued
- Clear error message

---

### Test Case 3.3.5: Negative Test - Missing Credentials

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login`  
**Test Data:** No query parameters

**Test Case Explanation:**  
Tests login without providing username or password. Both marked as optional in spec but required functionally.

**Expected Result:**
- HTTP Status Code: 400 (Invalid username/password supplied) OR
- HTTP Status Code: 200 (if optional and treated as no-op)
- Behavior with missing credentials documented

---

### Test Case 3.3.6: Boundary Test - Empty Username

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=&password=12345`  
**Test Data:**
- Query parameter: `username=` (empty)
- Query parameter: `password=12345`

**Test Case Explanation:**  
Tests login with empty username string.

**Expected Result:**
- HTTP Status Code: 400 (Invalid credentials)
- Login fails

---

### Test Case 3.3.7: Boundary Test - Special Characters in Credentials

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/login?username=user%40domain&password=p%40ssw0rd%21`  
**Test Data:**
- Credentials with special characters: @, !, etc.

**Test Case Explanation:**  
Tests login with special characters in username/password (URL encoded).

**Expected Result:**
- HTTP Status Code: 200 or 400 depending on credentials
- Special characters properly decoded
- No injection vulnerabilities

---

## 3.4 GET /user/logout - Logout User

### Test Case 3.4.1: Positive Test - Logout without Authentication

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/logout`  
**Test Data:** No parameters

**Test Case Explanation:**  
Tests logout operation. API allows logout without explicit authentication (session-based).

**Expected Result:**
- HTTP Status Code: 200
- Response indicates successful logout
- Current session terminated

---

### Test Case 3.4.2: Positive Test - Logout After Login

**Scenario Type:** Positive  
**Step 1 - Login:** `GET /user/login?username=theUser&password=12345`  
**Step 2 - Logout:** `GET /user/logout`

**Test Case Explanation:**  
Tests logout flow after successful login.

**Expected Result:**
- Login: HTTP Status Code: 200, token returned
- Logout: HTTP Status Code: 200
- Session properly terminated

---

### Test Case 3.4.3: Regression Test - Cannot Use Token After Logout

**Scenario Type:** Regression  
**Step 1:** Login and get token  
**Step 2:** Logout  
**Step 3:** Try to access protected endpoint with token

**Test Case Explanation:**  
Tests that token is invalidated after logout.

**Expected Result:**
- Logout: HTTP Status Code: 200
- Subsequent request with old token: Should be rejected
- Token properly invalidated

---

## 3.5 GET /user/{username} - Get User by Username

### Test Case 3.5.1: Positive Test - Get Existing User

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:** Path parameter `username=theUser`  

**Test Case Explanation:**  
Tests retrieval of user by username. API docs suggest "user1" for testing.

**Expected Result:**
- HTTP Status Code: 200
- Response contains User object with matching username
- All user fields returned

---

### Test Case 3.5.2: Positive Test - Get User "user1"

**Scenario Type:** Positive  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/user1`  
**Test Data:** Path parameter `username=user1`  

**Test Case Explanation:**  
Uses example username from API documentation.

**Expected Result:**
- HTTP Status Code: 200
- User1 data returned if exists
- Standard test case

---

### Test Case 3.5.3: Negative Test - Get Non-Existent User

**Scenario Type:** Negative  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/nonexistentuser123`  
**Test Data:** Path parameter `username=nonexistentuser123`  

**Test Case Explanation:**  
Tests retrieval of user that doesn't exist.

**Expected Result:**
- HTTP Status Code: 404 (User not found)
- Error message indicates user not found
- No default user returned

---

### Test Case 3.5.4: Boundary Test - Empty Username

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/`  (empty username in path)  
**Test Data:** Path parameter `username=` (empty)

**Test Case Explanation:**  
Tests GET with empty username path parameter.

**Expected Result:**
- HTTP Status Code: 400 or 404
- Error message for empty username
- No user operation on empty string

---

### Test Case 3.5.5: Boundary Test - Special Characters in Username

**Scenario Type:** Boundary  
**Test URL:** `GET https://petstore3.swagger.io/api/v3/user/user%40special`  
**Test Data:** Path parameter with special characters

**Test Case Explanation:**  
Tests retrieval with special characters in username.

**Expected Result:**
- HTTP Status Code: 200 (if user exists) or 404 (if not found)
- Special characters properly decoded
- No URL injection

---

### Test Case 3.5.6: Regression Test - Verify Retrieved Data Matches Created User

**Scenario Type:** Regression  
**Step 1 - Create User:**
```json
{
  "username": "verifyuser",
  "firstName": "Verify",
  "email": "verify@test.com"
}
```
**Step 2 - Get User:** `GET /user/verifyuser`

**Test Case Explanation:**  
Tests that retrieved user data matches what was created.

**Expected Result:**
- Create: HTTP Status Code: 200
- Get: HTTP Status Code: 200
- Retrieved fields match created data exactly

---

## 3.6 PUT /user/{username} - Update User

### Test Case 3.6.1: Positive Test - Update User All Fields

**Scenario Type:** Positive  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:**
```json
{
  "id": 1,
  "username": "theUser",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "password": "newpassword123",
  "phone": "5559876543",
  "userStatus": 2
}
```

**Test Case Explanation:**  
Tests complete user profile update with all fields.

**Expected Result:**
- HTTP Status Code: 200
- User record updated with all new values
- Changes persisted in system

---

### Test Case 3.6.2: Positive Test - Update User Partial Data

**Scenario Type:** Positive  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:**
```json
{
  "firstName": "Jane",
  "email": "jane@example.com"
}
```

**Test Case Explanation:**  
Tests partial update with only specific fields.

**Expected Result:**
- HTTP Status Code: 200
- firstName and email updated
- Other fields remain unchanged
- No required field validation for PUT

---

### Test Case 3.6.3: Positive Test - Update User Password Only

**Scenario Type:** Positive  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:**
```json
{
  "password": "brandnewpassword"
}
```

**Test Case Explanation:**  
Tests updating only password field.

**Expected Result:**
- HTTP Status Code: 200
- User password changed
- Other user fields unaffected

---

### Test Case 3.6.4: Negative Test - Update Non-Existent User

**Scenario Type:** Negative  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/user/nonexistentuser`  
**Test Data:**
```json
{
  "firstName": "Test"
}
```

**Test Case Explanation:**  
Tests update attempt on user that doesn't exist.

**Expected Result:**
- HTTP Status Code: 404 (user not found) OR
- HTTP Status Code: 400 (bad request)
- Clear error message
- New user not created

---

### Test Case 3.6.5: Boundary Test - Update with Empty Fields

**Scenario Type:** Boundary  
**Test URL:** `PUT https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:**
```json
{
  "firstName": "",
  "email": "",
  "phone": ""
}
```

**Test Case Explanation:**  
Tests update with empty string values for fields.

**Expected Result:**
- HTTP Status Code: 200 or 400
- If accepted: fields cleared
- If rejected: error message for empty fields

---

### Test Case 3.6.6: Regression Test - Update and Verify Changes Persist

**Scenario Type:** Regression  
**Step 1 - Update:** `PUT /user/testuser` with new data
**Step 2 - Get:** `GET /user/testuser`

**Test Case Explanation:**  
Tests that updates are persisted and retrievable.

**Expected Result:**
- Update: HTTP Status Code: 200
- Get: HTTP Status Code: 200
- Retrieved data matches updated values
- Changes persist across requests

---

## 3.7 DELETE /user/{username} - Delete User

### Test Case 3.7.1: Positive Test - Delete Existing User

**Scenario Type:** Positive  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/user/theUser`  
**Test Data:** Path parameter `username=theUser`  

**Test Case Explanation:**  
Tests successful deletion of user.

**Expected Result:**
- HTTP Status Code: 200 (User deleted)
- User removed from system
- Cannot retrieve user after deletion

---

### Test Case 3.7.2: Negative Test - Delete Non-Existent User

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/user/nonexistentuser123`  
**Test Data:** Path parameter `username=nonexistentuser123`  

**Test Case Explanation:**  
Tests deletion of user that doesn't exist.

**Expected Result:**
- HTTP Status Code: 404 (User not found) OR
- HTTP Status Code: 200 (idempotent delete)
- Clear documentation of behavior

---

### Test Case 3.7.3: Negative Test - Invalid Username for Delete

**Scenario Type:** Negative  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/user/`  (empty username)

**Test Case Explanation:**  
Tests deletion with empty username.

**Expected Result:**
- HTTP Status Code: 400 (Invalid username supplied)
- Error message for missing username

---

### Test Case 3.7.4: Boundary Test - Special Characters in Username

**Scenario Type:** Boundary  
**Test URL:** `DELETE https://petstore3.swagger.io/api/v3/user/user%40special%21`  
**Test Data:** Username with special characters

**Test Case Explanation:**  
Tests deletion of user with special characters in username.

**Expected Result:**
- HTTP Status Code: 200 (if user exists) or 404
- Special characters properly decoded
- No encoding issues

---

### Test Case 3.7.5: Regression Test - Delete and Verify Non-Existence

**Scenario Type:** Regression  
**Step 1 - Delete:** `DELETE /user/deletetest`  
**Step 2 - Get:** `GET /user/deletetest`

**Test Case Explanation:**  
Tests that deleting user makes them unretrievable.

**Expected Result:**
- Delete: HTTP Status Code: 200 (if exists)
- Get: HTTP Status Code: 404 (user not found)
- User completely removed from system

---

### Test Case 3.7.6: Regression Test - Double Delete Idempotency

**Scenario Type:** Regression  
**Step 1:** `DELETE /user/doubletest` (first delete)  
**Step 2:** `DELETE /user/doubletest` (second delete)

**Test Case Explanation:**  
Tests that deleting same user twice doesn't cause issues.

**Expected Result:**
- First delete: HTTP Status Code: 200 (if exists)
- Second delete: HTTP Status Code: 200 or 404
- No errors or side effects from double delete

---

---

# 4. CROSS-ENDPOINT REGRESSION TESTS

## 4.1 Pet Lifecycle Test

**Scenario Type:** Regression  
**Test Steps:**
1. Create new pet via POST /pet
2. Retrieve pet via GET /pet/{petId}
3. Update pet via PUT /pet
4. Find pets via GET /pet/findByStatus
5. Upload image via POST /pet/{petId}/uploadImage
6. Delete pet via DELETE /pet/{petId}
7. Verify GET /pet/{petId} returns 404

**Expected Results:**
- All operations succeed in sequence
- Pet data persists correctly across operations
- Delete properly removes pet from all queries

---

## 4.2 Store Operations Test

**Scenario Type:** Regression  
**Test Steps:**
1. Get initial inventory via GET /store/inventory
2. Create order via POST /store/order
3. Retrieve order via GET /store/order/{orderId}
4. Verify inventory changes if order affects pet counts
5. Delete order via DELETE /store/order/{orderId}
6. Verify order no longer retrievable

**Expected Results:**
- Orders properly tracked
- Inventory reflects order operations
- Delete removes order from system

---

## 4.3 User Lifecycle Test

**Scenario Type:** Regression  
**Test Steps:**
1. Create user via POST /user
2. Login user via GET /user/login
3. Retrieve user via GET /user/{username}
4. Update user via PUT /user/{username}
5. Logout via GET /user/logout
6. Login again to verify changes persisted
7. Delete user via DELETE /user/{username}
8. Verify cannot retrieve deleted user

**Expected Results:**
- User lifecycle complete successfully
- Login/logout work correctly
- Updates persist across session
- Deletion permanent

---

## 4.4 Concurrent Operation Test

**Scenario Type:** Regression  
**Test Steps:**
1. Create multiple pets simultaneously
2. Query inventory while creating pets
3. Create multiple users simultaneously
4. Verify all operations complete without data corruption

**Expected Results:**
- No race conditions
- Concurrent operations don't corrupt data
- All created entities persisted correctly

---

---

# 5. SECURITY & AUTHENTICATION TESTS

## 5.1 API Key Authentication Test

**Scenario Type:** Security  
**Test Steps:**
1. Test endpoint with valid API key
2. Test endpoint without API key (if required)
3. Test endpoint with invalid API key

**Expected Results:**
- Valid key: Operations succeed
- Missing key: 401/403 error if required
- Invalid key: 401/403 error

---

## 5.2 OAuth2 Scope Verification

**Scenario Type:** Security  
**Test Steps:**
1. Login with `read:pets` scope
2. Attempt write operations (should fail)
3. Login with `write:pets` scope
4. Verify write operations succeed

**Expected Results:**
- Scopes properly enforced
- Read-only tokens can't perform writes
- Write tokens allow writes with reads

---

---

# Test Summary

**Total Test Scenarios:** 100+  
**API Endpoints Covered:** 18  
**Scenario Types:**
- Positive Tests: ~30
- Negative Tests: ~35
- Boundary Tests: ~25
- Regression Tests: ~15+

**Recommendations:**
1. Automate all test cases using test framework (Postman, RestAssured, etc.)
2. Run full test suite before each release
3. Monitor execution time and coverage metrics
4. Update tests when API specification changes
5. Document any API behavior deviations from OpenAPI spec

---

**Report Generated:** March 1, 2026  
**Tester:** Senior Software Testing Professional  
**Status:** Ready for Execution
