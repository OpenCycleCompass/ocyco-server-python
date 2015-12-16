# API

## Tracks

### Track list

Retrieve track list

    GET /track/list


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| start | integer | Track to start with (default 0) |
| num   | integer | number of tracks (default 25, only for administrative users) |
| raw   | boolean | Return all tracks solely with *track_id* (only authorized users) |
| tracks | array of integers | Array of user tracks. The specified private tracks are included. (optional) |


#### Example

```
{
 "num": 24,
 "tokens": [
   "ibis_5565ad4e1b81c9.65580696",
 ]
}
```


#### Response

Status `200 OK`

```
[
 {
  "name": "Insert-Name-Here/Ratingen (11.04. ~18h; 64 Punkte)",
  "track_id": "tra_552950889bdd50.29229851"
 },
 {
  "name": "Insert-Name-Here/Aachen-Mitte (11.04. ~10h; 104 Punkte)",
  "track_id": "tra_5528dc4452c511.68030048"
 },
 {<...>}
]
```
25 tracks starting at *num* are returned if *raw* is not set.
If *raw* is set, *num* is ignored.


### Track number

Get number of tracks

    GET /track/num


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| tokens | array of string | Array of user tokens. Private tracks with specified tokens are included. (optional) |


#### Example

```
{
 "tokens": [
   "ibis_5565ad4e1b81c9.65580696",
 ]
}
```


#### Response

Status `200 OK`

```
{
 "num": 42
}
```

Number of public tracks.
If *tokens* is specified tracks uploaded using this tokens are likewise counted.


### Get track

Get track including geometry.

    GET /track/<track_id:string>


#### Parameters

*none*


#### Response

Status `200 OK`

```
{
 "track_id": <track_id:string>,
 "name": <name:string>,
 "comment": <comment:string>,
 "created": <inaccurate_date:string>,
 "length": <length_meter:integer>,
 "duration": <duration_seconds:integer>,
 "nodes": <number_of_geo_pts:integer>,
 "geometry": [
  {
   "id": 1,
   "lat": "51.30542810",
   "lon": "6.74659610",
   "alt": "0.00000000",
   "timestamp": "1423070769.000"
  },
  {<...>}
 ]
}
```


### Add track

Add a new track.

    PUSH /track/add


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| data  | JSON array of JSON objects * | Track data |
| public | boolean | Public visibility |
| token | string | User token retrieved from `GET /token/new` |
| name | string | Name for the track (optional) |
| comment | string | Additional comment (optional) |
| length | float | length in meter |
| duration | integer | duration in seconds |

\* JSON objects containing *lat* (float), *lon* (float), *time* (timestamp/integer) and optional *alt* (float)


#### Response

Status `200 OK`

```
{
 "success": true,
 "track_id": <track_id:string>,
 "nodes": <number_of_geo_pts:integer>,
 "created": <inaccurate_date:string>
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "track must contain at least 10 gps points"
}
```


### Delete track

Delete track.

    DELETE /track/<track_id:string>


#### Parameters

*none*


#### Response

Status `200 OK`

```
{
 "success": true,
 "nodes": 42
}
```

or in case of failure

Status `410 Gone`

```
{
 "success": false,
 "error": "track does not exist"
}
```

or if not authorized

Status `401 Unauthorized`

```
{
 "success": false,
 "error": "log in first"
}
```


## Token

### Create token

Get a new token.

    GET /token/new


#### Parameters

*none*


#### Response

Status `200 OK`

```
{
 "token": "ibis_559ad6e4475bd2.01987505",
 "created": 1436210916,
 "expiry": 1751570916
}
```
Returns a new created token including *created* and *expiry* timestamp.


### Verify token

Verify a token.

    GET /token/verify/<token:string>


#### Parameters

*none*


#### Response

Status `200 OK`

```
{
 "valid": true,
 "expiry": <date:string>
}
```
Returns true if token is valid.


## Routing Profiles

### List of routing profiles

Retrieve list of available routing profiles with description. 

    GET /profiles


Language of the description is determined by the *Accept-Language* header.


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| lang  | string  | *IETF language tag* of favored language, overrides *Accept-Language* header (optional) |

Default language is *en-US*.
Currently only *de-DE* and *en-US* languages are supported.


#### Example

    GET /profiles

```
{
 "lang": "de-DE"
}
```


#### Response

Status `200 OK`

```
{
 "default": "Standard",
 "fastest": "Schnellste Route",
 "scenery": "Schönste Route",
 "shortest": "Kürzeste Route"
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "error": "language is unknown"
}
```


### Get costs

