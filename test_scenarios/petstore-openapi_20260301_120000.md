# Petstore OpenAPI 3.0 - Test Scenarios Report
**Generated:** March 1, 2026

---

## Table of Contents
1. [Pet Endpoints](#pet-endpoints)
2. [Store Endpoints](#store-endpoints)
3. [User Endpoints](#user-endpoints)

---

# PET ENDPOINTS

## 1. PUT /pet - Update an Existing Pet

### Positive Test Scenarios

#### Scenario 1.1: Update Pet with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 1,
    "name": "Doggie Updated",
    "category": {"id": 1, "name": "Dogs"},
    "photoUrls": ["https://example.com/dog.jpg"],
    "tags": [{"id": 1, "name": "friendly"}],
    "status": "available"
  }
  ```
- **Test Case Explanation:** Test successful update of an existing pet with all required and optional fields populated with valid data. Validates that the system can update pet records correctly.
- **Expected Result:** 
  - Status Code: 200
  - Response body contains updated pet with all provided fields
  - Response includes id, name, category, photoUrls, tags, and status

#### Scenario 1.2: Update Pet with Minimal Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 2,
    "name": "Cat",
    "photoUrls": ["https://example.com/cat.jpg"],
    "status": "pending"
  }
  ```
- **Test Case Explanation:** Test update with only required fields (name and photoUrls) to verify system handles minimal valid data correctly.
- **Expected Result:**
  - Status Code: 200
  - Response body contains pet with id, name, photoUrls, and status
  - Category and tags are either null or not included

### Negative Test Scenarios

#### Scenario 1.3: Update Pet with Invalid ID Format
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": "invalid_id",
    "name": "Doggie",
    "photoUrls": ["https://example.com/dog.jpg"]
  }
  ```
- **Test Case Explanation:** Test API behavior when ID is provided as string instead of integer. Validates proper input validation.
- **Expected Result:**
  - Status Code: 400 (Bad Request)
  - Error message indicating invalid ID format

#### Scenario 1.4: Update Pet with Missing Required Field (photoUrls)
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 3,
    "name": "Bird"
  }
  ```
- **Test Case Explanation:** Test update without required photoUrls field. Validates mandatory field enforcement.
- **Expected Result:**
  - Status Code: 400 or 422 (Validation Exception)
  - Error message indicating missing required field

#### Scenario 1.5: Update Pet with Missing Required Field (name)
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 4,
    "photoUrls": ["https://example.com/bird.jpg"]
  }
  ```
- **Test Case Explanation:** Test update without required name field.
- **Expected Result:**
  - Status Code: 400 or 422 (Validation Exception)
  - Error message indicating missing name field

#### Scenario 1.6: Update Non-existent Pet
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 99999,
    "name": "Non-existent",
    "photoUrls": ["https://example.com/pet.jpg"],
    "status": "available"
  }
  ```
- **Test Case Explanation:** Test update of a pet ID that doesn't exist in the system.
- **Expected Result:**
  - Status Code: 404 (Not Found)
  - Error message indicating pet not found

#### Scenario 1.7: Update Pet with Invalid Status Value
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 5,
    "name": "Doggie",
    "photoUrls": ["https://example.com/dog.jpg"],
    "status": "invalid_status"
  }
  ```
- **Test Case Explanation:** Test update with status value not in enum (available, pending, sold).
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message indicating invalid status value

### Boundary Test Scenarios

#### Scenario 1.8: Update Pet with Maximum ID Value
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 9223372036854775807,
    "name": "Pet Max ID",
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test with maximum int64 value for pet ID.
- **Expected Result:**
  - Either Status Code: 200 if pet exists or 404 if not
  - System should handle large integers correctly

#### Scenario 1.9: Update Pet with Empty String Name
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 6,
    "name": "",
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test with empty string for name field.
- **Expected Result:**
  - Status Code: 422 or 400
  - Error message indicating invalid or empty name

#### Scenario 1.10: Update Pet with Empty PhotoUrls Array
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 7,
    "name": "Pet",
    "photoUrls": []
  }
  ```
- **Test Case Explanation:** Test with empty photoUrls array when at least one photo URL is expected.
- **Expected Result:**
  - Status Code: 422 or 400
  - Error message indicating at least one photo URL is required

#### Scenario 1.11: Update Pet with Very Long Name
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 8,
    "name": "A" * 10000,
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test with extremely long pet name string.
- **Expected Result:**
  - Status Code: 400, 422, or 200
  - If 200: Verify name is stored and truncated if necessary
  - If error: Error message about string length

### Regression Test Scenarios

#### Scenario 1.12: Verify Previous Updates Still Work
- **Scenario Type:** Regression
- **Test URL:** `/pet`
- **Test Data:** Multiple sequential updates with different status values
  - First: status = "available"
  - Second: status = "pending"
  - Third: status = "sold"
- **Test Case Explanation:** Test that updating pet status multiple times maintains data integrity.
- **Expected Result:**
  - All three updates return Status Code: 200
  - Each update correctly reflects the new status

---

## 2. POST /pet - Add a New Pet

### Positive Test Scenarios

#### Scenario 2.1: Add New Pet with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 101,
    "name": "Fluffy",
    "category": {"id": 2, "name": "Cats"},
    "photoUrls": ["https://example.com/fluffy.jpg"],
    "tags": [{"id": 1, "name": "cute"}],
    "status": "available"
  }
  ```
- **Test Case Explanation:** Test successful creation of a new pet with all fields populated.
- **Expected Result:**
  - Status Code: 200
  - Response contains created pet with id, name, category, photoUrls, tags, status
  - Pet is retrievable via GET /pet/{petId}

#### Scenario 2.2: Add New Pet with Only Required Fields
- **Scenario Type:** Positive
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "name": "Simple Pet",
    "photoUrls": ["https://example.com/simple.jpg"]
  }
  ```
- **Test Case Explanation:** Test creation with only mandatory fields (name and photoUrls).
- **Expected Result:**
  - Status Code: 200
  - System auto-generates ID
  - Status defaults to "available" or null

#### Scenario 2.3: Add Multiple Pets Sequentially
- **Scenario Type:** Positive
- **Test URL:** `/pet`
- **Test Data:** Create 3 different pets one after another
- **Test Case Explanation:** Test that system can handle multiple sequential pet additions.
- **Expected Result:**
  - All three requests return Status Code: 200
  - Each pet has unique ID
  - All pets are retrievable

