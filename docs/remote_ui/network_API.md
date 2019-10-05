# Creating new Login

If ACTIVITY None, this process creates a login point to a new network with incoming data.
If ACTIVITY is not None (True/False), it changes network connector's activity status of stand_ui.

## Request
```http
POST /api/network?activity=<ACTIVITY>&admin_id=<ADMIN_ID>
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
- If ACTIVITY None, and specific parameter SSID is given, its network are listed.
- If ACTIVITY is not None, network connector's activity status of stand_ui returns.

## Request
```http
GET /api/network?activity=<ACTIVITY>&ssid=<SSID>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
- If ACTIVITY is None
```json
{
    "status": "OK",
    "data":[{
        "ssid": "ssid",
        "password": "password"
    }]
}
```
- If ACTIVITY is not None (True/False)
```json
{
    "status": "OK",
    "data": true
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
