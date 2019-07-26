# Getting System Information.
Returns T_System based OS information

## Request
```http
GET /api/system_info
Host: domain
```

## Response
### On Success
```json
{
    "status": "OK",
    "data":{
    "disk_usage_percent": "usage_percent", 
    "free_disk_space": "free_usage",
    "cpu_usage_percent": "cpu_percent",
    "ram_usage_percent": "ram_usage",
    "cpu_temperature": "cpu_temperature"
    }
}
```
### On Failure
```json
{
    "status": "ERROR"
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

## DELETE Request

## Response

```json
{
    "status": "ERROR",
    "message": "NOT VALID"
}
```
