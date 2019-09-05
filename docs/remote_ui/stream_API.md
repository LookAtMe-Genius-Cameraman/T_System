# Showing the Stream.
Returns an error if the TYPE is empty.

## Request
```http
GET /api/scenario?type=<TYPE>&admin_id=<ADMIN_ID>
Host: domain
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
```

## Response
### On Success
```
flask.Response(stream, mimetype=mimetype)
```

### On Failure
```json
{
    "status": "ERROR",
    "message": "Missing or incorrect parameters"
}
```

## Stop the Stream Showing
Returns an error if the TYPE is empty.

## Request
```http
DEL /api/network?type=<TYPE>&admin_id=<ADMIN_ID>
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
    "message": "TYPE parameter is missing."
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
