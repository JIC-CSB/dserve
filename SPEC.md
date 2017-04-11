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
  }
  "uuid": "C4F5E4AB-A4CE-4DD7-91A3-0F4D7C646FE5",
  "dtool_version": 0.13.0,
  "name": "cotyledon_images",
  "creator_username": "olssont",
}
```

Request:

```
GET / HTTP/1.1
Host: localhost:5000
Accept: html

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
        "mimetype": "image/png",
        "size": 56
      },
      {
        "_links": { "self": { "href": "/items/md5different"  } }, 
        "identifier": "md5different",
        "mimetype": "image/png",
        "size": 102
      }
    ]
    number_of_items: 2,
    total_size: 158
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
     "mimetype": { "href": "/overlays/mimetype" }, 
     "coordinates": { "href": "/overlays/coordinates" } }, 
  } 
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
     "content": { "href": "/items/md5sljdflajsdf/raw" }
  }
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


### Creating a new / replacing an overlay

*Q: Should it be possible to update the overlay value from an individual item?*
*Q: How can one access an empty overlay?*

Request:

```
PUT /overlays/coordinates HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "md5sljdflajsdf": { "x": 800.0, "y": 0.56 },
  "md5different": { "x": 80.8, "y": 3.3 }
} 
```

Response:

```
HTTP/1.1 200 OK
```
