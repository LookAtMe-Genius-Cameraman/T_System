# Getting Logs.
Returns logfile.log of T_System.

## Request
```http
GET /api/logging?admin_id=<ADMIN_ID>
Host: domain
```

## Response
### On Success
```
flask.send_file("record.merged_file")

```
### On Failure
```json
{
    "status": "ERROR",
    "message": "FAILED"
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

## PUT Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```

## Clearing Logs
Clears logs vida deleting `logfile.log` file

## Request
```http
DEL /api/logging?admin_id=<ADMIN_ID>
Host: domain
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

