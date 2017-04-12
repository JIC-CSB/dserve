# Spec

## Root

Request:

```
GET / HTTP/1.1
Host: localhost:5000
Accept: application/hal-json

```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/hal+json

{
  "_links": {
     "self": { "href": "/"},
     "items": { "href": "/items" },
     "overlays": { "href": "/overlays" }
  },
  "uuid": "C4F5E4AB-A4CE-4DD7-91A3-0F4D7C646FE5",
  "dtool_version": "0.13.0",
  "name": "cotyledon_images",
  "creator_username": "olssont",
}
```

Request:

```
GET / HTTP/1.1
Host: localhost:5000
Accept: text/html

```

Response:

```
<html>
<!-- stuff with hyperlinks that can be clicked -->
</html>
```


## Items

Request:

```
GET /items HTTP/1.1
Host: localhost:5000
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/hal+json

{
  "_links": {
     "self": { "href": "/items"},
  }
  "_embedded": {
    "items": [
      {
        "_links": { "self": { "href": "/items/md5sljdflajsdf" } }, 
        "identifier": "md5sljdflajsdf",
        "coordinates": { "x": 4.0, "y": 5.6 },
        "mimetype": "image/png",
        "size": 56
      },
      {
        "_links": { "self": { "href": "/items/md5different"  } }, 
        "identifier": "md5different",
        "coordinates": { "x": 80.8, "y": 3.3 },
        "mimetype": "image/png",
        "size": 102
      }
    ],
    "number_of_items": 2,
    "total_size": 158
  } 
}
```

## Overlays

Request:

```
GET /overlays HTTP/1.1
Host: localhost:5000
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/hal+json

{
  "_links": {
     "self": { "href": "/overlays"},
     "coordinates": { "href": "/overlays/coordinates" } }, 
} 
```

## Specific item

Request:

```
GET /items/md5sljdflajsdf HTTP/1.1
Host: localhost:5000
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/hal+json

{
  "_links": {
     "self": { "href": "/items/md5sljdflajsdf"},
     "content": { "href": "/items/md5sljdflajsdf/raw" },
     "coordinates": { "href": "/items/md5sljdflajsdf/coordinates" }
  }
  "coordinates": { "x": 4.0, "y": 5.6 },
  "mimetype": "image/png",
  "size": 56
}
```

## Specific overlay

Request:

```
GET /overlays/coordinates HTTP/1.1
Host: localhost:5000
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "md5sljdflajsdf": { "x": 4.0, "y": 5.6 },
  "md5different": { "x": 80.8, "y": 3.3 }
} 
```


### Creating a new overlay

Request:

```
POST /overlays/score HTTP/1.1
Host: localhost:5000

```

Response:

```
HTTP/1.1 201 CREATED
```

If it exists:

```
HTTP/1.1 409 CONFLICT
```


## Value of overlay for a specific item

Request:

```
GET /items/md5sljdflajsdf/coordinates HTTP/1.1
Host: localhost:5000
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{ "x": 4.0, "y": 5.6 }
```

### Update the value of an overlay for a specific item

Request:

```
PUT /items/md5sljdflajsdf/coordinates HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{ "x": 800.0, "y": -90.5 }
```

Response:

```
HTTP/1.1 200 OK
```
