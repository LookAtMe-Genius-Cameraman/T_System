# Updating the auto-update status

## Request
```http
PUT /api/update?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json

{
    "auto_update": False,
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

# Getting Positions
- Returns an error if the ID is empty.

## Request
```http
GET /api/update?key=<KEY>&admin_id=<ADMIN_ID>
Host: domain
```
## Response

### On Success
```json
{
  "status": "OK",
  "data": "False"
}
```

### On failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
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
