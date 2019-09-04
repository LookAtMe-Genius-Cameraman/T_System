# Creating new Login

This process creates a login point to a new network.

## Request
```http
POST /api/network?admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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

# Getting Networks
- If a specific parameter SSID is given, its network are listed.

## Request
```http
GET /api/network?ssid=<SSID>&admin_id=<ADMIN_ID>
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

# Updating Network
Returns an error if the ID is empty.

## Request
```http
PUT /api/network?ssid=<SSID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

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
    "status": "ERROR",
    "message": "Missing or incorrect parameters"    
}
```

# Deleting Position
Removes the Network.

## Request
```http
DEL /api/network?ssid=<SSID>&admin_id=<ADMIN_ID>
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
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
