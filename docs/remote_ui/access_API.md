# Controlling the T_System Identity
Returns the response it holds name of T_System.

## Request
```http
POST /api/access
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{}
```

## Response
### On Success
```json
{
    "status": "OK",
    "data": "T_System"
}
```

# Getting Home page pf Remote UI
- Returns redirection to "/" url.

## Request
```http
GET /api/access
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