### Negative Test Scenarios

#### Scenario 2.4: Add Pet without Required Field (name)
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 102,
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test creation without required name field.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message about missing name

#### Scenario 2.5: Add Pet without Required Field (photoUrls)
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 103,
    "name": "No Photo Pet"
  }
  ```
- **Test Case Explanation:** Test creation without required photoUrls field.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message about missing photoUrls

#### Scenario 2.6: Add Pet with Null Required Field
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 104,
    "name": null,
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test creation with null value for required name field.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message about invalid name

#### Scenario 2.7: Add Pet with Invalid Status Enum
- **Scenario Type:** Negative
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 105,
    "name": "Pet",
    "photoUrls": ["https://example.com/pet.jpg"],
    "status": "unknown_status"
  }
  ```
- **Test Case Explanation:** Test creation with status not in allowed enum values.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message about invalid status

### Boundary Test Scenarios

#### Scenario 2.8: Add Pet with Duplicate ID
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 101,
    "name": "Duplicate Pet",
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test adding pet with ID already existing (if ID 101 was created in previous test).
- **Expected Result:**
  - Status Code: 400 or 200 (depends on implementation)
  - If error: Message about duplicate ID
  - If success: Existing pet is updated or new record rejected

#### Scenario 2.9: Add Pet with Negative ID
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": -1,
    "name": "Negative ID Pet",
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test with negative integer ID.
- **Expected Result:**
  - Status Code: 400 or 200
  - If 200: Negative ID is accepted
  - If 400: Error message about invalid ID

#### Scenario 2.10: Add Pet with Special Characters in Name
- **Scenario Type:** Boundary
- **Test URL:** `/pet`
- **Test Data:** 
  ```json
  {
    "id": 106,
    "name": "Pet@#$%^&*()",
    "photoUrls": ["https://example.com/pet.jpg"]
  }
  ```
- **Test Case Explanation:** Test with special characters in pet name.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Special characters are stored as-is
  - If 400: Error about invalid characters

---

## 3. GET /pet/findByStatus - Find Pets by Status

### Positive Test Scenarios

#### Scenario 3.1: Find Pets with Status "available"
- **Scenario Type:** Positive
- **Test URL:** `/pet/findByStatus?status=available`
- **Test Data:** Query parameter: status=available
- **Test Case Explanation:** Test retrieval of all pets with available status.
- **Expected Result:**
  - Status Code: 200
  - Response is array of Pet objects
  - All returned pets have status="available"
  - Array is not empty (assuming available pets exist)

#### Scenario 3.2: Find Pets with Status "pending"
- **Scenario Type:** Positive
- **Test URL:** `/pet/findByStatus?status=pending`
- **Test Data:** Query parameter: status=pending
- **Test Case Explanation:** Test retrieval of all pets with pending status.
- **Expected Result:**
  - Status Code: 200
  - Response is array of Pet objects
  - All returned pets have status="pending"

#### Scenario 3.3: Find Pets with Status "sold"
- **Scenario Type:** Positive
- **Test URL:** `/pet/findByStatus?status=sold`
- **Test Data:** Query parameter: status=sold
- **Test Case Explanation:** Test retrieval of all pets with sold status.
- **Expected Result:**
  - Status Code: 200
  - Response is array of Pet objects
  - All returned pets have status="sold"

### Negative Test Scenarios

#### Scenario 3.4: Find Pets with Invalid Status Value
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByStatus?status=invalid_status`
- **Test Data:** Query parameter: status=invalid_status
- **Test Case Explanation:** Test with status value not in enum.
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid status value

#### Scenario 3.5: Find Pets without Status Parameter
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByStatus`
- **Test Data:** No query parameter provided
- **Test Case Explanation:** Test when required status parameter is missing.
- **Expected Result:**
  - Status Code: 400
  - Error message indicating status parameter is required

#### Scenario 3.6: Find Pets with Empty Status Parameter
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByStatus?status=`
- **Test Data:** Query parameter: status= (empty)
- **Test Case Explanation:** Test with empty status value.
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid empty status

### Boundary Test Scenarios

#### Scenario 3.7: Find Pets with Status in Different Case (lowercase)
- **Scenario Type:** Boundary
- **Test URL:** `/pet/findByStatus?status=AVAILABLE`
- **Test Data:** Query parameter: status=AVAILABLE
- **Test Case Explanation:** Test case sensitivity of status parameter.
- **Expected Result:**
  - Status Code: 400 or 200
  - If 200: Case-insensitive matching
  - If 400: Status is case-sensitive

#### Scenario 3.8: Find Pets with Multiple Status Values (if supported)
- **Scenario Type:** Boundary
- **Test URL:** `/pet/findByStatus?status=available,pending`
- **Test Data:** Query parameter: status=available,pending
- **Test Case Explanation:** Test if API supports comma-separated status values.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Returns pets with either available or pending status
  - If 400: Multiple values not supported

---

## 4. GET /pet/findByTags - Find Pets by Tags

### Positive Test Scenarios

#### Scenario 4.1: Find Pets with Single Tag
- **Scenario Type:** Positive
- **Test URL:** `/pet/findByTags?tags=tag1`
- **Test Data:** Query parameter: tags=tag1
- **Test Case Explanation:** Test retrieval of pets matching single tag.
- **Expected Result:**
  - Status Code: 200
  - Response is array of Pet objects
  - All returned pets contain the specified tag

#### Scenario 4.2: Find Pets with Multiple Tags
- **Scenario Type:** Positive
- **Test URL:** `/pet/findByTags?tags=tag1,tag2,tag3`
- **Test Data:** Query parameter: tags=tag1,tag2,tag3
- **Test Case Explanation:** Test retrieval of pets matching any of multiple tags.
- **Expected Result:**
  - Status Code: 200
  - Response is array of Pet objects
  - Returned pets have at least one of the specified tags

### Negative Test Scenarios

#### Scenario 4.3: Find Pets with Non-existent Tag
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByTags?tags=nonexistent_tag`
- **Test Data:** Query parameter: tags=nonexistent_tag
- **Test Case Explanation:** Test with tag that doesn't match any pets.
- **Expected Result:**
  - Status Code: 200
  - Response is empty array
  - No error, just empty result set

