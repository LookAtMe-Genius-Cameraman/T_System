# Creating new Position

This process creates a new position for T_System's arm.

## Request
```http
POST /api/position?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json

{
    "name": "position_name",
    "cartesian_coords": [30, 25, 42],
    "polar_coords": [1.5, 1.02, 0.5],
}
```
## Response

### On Success
```json
{
  "status": "OK",
  "id": "b970138a-aecb-11e9-b130-cc2f714671ed"
}
```

### On failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

# Getting Positions
- If a specific parameter ID is given, its position are listed.

## Request
```http
GET /api/position?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[{
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "position_name",
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    }]
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```

# Updating Position
Returns an error if the ID is empty.

## Request
```http
PUT /api/position?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json

{
    "name": "position_name",
    "cartesian_coords": [18, 27, 48],
    "polar_coords": [1.2, 1.85, 0.65],
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

# Deleting Position
Removes the Position.

## Request
```http
DEL /api/position?id=<ID>&admin_id=<ADMIN_ID>
Content-Type: application/json
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
