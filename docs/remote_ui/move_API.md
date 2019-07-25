# Moving the Arm.
Returns an error if the ID is empty.

## Request
```http
PUT /api/scenario?id=<ID>&is_root=<IS_ROOT>
Host: domain
Content-Type: application/json

{
    "type": "Joint" / "axis",
    "id": "1" / "y",
    "quantity": "10"
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