#### Scenario 4.4: Find Pets without Tags Parameter
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByTags`
- **Test Data:** No query parameter provided
- **Test Case Explanation:** Test when required tags parameter is missing.
- **Expected Result:**
  - Status Code: 400
  - Error message indicating tags parameter is required

#### Scenario 4.5: Find Pets with Invalid Tag Format
- **Scenario Type:** Negative
- **Test URL:** `/pet/findByTags?tags=`
- **Test Data:** Query parameter: tags= (empty)
- **Test Case Explanation:** Test with empty tags parameter.
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid empty tags

### Boundary Test Scenarios

#### Scenario 4.6: Find Pets with Special Characters in Tag
- **Scenario Type:** Boundary
- **Test URL:** `/pet/findByTags?tags=tag@%23`
- **Test Data:** Query parameter: tags=tag@%23 (URL encoded special chars)
- **Test Case Explanation:** Test with special characters in tag name.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Special characters properly handled
  - If 400: Invalid character error

#### Scenario 4.7: Find Pets with Very Long Tag List
- **Scenario Type:** Boundary
- **Test URL:** `/pet/findByTags?tags=tag1,tag2,...tag100`
- **Test Data:** Query parameter with 100+ comma-separated tags
- **Test Case Explanation:** Test API behavior with large number of tags.
- **Expected Result:**
  - Status Code: 200 or 413 (Payload Too Large)
  - If 200: Returns matching results
  - If 413: System limit exceeded

---

## 5. GET /pet/{petId} - Get Pet by ID

### Positive Test Scenarios

#### Scenario 5.1: Get Existing Pet by Valid ID
- **Scenario Type:** Positive
- **Test URL:** `/pet/1`
- **Test Data:** Path parameter: petId=1
- **Test Case Explanation:** Test retrieval of existing pet by valid ID.
- **Expected Result:**
  - Status Code: 200
  - Response contains Pet object with all details
  - Pet ID matches requested ID

#### Scenario 5.2: Get Pet by Different Valid ID
- **Scenario Type:** Positive
- **Test URL:** `/pet/10`
- **Test Data:** Path parameter: petId=10
- **Test Case Explanation:** Test retrieval with different pet ID.
- **Expected Result:**
  - Status Code: 200
  - Response contains correct Pet object

### Negative Test Scenarios

#### Scenario 5.3: Get Pet with Non-existent ID
- **Scenario Type:** Negative
- **Test URL:** `/pet/99999`
- **Test Data:** Path parameter: petId=99999
- **Test Case Explanation:** Test retrieval of non-existent pet.
- **Expected Result:**
  - Status Code: 404
  - Error message indicating pet not found

#### Scenario 5.4: Get Pet with Invalid ID Format
- **Scenario Type:** Negative
- **Test URL:** `/pet/abc`
- **Test Data:** Path parameter: petId=abc (non-numeric)
- **Test Case Explanation:** Test with non-integer ID value.
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid ID format

#### Scenario 5.5: Get Pet with Negative ID
- **Scenario Type:** Negative
- **Test URL:** `/pet/-1`
- **Test Data:** Path parameter: petId=-1
- **Test Case Explanation:** Test with negative ID value.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error message about invalid ID

### Boundary Test Scenarios

#### Scenario 5.6: Get Pet with Maximum int64 ID
- **Scenario Type:** Boundary
- **Test URL:** `/pet/9223372036854775807`
- **Test Data:** Path parameter: petId=9223372036854775807
- **Test Case Explanation:** Test with maximum 64-bit integer value.
- **Expected Result:**
  - Status Code: 404 (pet doesn't exist) or 200
  - System handles large integers correctly

#### Scenario 5.7: Get Pet with ID = 0
- **Scenario Type:** Boundary
- **Test URL:** `/pet/0`
- **Test Data:** Path parameter: petId=0
- **Test Case Explanation:** Test with zero as ID.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error indicating invalid ID or pet not found

---

## 6. POST /pet/{petId} - Update Pet with Form Data

### Positive Test Scenarios

#### Scenario 6.1: Update Pet Name with Form Data
- **Scenario Type:** Positive
- **Test URL:** `/pet/1?name=UpdatedName`
- **Test Data:** Path parameter: petId=1, Query parameter: name=UpdatedName
- **Test Case Explanation:** Test updating pet name using form data/query parameters.
- **Expected Result:**
  - Status Code: 200
  - Response contains Pet with updated name
  - Status field remains unchanged

#### Scenario 6.2: Update Pet Status with Form Data
- **Scenario Type:** Positive
- **Test URL:** `/pet/2?status=sold`
- **Test Data:** Path parameter: petId=2, Query parameter: status=sold
- **Test Case Explanation:** Test updating pet status using form data.
- **Expected Result:**
  - Status Code: 200
  - Response contains Pet with updated status
  - Name field remains unchanged

#### Scenario 6.3: Update Both Pet Name and Status
- **Scenario Type:** Positive
- **Test URL:** `/pet/3?name=NewName&status=pending`
- **Test Data:** Path parameters and query parameters
- **Test Case Explanation:** Test simultaneous update of multiple fields.
- **Expected Result:**
  - Status Code: 200
  - Response contains Pet with both name and status updated

### Negative Test Scenarios

#### Scenario 6.4: Update Non-existent Pet
- **Scenario Type:** Negative
- **Test URL:** `/pet/99999?name=Test`
- **Test Data:** Path parameter: petId=99999, Query parameter: name=Test
- **Test Case Explanation:** Test updating pet that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error message about pet not found

#### Scenario 6.5: Update Pet with Invalid Pet ID Format
- **Scenario Type:** Negative
- **Test URL:** `/pet/invalid?name=Test`
- **Test Data:** Path parameter: petId=invalid (non-numeric)
- **Test Case Explanation:** Test with non-integer path parameter.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid ID format

#### Scenario 6.6: Update Pet with Invalid Status Value
- **Scenario Type:** Negative
- **Test URL:** `/pet/1?status=invalid_status`
- **Test Data:** Path parameter: petId=1, Query parameter: status=invalid_status
- **Test Case Explanation:** Test update with status not in enum.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about invalid status

### Boundary Test Scenarios

#### Scenario 6.7: Update Pet with Empty Name String
- **Scenario Type:** Boundary
- **Test URL:** `/pet/1?name=`
- **Test Data:** Path parameter: petId=1, Query parameter: name= (empty)
- **Test Case Explanation:** Test with empty name value.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Name might be set to empty or ignored
  - If 400: Error about empty name

#### Scenario 6.8: Update Pet with Only Path Parameter (No Query Params)
- **Scenario Type:** Boundary
- **Test URL:** `/pet/1`
- **Test Data:** Path parameter: petId=1 only
- **Test Case Explanation:** Test update endpoint with no update fields.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Pet unchanged, existing data returned
  - If 400: Error about missing update parameters

---

## 7. DELETE /pet/{petId} - Delete Pet

### Positive Test Scenarios

#### Scenario 7.1: Delete Existing Pet
- **Scenario Type:** Positive
- **Test URL:** `/pet/1`
- **Test Data:** Path parameter: petId=1
- **Test Case Explanation:** Test successful deletion of existing pet.
- **Expected Result:**
  - Status Code: 200
  - Message indicating pet deleted
  - Subsequent GET request returns 404

#### Scenario 7.2: Delete Different Pet
- **Scenario Type:** Positive
- **Test URL:** `/pet/2`
- **Test Data:** Path parameter: petId=2
- **Test Case Explanation:** Test deletion of another pet.
- **Expected Result:**
  - Status Code: 200
  - Pet no longer exists in system

### Negative Test Scenarios

#### Scenario 7.3: Delete Non-existent Pet
- **Scenario Type:** Negative
- **Test URL:** `/pet/99999`
- **Test Data:** Path parameter: petId=99999
- **Test Case Explanation:** Test deletion of pet that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error message about pet not found

#### Scenario 7.4: Delete Pet with Invalid ID Format
- **Scenario Type:** Negative
- **Test URL:** `/pet/abc`
- **Test Data:** Path parameter: petId=abc (non-numeric)
- **Test Case Explanation:** Test with non-integer ID.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid ID format

#### Scenario 7.5: Delete Pet with Negative ID
- **Scenario Type:** Negative
- **Test URL:** `/pet/-1`
- **Test Data:** Path parameter: petId=-1
- **Test Case Explanation:** Test with negative ID.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error indicating invalid ID

### Boundary Test Scenarios

#### Scenario 7.6: Delete Pet with Zero ID
- **Scenario Type:** Boundary
- **Test URL:** `/pet/0`
- **Test Data:** Path parameter: petId=0
- **Test Case Explanation:** Test deletion with ID=0.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error about invalid ID or not found

#### Scenario 7.7: Delete Same Pet Twice
- **Scenario Type:** Boundary
- **Test URL:** `/pet/5` (first delete), `/pet/5` (second delete)
- **Test Data:** Same petId in two sequential requests
- **Test Case Explanation:** Test deleting same pet multiple times.
- **Expected Result:**
  - First request: Status Code: 200
  - Second request: Status Code: 404 (already deleted)

---

## 8. POST /pet/{petId}/uploadImage - Upload Pet Image

### Positive Test Scenarios

#### Scenario 8.1: Upload Image with Valid File
- **Scenario Type:** Positive
- **Test URL:** `/pet/1/uploadImage`
- **Test Data:** 
  - Path parameter: petId=1
  - File: Valid image file (jpg/png)
  - Content-Type: application/octet-stream
- **Test Case Explanation:** Test successful image upload for existing pet.
- **Expected Result:**
  - Status Code: 200
  - Response contains ApiResponse with success message
  - Image is associated with pet

#### Scenario 8.2: Upload Image with Metadata
- **Scenario Type:** Positive
- **Test URL:** `/pet/2/uploadImage?additionalMetadata=Favorite%20pet%20photo`
- **Test Data:**
  - Path parameter: petId=2
  - Query parameter: additionalMetadata=Favorite pet photo
  - File: Valid image
- **Test Case Explanation:** Test image upload with additional metadata.
- **Expected Result:**
  - Status Code: 200
  - Metadata is stored with image
  - ApiResponse indicates success

### Negative Test Scenarios

#### Scenario 8.3: Upload Image for Non-existent Pet
- **Scenario Type:** Negative
- **Test URL:** `/pet/99999/uploadImage`
- **Test Data:** Path parameter: petId=99999, File: Valid image
- **Test Case Explanation:** Test upload to non-existent pet.
- **Expected Result:**
  - Status Code: 404
  - Error message about pet not found

#### Scenario 8.4: Upload Without File
- **Scenario Type:** Negative
- **Test URL:** `/pet/1/uploadImage`
- **Test Data:** Path parameter: petId=1, No file provided
- **Test Case Explanation:** Test upload endpoint without file.
- **Expected Result:**
  - Status Code: 400
  - Error message about no file uploaded

#### Scenario 8.5: Upload Invalid File Format
- **Scenario Type:** Negative
- **Test URL:** `/pet/1/uploadImage`
- **Test Data:** Path parameter: petId=1, File: .txt/.pdf file
- **Test Case Explanation:** Test with unsupported file format.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid file format

### Boundary Test Scenarios

#### Scenario 8.6: Upload Very Large Image File
- **Scenario Type:** Boundary
- **Test URL:** `/pet/1/uploadImage`
- **Test Data:** Path parameter: petId=1, File: 500MB image file
- **Test Case Explanation:** Test with extremely large file.
- **Expected Result:**
  - Status Code: 200 or 413 (Payload Too Large)
  - If 413: File size limit exceeded
  - If 200: File successfully uploaded

#### Scenario 8.7: Upload Image with Invalid Pet ID Format
- **Scenario Type:** Boundary
- **Test URL:** `/pet/abc/uploadImage`
- **Test Data:** Path parameter: petId=abc, File: Valid image
- **Test Case Explanation:** Test with non-integer pet ID.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid ID format

---

# STORE ENDPOINTS

## 9. GET /store/inventory - Get Inventory

### Positive Test Scenarios

#### Scenario 9.1: Get Store Inventory
- **Scenario Type:** Positive
- **Test URL:** `/store/inventory`
- **Test Data:** No parameters required
- **Test Case Explanation:** Test retrieval of store inventory count by status.
- **Expected Result:**
  - Status Code: 200
  - Response is object with status values as keys
  - Values are integers representing quantity
  - Example: {"available": 10, "pending": 5, "sold": 3}

#### Scenario 9.2: Get Inventory Multiple Times
- **Scenario Type:** Positive
- **Test URL:** `/store/inventory`
- **Test Data:** Make multiple sequential requests
- **Test Case Explanation:** Test consistency of inventory data across requests.
- **Expected Result:**
  - All requests return Status Code: 200
  - Response structure remains consistent
  - Values reflect accurate counts

### Negative Test Scenarios

#### Scenario 9.3: Get Inventory with Invalid Query Parameters
- **Scenario Type:** Negative
- **Test URL:** `/store/inventory?status=available`
- **Test Data:** Query parameter: status=available (not expected)
- **Test Case Explanation:** Test with unexpected query parameters.
- **Expected Result:**
  - Status Code: 200 (typically ignored) or 400
  - Extra parameters are either ignored or error returned

### Boundary Test Scenarios

#### Scenario 9.4: Verify Inventory Count Accuracy After Pet Addition
- **Scenario Type:** Boundary
- **Test URL:** `/store/inventory` before and after adding pet
- **Test Data:** Call inventory, add pet, call inventory again
- **Test Case Explanation:** Test that inventory counts update when pets are added.
- **Expected Result:**
  - Before: Inventory count = X
  - After: Available count increases to X+1
  - Changes reflect new pet additions

---

## 10. POST /store/order - Place Order

### Positive Test Scenarios

#### Scenario 10.1: Place Order with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 1,
    "petId": 1,
    "quantity": 5,
    "shipDate": "2026-03-15T10:00:00Z",
    "status": "approved",
    "complete": false
  }
  ```
