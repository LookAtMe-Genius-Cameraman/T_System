## POST Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```

# Getting Records
- If a specific parameter DATE is given, its records info returns.
- If a specific parameter ID is given, its video record returns.
- Returns an error if the ID and DATE both full.

## Request
```http
GET /api/record?date=<DATE>&id=<ID>&admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
- İf both ID and DATE parameters empty
```json
{
    "status": "OK",
    "data":["22_05_2019", "23_05_2019","27_05-2019"]
}
```
- İf DATE parameter full
```json
{
    "status": "OK",
    "data":[
    {
        "id": "b970138a-argb-11e9-b145-cc2f844671ed", 
        "name": "record_name", 
        "time": "12_27_54", 
        "length": 180
    }]
}
```
- İf ID parameter full
```json
{
    "status": "OK",
    "data": "PATH_OF_VIDEO_FILE"
}
```
### On Failure
```json
{
    "status": "ERROR",
    "message": "DATE and ID parameters giving together"

}
```

# Updating Record
Returns an error if the ID is empty.

## Request
```http
PUT /api/record?id=<ID>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8

{
    "name": "record_name"
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

# Deleting Record
Removes the Record.

## Request
```http
DEL /api/record?id=<ID>&admin_id=<ADMIN_ID>
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
