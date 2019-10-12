# Updating T_System Identity
If CAUSE parameter is full, its key will be updated.

## Request
```http
PUT /api/identity?cause=<CAUSE>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/json; charset=UTF-8

{
    "public_id": "MY3T55"
    "private_id": "PR47V1"
    "name": "T_System-MY3T55"
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
    "message": "missing or incorrect parameters"
}
```

# Getting Identity information of T_System

## Request
```http
GET /api/identity?admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
- If ADMIN_ID is full
```json
{
    "status": "OK",
    "data": {
        "public_id": "MY3T55",
        "private_id": "PR47V1",
        "name": "T_System-MY3T55"
      }
}
```
- If ADMIN_ID is empty
```json
{
    "status": "OK",
    "data": {
        "public_id": "MY3T55",
        "private_id": null,
        "name": "T_System-MY3T55"
    }
}
```

### On Failure
```json
{
    "status": "ERROR",
    "message": "missing or incorrect parameters"
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

## DELETE Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```
