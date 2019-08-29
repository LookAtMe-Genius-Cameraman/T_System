# Creating new Position

This process creates a new position for T_System's arm.
Returns an error if the DB is empty.

## Request
```http
POST /api/position?db=<DB>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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
- Returns an error if the DB is empty.

## Request
```http
GET /api/position?db=<DB>&id=<ID>&admin_id=<ADMIN_ID>
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
Returns an error if the ID or DB is empty.

## Request
```http
PUT /api/position?db=<DB>&id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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
Returns an error if the DB is empty.


## Request
```http
DEL /api/position?db=<DB>&id=<ID>&admin_id=<ADMIN_ID>
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
