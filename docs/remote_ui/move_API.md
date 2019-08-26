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
    "status": "ERROR"
}
```

## POST Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```

# Getting Current Position
- Returns T_System's arm current position info as cartesian and polar coordinates.

## Request
```http
GET /api/move?admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
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
