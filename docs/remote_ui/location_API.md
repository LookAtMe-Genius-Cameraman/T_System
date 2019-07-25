# Creating new Location

This process creates a new location.

## Request
```http
POST /api/location
Host: domain
Content-Type: application/json

{
    "name": "Istanbul",
    "ip": "172.22.9.27",
}
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

# Getting Locations
- If a specific parameter ID is given, its records are listed.

## Request
```http
GET /api/location?id=<ID>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[{
        "id": 1,
        "name": "ANKARA",
        "ip": "192.168.2.10",
    }]
```
### On Failure
```json
{
    "status": "ERROR"
}
```


# Changing Location
Returns an error if the ID is empty.

## Request
```http
PUT /api/location?id=<ID>
Host: domain
Content-Type: application/json

{
    "name": "Istanbul",
    "ip": "172.22.9.27",
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

# Deleting location
This process removed the location.

## Request
```http
DEL /api/location?id=<ID>
Content-Type: application/json
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
    "message": "ID parameter is missing."
}
```
