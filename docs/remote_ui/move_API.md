# Moving the arm by action 
Returns an error if the DB_NAME, ACTION or A_TYPE are empty.

## Request
```http
POST /api/move?db_name=<DB_NAME>&actıon=<ACTION>&a_type=<A_TYPE>&root=<ROOT>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
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

# Moving the Arm.
Returns an error if the ID is empty.

## Request
```http
PUT /api/move?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{
    "type": "Joint" / "axis",
    "id": "1" / "y",
    "quantity": 10
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
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

# Setting the Arm 
Returns an error if the EXPAND is empty.

## Request
```http
PATCH /api/move?expand=<EXPAND>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
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

# Getting Current Position
- If a specific parameter CAUSE is given as 'joint_count', Robotic Arm's joint count returns.
- Returns T_System's arm current position info as cartesian and polar coordinates.

## Request
```http
GET /api/move?cause=<CAUSE>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
- If CAUSE is 'joint_count'
```json
{
    "status": "OK",
    "data": 5
}
```
- If CAUSE is empty

```json
{
    "status": "OK",
    "data": {
        "cartesian_coords": [30, 25, 42],
        "polar_coords": [1.5, 1.02, 0.5]
    }
}
```

## DELETE Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```
