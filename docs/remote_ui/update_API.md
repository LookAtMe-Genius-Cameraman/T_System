# Updating the auto-update status

## Request
```http
PUT /api/update?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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

## Up-To-Date T_System
```http
POST /api/update?admin_id=<ADMIN_ID>
Host: domain
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

# Getting Update Status
- Returns an error if the KEY is empty.
- Valid key is "auto_update".

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