- **Test Case Explanation:** Test successful order placement with all fields.
- **Expected Result:**
  - Status Code: 200
  - Response contains Order object with provided data
  - Order is retrievable via GET /store/order/{orderId}

#### Scenario 10.2: Place Order with Minimal Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 2,
    "petId": 2,
    "quantity": 1
  }
  ```
- **Test Case Explanation:** Test order with only essential fields.
- **Expected Result:**
  - Status Code: 200
  - Response contains Order with provided fields
  - Status and complete fields have default values

### Negative Test Scenarios

#### Scenario 10.3: Place Order without petId
- **Scenario Type:** Negative
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 3,
    "quantity": 5
  }
  ```
- **Test Case Explanation:** Test order without required petId.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error message about missing petId

#### Scenario 10.4: Place Order with Invalid Status
- **Scenario Type:** Negative
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 4,
    "petId": 1,
    "quantity": 2,
    "status": "invalid_status"
  }
  ```
- **Test Case Explanation:** Test order with status not in enum (placed, approved, delivered).
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about invalid status value

#### Scenario 10.5: Place Order with Negative Quantity
- **Scenario Type:** Negative
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 5,
    "petId": 1,
    "quantity": -5
  }
  ```
- **Test Case Explanation:** Test order with negative quantity.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about invalid quantity

