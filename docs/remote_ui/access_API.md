# Controlling the T_System Identity
Returns the response it holds private id of T_System.

## Request
```http
POST /api/access
Host: domain
Content-Type: application/json; charset=UTF-8

{
    "id": "MY3T55"
}
```

## Response
### On Success
```json
{
    "status": "OK",
    "data": "PR47V1"
}
```

### On Failure
```json
{
    "status": "ERROR",
    "message": "missing or incorrect parameters"
}
```

# Getting Home page of Remote UI
- Returns an error if ID is empty.
- If ID correct returns redirection to "/" url.

## Request
```http
GET /api/access?id=<ID>
Host: domain
```

## Response
### On Success
```
redirect('/')
```

### On Failure
```json
{
    "status": "ERROR",
    "message": "missing or incorrect parameters"
}
```

## PUT Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```

# Terminating Sessions of T_System
- If CAUSE parameter is "shutdown", shutdown system.
- If CAUSE parameter is "restart", restart system.
- If CAUSE parameter is empty, connection with the device and Remote UI will corrupted.

## Request
```http
DELETE /api/access?cause=<CAUSE>
Host: domain
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
}
```
