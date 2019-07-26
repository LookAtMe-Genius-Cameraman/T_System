# Creating new Login

This process creates a login point to a new network.

## Request
```http
POST /api/network?is_root=<IS_ROOT>
Host: domain
Content-Type: application/json

{
    "ssid": "ssid",
    "password": "password"
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

# Getting Positions
- If a specific parameter SSID is given, its network are listed.

## Request
```http
GET /api/network?ssid=<SSID>&is_root=<IS_ROOT>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[{
        "ssid": "ssid",
        "password": "password"
    }]
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```

# Updating Position
Returns an error if the ID is empty.

## Request
```http
PUT /api/network?ssid=<SSID>&is_root=<IS_ROOT>
Host: domain
Content-Type: application/json

{
    "ssid": "ssid",
    "password": "password"
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

# Deleting Position
Removes the Network.

## Request
```http
DEL /api/network?ssid=<SSID>&is_root=<IS_ROOT>
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
    "message": "SSID parameter is missing."
}
```