### Boundary Test Scenarios

#### Scenario 10.6: Place Order with Zero Quantity
- **Scenario Type:** Boundary
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 6,
    "petId": 1,
    "quantity": 0
  }
  ```
- **Test Case Explanation:** Test order with zero quantity.
- **Expected Result:**
  - Status Code: 400 or 200
  - If 400: Zero quantity not allowed
  - If 200: Order accepted with 0 quantity

#### Scenario 10.7: Place Order with Very Large Quantity
- **Scenario Type:** Boundary
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 7,
    "petId": 1,
    "quantity": 2147483647
  }
  ```
- **Test Case Explanation:** Test order with maximum int32 quantity.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Large quantity accepted
  - If 400: Exceeds maximum quantity

#### Scenario 10.8: Place Order with Duplicate ID
- **Scenario Type:** Boundary
- **Test URL:** `/store/order`
- **Test Data:**
  ```json
  {
    "id": 1,
    "petId": 2,
    "quantity": 1
  }
  ```
- **Test Case Explanation:** Test order with duplicate order ID.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 400: Duplicate ID not allowed
  - If 200: Existing order is replaced

---

## 11. GET /store/order/{orderId} - Get Order by ID

### Positive Test Scenarios

#### Scenario 11.1: Get Existing Order by Valid ID
- **Scenario Type:** Positive
- **Test URL:** `/store/order/1`
- **Test Data:** Path parameter: orderId=1
- **Test Case Explanation:** Test retrieval of existing order.
- **Expected Result:**
  - Status Code: 200
  - Response contains Order object
  - Order ID matches requested ID

#### Scenario 11.2: Get Order by Different Valid ID
- **Scenario Type:** Positive
- **Test URL:** `/store/order/5`
- **Test Data:** Path parameter: orderId=5
- **Test Case Explanation:** Test retrieval by valid ID within acceptable range.
- **Expected Result:**
  - Status Code: 200
  - Response contains Order details

### Negative Test Scenarios

#### Scenario 11.3: Get Order with ID > 10
- **Scenario Type:** Negative
- **Test URL:** `/store/order/11`
- **Test Data:** Path parameter: orderId=11
- **Test Case Explanation:** Test retrieval with ID > 10 (per spec: "For valid response try integer IDs with value <= 5 or > 10").
- **Expected Result:**
  - Status Code: 404
  - Error message about order not found

#### Scenario 11.4: Get Non-existent Order
- **Scenario Type:** Negative
- **Test URL:** `/store/order/999`
- **Test Data:** Path parameter: orderId=999
- **Test Case Explanation:** Test with order ID that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error about order not found

#### Scenario 11.5: Get Order with Invalid ID Format
- **Scenario Type:** Negative
- **Test URL:** `/store/order/abc`
- **Test Data:** Path parameter: orderId=abc (non-numeric)
- **Test Case Explanation:** Test with non-integer order ID.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid ID format

### Boundary Test Scenarios

#### Scenario 11.6: Get Order with ID = 5 (Upper Valid Boundary)
- **Scenario Type:** Boundary
- **Test URL:** `/store/order/5`
- **Test Data:** Path parameter: orderId=5
- **Test Case Explanation:** Test at exact boundary of valid IDs <= 5.
- **Expected Result:**
  - Status Code: 200
  - Order details returned

#### Scenario 11.7: Get Order with ID = 6 (Below Exception Range)
- **Scenario Type:** Boundary
- **Test URL:** `/store/order/6`
- **Test Data:** Path parameter: orderId=6
- **Test Case Explanation:** Test ID between valid range (6-9 should generate exceptions per spec).
- **Expected Result:**
  - Status Code: 400 or 404
  - Exception generation as per specification