Retrieve routing costs for specified routing profile.

    GET /profiles/<profile_name:string>


Language of the description is determined by the *Accept-Language* header.


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| lang  | string  | *IETF language tag* of favored language, overrides *Accept-Language* header (optional) |

Default language is *en-US*.
Currently only *de-DE* and *en-US* languages are supported.


#### Example

    GET /profiles/default

```
{
 "lang": "de-DE"
}
```

#### Response
Status `200 OK`

```
{
 "name": "default",
 "costs": [
  {
   "name": "bridleway",
   "cost": 100000,
   "id": 120
  },
  {
  "name": "unclassified",
  "cost": 1,
  "id": 123
  },
  {<...>}
 ],
 "amount_dyncost": "0.5"
}
```

### Modify profile

Modify costs and amount of dyncost for a routing profile.

    POST /profiles/<profile_name:string>

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| amount_dyncost | float (between 0 and 1) | Influence of dyncost for route calculation (0%...100%) |
| \<cost_name:string\> | float | cost for way type <cost_name>; default 1, lower means prefer, higher means avoid |


#### Example

    POST /profiles/default

```
{
 "amount_dyncost": 0.75,
 "primary": 2.5,
 "secondary": 1.5,
 "grade1": 0.9,
 "grade2": 1.05,
 <...>
}
```

#### Response

