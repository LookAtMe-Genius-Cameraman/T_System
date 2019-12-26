# Creating New Accounts to Remote Storage Services

This process creates a new accounts for synchronization ability with cloud based remote storage services of T_System.
For creating accounts NAME parameter requires. It is service name.

## Request
```http
POST /api/r_sync?name=<NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
Content-Type: application/json; charset=UTF-8

{
    "name": "ACCOUNT_NAME_OF_USER",
    "key": "STREAM_KEY"
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

# Getting Services
- If a specific parameter NAME is given, its service are listed.

## Request
```http
GET /api/r_sync?name=<NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
```

## Response
### On Success
- If NAME is given as `Dropbox` so if service is `Dropbox`
```json
{
    "status": "OK",
    "data":[{
        "name": "Dropbox",
        "to_be_used": true,
        "accounts": {
                  "name": "USER", 
                  "key": "STREAM_KEY", 
                  "is_active": false
                  }
    }]
}
```
### On Failure
```json
{
    "status": "ERROR"
}
```

# Updating Accounts
Returns an error if the NAME parameter is empty.

## Request
```http
PUT /api/r_sync?name=<NAME>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
Content-Type: application/json; charset=UTF-8

{
    "name": "ACCOUNT_NAME_OF_USER",
    "key": "STREAM_KEY"
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
    "message": "NAME parameter is missing."
}
```

# Setting the Usage Status of Remote Storage Services and Accounts of These Services.
Returns an error if the CAUSE or IN_USE is empty.
CAUSE parameter can be either `service`, `account` or `sync`. If `sync` is given, folder synchronization process will be started or stopped by IN_USE. Otherwise, parameters will be set.

## Request
```http
PATCH /api/r_sync?cause=<CAUSE>&in_use=<IN_USE>&name=<NAME>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
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

# Deleting Accounts
This process removes the accounts that records on remote storage services about cloud based folder synchronization ability of T_System.
Returns an error if the NAME or ACCOUNT_NAME parameter is empty.


## Request
```http
DEL /api/live_stream?name=<NAME>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
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
    "message": "NAME parameter is missing."
}
```