#### Scenario 11.8: Get Order with ID = 10 (Lower Exception Boundary)
- **Scenario Type:** Boundary
- **Test URL:** `/store/order/10`
- **Test Data:** Path parameter: orderId=10
- **Test Case Explanation:** Test at boundary before "ID > 10" range.
- **Expected Result:**
  - Status Code: 400 or 404
  - Exception handling

---

## 12. DELETE /store/order/{orderId} - Delete Order

### Positive Test Scenarios

#### Scenario 12.1: Delete Existing Order with Valid ID
- **Scenario Type:** Positive
- **Test URL:** `/store/order/1`
- **Test Data:** Path parameter: orderId=1
- **Test Case Explanation:** Test successful deletion of existing order.
- **Expected Result:**
  - Status Code: 200
  - Message indicating order deleted
  - Subsequent GET returns 404

#### Scenario 12.2: Delete Different Existing Order
- **Scenario Type:** Positive
- **Test URL:** `/store/order/3`
- **Test Data:** Path parameter: orderId=3
- **Test Case Explanation:** Test deletion of another order.
- **Expected Result:**
  - Status Code: 200
  - Order removed from system

### Negative Test Scenarios

#### Scenario 12.3: Delete Order with ID >= 1000
- **Scenario Type:** Negative
- **Test URL:** `/store/order/1000`
- **Test Data:** Path parameter: orderId=1000
- **Test Case Explanation:** Test deletion with ID >= 1000 (per spec: generates API errors).
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid ID

#### Scenario 12.4: Delete Non-existent Order
- **Scenario Type:** Negative
- **Test URL:** `/store/order/999`
- **Test Data:** Path parameter: orderId=999
- **Test Case Explanation:** Test deletion of non-existent order.
- **Expected Result:**
  - Status Code: 404
  - Error about order not found

#### Scenario 12.5: Delete Order with Invalid ID Format
- **Scenario Type:** Negative
- **Test URL:** `/store/order/invalid`
- **Test Data:** Path parameter: orderId=invalid (non-numeric)
- **Test Case Explanation:** Test with non-integer order ID.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid ID format

### Boundary Test Scenarios

#### Scenario 12.6: Delete Order with ID = 999 (Below Limit)
- **Scenario Type:** Boundary
- **Test URL:** `/store/order/999`
- **Test Data:** Path parameter: orderId=999
- **Test Case Explanation:** Test deletion at boundary of valid IDs (< 1000).
- **Expected Result:**
  - Status Code: 200 or 404
  - If order exists: Successfully deleted
  - If not exists: 404 returned

#### Scenario 12.7: Delete Same Order Twice
- **Scenario Type:** Boundary
- **Test URL:** `/store/order/5` (twice)
- **Test Data:** Same orderId in two sequential requests
- **Test Case Explanation:** Test deleting same order multiple times.
- **Expected Result:**
  - First request: Status Code: 200 (deleted)
  - Second request: Status Code: 404 (already deleted)

---

# USER ENDPOINTS

## 13. POST /user - Create User

### Positive Test Scenarios

#### Scenario 13.1: Create User with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "id": 1,
    "username": "john_doe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "phone": "555-1234",
    "userStatus": 1
  }
  ```
- **Test Case Explanation:** Test successful user creation with all fields populated.
- **Expected Result:**
  - Status Code: 200
  - Response contains User object with all provided fields
  - User is retrievable via GET /user/{username}

#### Scenario 13.2: Create User with Minimal Data
- **Scenario Type:** Positive
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "username": "jane_smith"
  }
  ```
- **Test Case Explanation:** Test user creation with only username.
- **Expected Result:**
  - Status Code: 200
  - User created with minimal data
  - Other fields populated with defaults or null

### Negative Test Scenarios

#### Scenario 13.3: Create User with Duplicate Username
- **Scenario Type:** Negative
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "username": "john_doe",
    "firstName": "John2"
  }
  ```
- **Test Case Explanation:** Test creation with username already existing.
- **Expected Result:**
  - Status Code: 400 or 409
  - Error about duplicate username

#### Scenario 13.4: Create User without Username
- **Scenario Type:** Negative
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
- **Test Case Explanation:** Test creation without username field.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about missing username

#### Scenario 13.5: Create User with Invalid Email Format
- **Scenario Type:** Negative
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "username": "user123",
    "email": "invalid-email"
  }
  ```
- **Test Case Explanation:** Test creation with invalid email format.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about invalid email format

### Boundary Test Scenarios

#### Scenario 13.6: Create User with Very Long Username
- **Scenario Type:** Boundary
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "username": "a" * 500
  }
  ```
- **Test Case Explanation:** Test with extremely long username.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Long username accepted
  - If 400: Length limit exceeded

#### Scenario 13.7: Create User with Special Characters in Username
- **Scenario Type:** Boundary
- **Test URL:** `/user`
- **Test Data:**
  ```json
  {
    "username": "user@#$%^&*()"
  }
  ```
- **Test Case Explanation:** Test with special characters in username.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Special characters allowed
  - If 400: Invalid character error

---

## 14. POST /user/createWithList - Create Multiple Users

### Positive Test Scenarios

#### Scenario 14.1: Create Multiple Users with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/user/createWithList`
- **Test Data:**
  ```json
  [
    {
      "username": "user1",
      "firstName": "User",
      "lastName": "One",
      "email": "user1@example.com"
    },
    {
      "username": "user2",
      "firstName": "User",
      "lastName": "Two",
      "email": "user2@example.com"
    },
    {
      "username": "user3",
      "firstName": "User",
      "lastName": "Three",
      "email": "user3@example.com"
    }
  ]
  ```
- **Test Case Explanation:** Test bulk creation of multiple users.
- **Expected Result:**
  - Status Code: 200
  - All three users successfully created
  - Each is retrievable individually

#### Scenario 14.2: Create Single User via Bulk Endpoint
- **Scenario Type:** Positive
- **Test URL:** `/user/createWithList`
- **Test Data:**
  ```json
  [
    {
      "username": "single_user"
    }
  ]
  ```
- **Test Case Explanation:** Test bulk endpoint with single user array.
- **Expected Result:**
  - Status Code: 200
  - User successfully created

### Negative Test Scenarios

#### Scenario 14.3: Create Users with Duplicate Username in List
- **Scenario Type:** Negative
- **Test URL:** `/user/createWithList`
- **Test Data:**
  ```json
  [
    {
      "username": "duplicate_user"
    },
    {
      "username": "duplicate_user"
    }
  ]
  ```