Status `204 No Content`

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "cost <cost_name> does not exist"
}
```


### Add profile

Modify costs and amount of dyncost for a routing profile.

    PUT /profiles/<profile_name:string>

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| amount_dyncost | float (between 0 and 1) | Influence of dyncost for route calculation (0%...100%) |
| \<cost_name:string\> | float | cost for way type <cost_name>; default 1, lower means prefer, higher means avoid |


#### Example

    POST /profiles/default

```
{
 "amount_dyncost": 0.75,
 "primary": 2.5,
 "secondary": 1.5,
 "grade1": 0.9,
 "grade2": 1.05,
 <...>
}
```

#### Response

Status `201 Created`
```
{
 "success": true
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "all costs must be supplied"
}
```


### Get Geo Data

Get segments contained in database.

    GET /geo

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| start_lat | float | Start latitude of bounding box |
| start_lon | float | Start longitude of bounding box |
| end_lat | float | End latitude of bounding box |
| end_lon | float | End longitude of bounding box |


#### Example

    GET /geo

```
{
 "start_lat": 50.051650,
 "start_lon": 6.514608685,
 "end_lat": 50.9048,
 "end_lon": 7.980940
}
```

#### Response

Status `200 OK`

```
{
 "segment_count": 42,
 "segments": [
  {
   "gid": 214273,
   "osm_id": 7342142,
   "coords": [
    {
     "lat": 50.42421221327,
     "lon": 7.3021042
    },
    <more coordinates (at least 1)>
   ]
  },
  <more segments>
 ]
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "bounding box must be supplied"
}
```


### Get Profile Geo Data

Get profiles specific cost (geo information).

    GET /geo/profiles/<profile_name:string>

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| start_lat | float | Start latitude of bounding box |
| start_lon | float | Start longitude of bounding box |
| end_lat | float | End latitude of bounding box |
| end_lon | float | End longitude of bounding box |


#### Example

    GET /geo/profiles/fastest

```
{
 "start_lat": 50.051650,
 "start_lon": 6.514608685,
 "end_lat": 50.9048,
 "end_lon": 7.980940
}
```

#### Response

Status `200 OK`

```
{
 "segment_count": 42,
 "segments": [
  {
   "gid": 214273,
   "osm_id": 7342142,
   "cost": 1.121212021,
   "coords": [
    {
     "lat": 50.42421221327,
     "lon": 7.3021042
    },
    <more coordinates (at least 1)>
   ]
  },
  <more segments>
 ]
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "bounding box must be supplied"
}
```


### Get *Dyncost* Geo Data

Get dynamic cost (geo information).

    GET /geo/dyncost

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| start_lat | float | Start latitude of bounding box |
| start_lon | float | Start longitude of bounding box |
| end_lat | float | End latitude of bounding box |
| end_lon | float | End longitude of bounding box |


#### Example

    GET /geo/dyncost

```
{
 "start_lat": 50.051650,
 "start_lon": 6.514608685,
 "end_lat": 50.9048,
 "end_lon": 7.980940
}
```

#### Response

Status `200 OK`

```
{
 "segment_count": 42,
 "segments": [
  {
   "gid": 214273,
   "osm_id": 7342142,
   "cost": 1.121212021,
   "coords": [
    {
     "lat": 50.42421221327,
     "lon": 7.3021042
    },
    <more coordinates (at least 1)>
   ]
  },
  <more segments>
 ]
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "bounding box must be supplied"
}
```

## Routing

### Calculate Route

Calculate a route between two specified points using a routing profile

    POST /routing/route


#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| profile | string | Routing profile to use for route calculation |


##### Start Point

In JSON object *start*:

| Name  | Type    | Description |
|-------|---------|-------------|
| lat | float | Start point latitude |
| lon | float | Start point longitude |

**or**

| Name  | Type    | Description |
|-------|---------|-------------|
| search | float | Search start point in Nominatim/Photon geocoding database |

**or**

| Name  | Type    | Description |
|-------|---------|-------------|
| osm_id | integer | Start point OSM ID |


##### End Point

In JSON object *end*:

| Name  | Type    | Description |
|-------|---------|-------------|
| lat | float | End point latitude |
| lon | float | End point longitude |

**or**

| Name  | Type    | Description |
|-------|---------|-------------|
| search | float | Search end point in Nominatim/Photon geocoding database |

**or**

| Name  | Type    | Description |
|-------|---------|-------------|
| osm_id | integer | End point OSM ID |


#### Example

    POST /routing/route

```
{
 "profile": "shortest",
 "start": {
  "lat": 50.425651,
  "lon": 7.073021
 },
 "end": {
  "search": "Hauptbahnhof Düsseldorf"
 }
}
```

**or**

    POST /routing/route

```
{
 "profile": "fastest",
 "start": {
  "osm_id": 21951651
 },
 "end": {
  "lat": 50.425651,
  "lon": 7.073021
 }
}
```

#### Response

Status `200 OK`

```
{
 "distance": 9834.18006502,
 "coords_count": 42,
 "coords": [
  {
   "lat": 50.42421221327,
   "lon": 7.3021042
  },
  <more coordinates (at least 1)>
 ],
 "start": {
  "lat": 50.425670,
  "lon": 7.0731012
  "osm_id": 1465168
 },
 "end": {
  "lat": 51.5161651,
  "lon": 7.51265022,
  "osm_id": 2451651
 }
}
```

or in case of failure

Status `401 Bad Request`

```
{
 "success": false,
 "error": "no start location found"
}
```
**or**

Status `404 Not Found`

```
{
 "success": false,
 "error": "no route found"
}
```

## Geocoding

### Get internal ID

Query internal ID of nearest OSM object to given lat-lon tupel.

    POST /geocoding/id

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| lat | float | Latitude |
| lon | float | Longitude |


#### Example

    POST /geocoding/id

```
{
 "lat": 50.051650,
 "lon": 6.514608685
}
```

#### Response

Status `200 OK`

```
{
 "id": 4265115
}
```

or in case of failure

Status `404 Not Found`

```
{
 "success": false,
 "error": "no osm object found"
}
```


### Get OSM ID

Query OSM ID of nearest OSM object to given lat-lon tupel.

    POST /geocoding/osm_id

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| lat | float | Latitude |
| lon | float | Longitude |


#### Example

    POST /geocoding/osm_id

```
{
 "lat": 50.051650,
 "lon": 6.514608685
}
```

#### Response

Status `200 OK`

```
{
 "osm_id": 4265115
}
```

or in case of failure

Status `404 Not Found`

```
{
 "success": false,
 "error": "no osm object found"
}
```


### Search Address

Get coordinates of given address.

    GET /geocoding/address/<address:string>

#### Parameters

*none*


#### Example

    GET /geocoding/address/<address:string>


#### Response

Status `200 OK`

```
{
"lon": 13.3888599,
"lat": 52.5170365
}
```

or in case of failure

Status `404 Not Found`

```
{
 "success": false,
 "error": "address not found"
}
```


### Search City

Get city of given coordinates.

    POST /geocoding/city

#### Parameters

| Name  | Type    | Description |
|-------|---------|-------------|
| lat | float | Latitude |
| lon | float | Longitude |


#### Example

    POST /geocoding/city

```
{
 "lat": 50.051650,
 "lon": 6.514608685
}
```


#### Response

Status `200 OK`

```
{
"city": "Düsseldorf"
}
```

or in case of failure

Status `404 Not Found`

```
{
 "success": false,
 "error": "no city found"
}
```


## Version

### Show version

Get server version

    GET /version


#### Parameters

*none*


#### Example

    GET /version


#### Response

Status `200 OK`

```
{
 "version": "0.1.2",
 "builddate": "2014-12-23T17:36:12.321Z",
 "git_branch": "master"
}
```

or in case of failure

Status `404 Not Found`
