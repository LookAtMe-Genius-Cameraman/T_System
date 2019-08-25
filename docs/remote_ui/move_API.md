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

## GET Request

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