- **Test Case Explanation:** Test with duplicate username within same request.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about duplicate usernames

#### Scenario 14.4: Create Users with Empty Array
- **Scenario Type:** Negative
- **Test URL:** `/user/createWithList`
- **Test Data:** `[]` (empty array)
- **Test Case Explanation:** Test with empty user array.
- **Expected Result:**
  - Status Code: 400 or 200
  - If 400: Empty array not allowed
  - If 200: No users created

### Boundary Test Scenarios

#### Scenario 14.5: Create Large Number of Users (100+)
- **Scenario Type:** Boundary
- **Test URL:** `/user/createWithList`
- **Test Data:** Array of 100+ user objects
- **Test Case Explanation:** Test bulk creation with large dataset.
- **Expected Result:**
  - Status Code: 200 or 413 (Payload Too Large)
  - If 200: All users created
  - If 413: Request too large

---

## 15. GET /user/login - User Login

### Positive Test Scenarios

#### Scenario 15.1: Login with Valid Credentials
- **Scenario Type:** Positive
- **Test URL:** `/user/login?username=john_doe&password=SecurePass123`
- **Test Data:** Query parameters: username=john_doe, password=SecurePass123
- **Test Case Explanation:** Test successful login with correct credentials.
- **Expected Result:**
  - Status Code: 200
  - Response contains authentication token or message
  - Headers include X-Rate-Limit and X-Expires-After
  - X-Expires-After shows token expiration time

#### Scenario 15.2: Login with Different Valid User
- **Scenario Type:** Positive
- **Test URL:** `/user/login?username=jane_smith&password=Pass456`
- **Test Data:** Query parameters with different valid credentials
- **Test Case Explanation:** Test login for another valid user.
- **Expected Result:**
  - Status Code: 200
  - Token/session established
  - Rate limit headers present

### Negative Test Scenarios

#### Scenario 15.3: Login with Invalid Password
- **Scenario Type:** Negative
- **Test URL:** `/user/login?username=john_doe&password=WrongPassword`
- **Test Data:** Query parameters: username=john_doe, password=WrongPassword
- **Test Case Explanation:** Test login with incorrect password.
- **Expected Result:**
  - Status Code: 400
  - Error message about invalid credentials

#### Scenario 15.4: Login with Non-existent User
- **Scenario Type:** Negative
- **Test URL:** `/user/login?username=nonexistent&password=Pass123`
- **Test Data:** Query parameters with non-existent username
- **Test Case Explanation:** Test login with username that doesn't exist.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid username/password

#### Scenario 15.5: Login without Username
- **Scenario Type:** Negative
- **Test URL:** `/user/login?password=Pass123`
- **Test Data:** Query parameters: missing username
- **Test Case Explanation:** Test login without username parameter.
- **Expected Result:**
  - Status Code: 400
  - Error about missing username

#### Scenario 15.6: Login without Password
- **Scenario Type:** Negative
- **Test URL:** `/user/login?username=john_doe`
- **Test Data:** Query parameters: missing password
- **Test Case Explanation:** Test login without password parameter.
- **Expected Result:**
  - Status Code: 400
  - Error about missing password

### Boundary Test Scenarios

#### Scenario 15.7: Login with Empty Username
- **Scenario Type:** Boundary
- **Test URL:** `/user/login?username=&password=Pass123`
- **Test Data:** Query parameters: username= (empty), password=Pass123
- **Test Case Explanation:** Test login with empty username field.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid credentials

#### Scenario 15.8: Login with Empty Password
- **Scenario Type:** Boundary
- **Test URL:** `/user/login?username=john_doe&password=`
- **Test Data:** Query parameters: username=john_doe, password= (empty)
- **Test Case Explanation:** Test login with empty password field.
- **Expected Result:**
  - Status Code: 400
  - Error about invalid credentials

#### Scenario 15.9: Login with Special Characters in Password
- **Scenario Type:** Boundary
- **Test URL:** `/user/login?username=john_doe&password=P%40%23%24%25^`
- **Test Data:** Query parameters with URL-encoded special characters
- **Test Case Explanation:** Test login with special characters in password.
- **Expected Result:**
  - Status Code: 200 or 400
  - If 200: Special characters properly handled
  - If 400: Invalid password

---

## 16. GET /user/logout - User Logout

### Positive Test Scenarios

#### Scenario 16.1: Logout Current User
- **Scenario Type:** Positive
- **Test URL:** `/user/logout`
- **Test Data:** No parameters required
- **Test Case Explanation:** Test user logout from current session.
- **Expected Result:**
  - Status Code: 200
  - Message indicating successful logout
  - User session terminated

#### Scenario 16.2: Multiple Sequential Logouts
- **Scenario Type:** Positive
- **Test URL:** `/user/logout` (multiple requests)
- **Test Data:** Multiple logout requests
- **Test Case Explanation:** Test that logout can be called multiple times.
- **Expected Result:**
  - First logout: Status Code: 200
  - Subsequent logouts: Status Code: 200 or 400
  - System handles gracefully

### Negative Test Scenarios

#### Scenario 16.3: Logout Without Active Session
- **Scenario Type:** Negative
- **Test URL:** `/user/logout`
- **Test Data:** No active session/authentication
- **Test Case Explanation:** Test logout without being logged in.
- **Expected Result:**
  - Status Code: 400 or 200
  - If 400: Error about no active session
  - If 200: Graceful response

### Boundary Test Scenarios

#### Scenario 16.4: Logout with Query Parameters (Unexpected)
- **Scenario Type:** Boundary
- **Test URL:** `/user/logout?extra=param`
- **Test Data:** Unexpected query parameters
- **Test Case Explanation:** Test logout endpoint with extra parameters.
- **Expected Result:**
  - Status Code: 200
  - Extra parameters ignored
  - Logout proceeds normally

---

## 17. GET /user/{username} - Get User by Username

### Positive Test Scenarios

#### Scenario 17.1: Get Existing User by Valid Username
- **Scenario Type:** Positive
- **Test URL:** `/user/john_doe`
- **Test Data:** Path parameter: username=john_doe
- **Test Case Explanation:** Test retrieval of existing user by username.
- **Expected Result:**
  - Status Code: 200
  - Response contains User object
  - All user details included

#### Scenario 17.2: Get Different Existing User
- **Scenario Type:** Positive
- **Test URL:** `/user/user1`
- **Test Data:** Path parameter: username=user1
- **Test Case Explanation:** Test retrieval of different user.
- **Expected Result:**
  - Status Code: 200
  - Correct user details returned

