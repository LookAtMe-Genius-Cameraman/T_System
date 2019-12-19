# Creating new Website and Stream Identity

This process creates a new Website or Stream Identity for Online Stream ability of T_System Vision.
For creating websites, Root authentication requires.
For creating stream Identities ID parameter requires.

## Request
```http
POST /api/live_stream?id=<ID>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
Content-Type: application/json; charset=UTF-8

# For website creation:
{
    "name": "youtube",
    "url": "www.youtube.com",
    "server": "rtmp://a.rtmp.youtube.com/live2/"
}

# For Stream Identity creation:
{
    "account_name": "youtuber_1",
    "key": "STREAM_KEY"
}
```
## Response

### On Success
```json
{
  "status": "OK",
}
```

### On failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

# Getting Websites
- If a specific parameter ID is given, its website are listed.

## Request
```http
GET /api/live_stream?id=<ID>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":[{
        "id": "b970138a-aecb-11e9-b130-cc2f714671ed",
        "name": "youtube",
        "url": "www.youtube.com",
        "server": "rtmp://a.rtmp.youtube.com/live2/",
        "to_be_used": true,
        "stream_ids": {
                  "account_name": "youtuber_1", 
                  "key": "STREAM_KEY", 
                  "key_file": "PATH_Of_FILE/youtuber_1.key", 
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

# Updating Websites and Stream IDs
Returns an error if the ID parameter is empty.

## Request
```http
PUT /api/live_stream?id=<ID>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
Host: domain
Content-Type: application/json; charset=UTF-8

# For website updating:
{
    "name": "youtube",
    "url": "www.youtube.com",
    "server": "rtmp://a.rtmp.youtube.com/live2/"
}

# For Stream Identity updating:
{
    "account_name": "youtuber_1",
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
    "message": "ID parameter is missing."
}
```

# Setting the Usage Status of WebSites and WebSite's Stream IDs
Returns an error if the CAUSE or IN_USE is empty.
CAUSE parameter can be either `website`, `stream_id` or `live`. If `live` is given, online stream will be started or stopped by IN_USE. Otherwise, parameters will be set.

## Request
```http
PATCH /api/live_stream?cause=<CAUSE>&in_use=<IN_USE>&id=<ID>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>
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

# Deleting Websites and Stream Ids
This process removes the websites or Stream IDs of Online Stream ability of T_System Vision.
Returns an error if the ID parameter is empty.


## Request
```http
DEL /api/live_stream?id=<ID>&account_name=<ACCOUNT_NAME>&admin_id=<ADMIN_ID>&root=<ROOT>
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
    "message": "ID parameter is missing."
}
```
