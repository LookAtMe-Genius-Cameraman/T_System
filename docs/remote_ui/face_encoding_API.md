# Adding new Face Encoding

This process generates a new face encoding for T_System's human face recognition ability.

## Request
```http
POST /api/face_encoding?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{   
    "face_name": "face_name",
    "photos": [{"name": "photo_name", "base_sf": "..."}, {"name": "photo_name", "base_sf": "..."}],
}
```
## Response

### On Success
```json
{
  "status": "OK"
}
```

### On failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

# Getting Faces
- If a specific parameter ID is given, its face are listed.

## Request
```http
GET /api/face_encoding?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[{
        "id": "z970136a-aegb-15e9-b130-cy2f756671ed",
        "name": "face_name",
        "image_names": ["image_name"]
    }]
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```

# Updating Face
Returns an error if the ID is empty.

## Request
```http
PUT /api/face_encoding?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{
    "face_name": "face_name",
    "photos": [{"name": "photo_name", "base_sf": "..."}, {"name": "photo_name", "base_sf": "..."}],
}
```

## Response
### On Success
```json
{
    "status": "OK"
}
```

### On Failure
```json
{
    "status": "ERROR"
}
```

# Deleting Face
Removes the Face.

## Request
```http
DEL /api/face_encoding?id=<ID>&admin_id=<ADMIN_ID>
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```

## Response
### On Success
```json
{
    "status": "OK"
}
```
### On Failure
```json
{
    "status": "ERROR",
    "message": "ID parameter is missing."
}
```
