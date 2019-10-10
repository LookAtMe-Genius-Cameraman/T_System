# Controlling the T_System Identity
Returns the response it holds private id of T_System.

## Request
```http
POST /api/access
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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

# Getting Home page pf Remote UI
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

## PUT Request

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