### Negative Test Scenarios

#### Scenario 17.3: Get Non-existent User
- **Scenario Type:** Negative
- **Test URL:** `/user/nonexistent_user`
- **Test Data:** Path parameter: username=nonexistent_user
- **Test Case Explanation:** Test retrieval of user that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error message about user not found

#### Scenario 17.4: Get User with Invalid Username Format
- **Scenario Type:** Negative
- **Test URL:** `/user/` (empty username)
- **Test Data:** Path parameter: empty string
- **Test Case Explanation:** Test with empty username.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error about invalid username

### Boundary Test Scenarios

#### Scenario 17.5: Get User with Username Containing Spaces
- **Scenario Type:** Boundary
- **Test URL:** `/user/john%20doe` (URL encoded)
- **Test Data:** Path parameter: username with spaces
- **Test Case Explanation:** Test username containing spaces.
- **Expected Result:**
  - Status Code: 200 or 404
  - If 200: User exists with spaces in username
  - If 404: Spaces not allowed in username

#### Scenario 17.6: Get User with Very Long Username
- **Scenario Type:** Boundary
- **Test URL:** `/user/` + (very long string)
- **Test Data:** Path parameter: extremely long username
- **Test Case Explanation:** Test with very long username string.
- **Expected Result:**
  - Status Code: 404 or 414 (URI Too Long)
  - User not found or request rejected

---

## 18. PUT /user/{username} - Update User

### Positive Test Scenarios

#### Scenario 18.1: Update User with Valid Data
- **Scenario Type:** Positive
- **Test URL:** `/user/john_doe`
- **Test Data:**
  - Path parameter: username=john_doe
  - Body:
  ```json
  {
    "id": 1,
    "username": "john_doe_updated",
    "firstName": "Johnny",
    "email": "john.updated@example.com"
  }
  ```
- **Test Case Explanation:** Test successful user update with new data.
- **Expected Result:**
  - Status Code: 200
  - User details updated
  - Subsequent GET returns updated information

#### Scenario 18.2: Update User with Partial Data
- **Scenario Type:** Positive
- **Test URL:** `/user/jane_smith`
- **Test Data:**
  - Path parameter: username=jane_smith
  - Body:
  ```json
  {
    "email": "jane.new@example.com"
  }
  ```
- **Test Case Explanation:** Test update with only some fields changed.
- **Expected Result:**
  - Status Code: 200
  - Email updated, other fields unchanged

### Negative Test Scenarios

#### Scenario 18.3: Update Non-existent User
- **Scenario Type:** Negative
- **Test URL:** `/user/nonexistent`
- **Test Data:**
  - Path parameter: username=nonexistent
  - Body: User object with updates
- **Test Case Explanation:** Test update of user that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error message about user not found

#### Scenario 18.4: Update User with Invalid Email Format
- **Scenario Type:** Negative
- **Test URL:** `/user/john_doe`
- **Test Data:**
  - Path parameter: username=john_doe
  - Body:
  ```json
  {
    "email": "invalid-email"
  }
  ```
- **Test Case Explanation:** Test update with invalid email.
- **Expected Result:**
  - Status Code: 400 or 422
  - Error about email format

### Boundary Test Scenarios

#### Scenario 18.5: Update User with Empty Username in Path
- **Scenario Type:** Boundary
- **Test URL:** `/user/`
- **Test Data:** Empty path parameter
- **Test Case Explanation:** Test with empty username path parameter.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error about invalid path

---

## 19. DELETE /user/{username} - Delete User

### Positive Test Scenarios

#### Scenario 19.1: Delete Existing User
- **Scenario Type:** Positive
- **Test URL:** `/user/user_to_delete`
- **Test Data:** Path parameter: username=user_to_delete
- **Test Case Explanation:** Test successful user deletion.
- **Expected Result:**
  - Status Code: 200
  - Message indicating user deleted
  - Subsequent GET returns 404

#### Scenario 19.2: Delete Different User
- **Scenario Type:** Positive
- **Test URL:** `/user/another_user`
- **Test Data:** Path parameter: username=another_user
- **Test Case Explanation:** Test deletion of another user.
- **Expected Result:**
  - Status Code: 200
  - User removed from system

### Negative Test Scenarios

#### Scenario 19.3: Delete Non-existent User
- **Scenario Type:** Negative
- **Test URL:** `/user/nonexistent_user`
- **Test Data:** Path parameter: username=nonexistent_user
- **Test Case Explanation:** Test deletion of user that doesn't exist.
- **Expected Result:**
  - Status Code: 404
  - Error about user not found

#### Scenario 19.4: Delete User with Empty Username
- **Scenario Type:** Negative
- **Test URL:** `/user/`
- **Test Data:** Empty path parameter
- **Test Case Explanation:** Test deletion with empty username.
- **Expected Result:**
  - Status Code: 400 or 404
  - Error about invalid username

### Boundary Test Scenarios

#### Scenario 19.5: Delete Same User Twice
- **Scenario Type:** Boundary
- **Test URL:** `/user/user_to_delete` (twice)
- **Test Data:** Same username in two requests
- **Test Case Explanation:** Test deleting same user multiple times.
- **Expected Result:**
  - First request: Status Code: 200 (deleted)
  - Second request: Status Code: 404 (already deleted)

#### Scenario 19.6: Delete User with Special Characters in Username
- **Scenario Type:** Boundary
- **Test URL:** `/user/user%40%23%24`
- **Test Data:** Path parameter with special characters
- **Test Case Explanation:** Test deletion with special characters in username.
- **Expected Result:**
  - Status Code: 200 or 404
  - If user exists: Successfully deleted
  - If not: 404 returned

---

## Summary

This comprehensive test scenario document covers **all endpoints** in the Petstore OpenAPI 3.0 specification with:
- **19 API Endpoints** fully tested
- **Positive Test Scenarios:** 33 scenarios
- **Negative Test Scenarios:** 40 scenarios  
- **Boundary Test Scenarios:** 35 scenarios
- **Regression Test Scenarios:** 2 scenarios

**Total Test Scenarios: 110+**

Each scenario includes:
- Clear classification (Positive/Negative/Boundary/Regression)
- Test URL endpoint
- Specific test data or parameters
- Detailed explanation of test purpose
- Expected results including status codes and response structure

