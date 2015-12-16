# Database Structure

## Considerations

* Do not use *tokens*, instead let the user store his recorded *track ids*.
This is better data protection and tokens are not going to get used for special functions in future.
* Use *TEXT* for all columns containing strings.
See [this link](http://www.depesz.com/2010/03/02/charx-vs-varcharx-vs-varchar-vs-text/) for more information.
* time/timestamp is stored in PostgreSQL *timestamp* columns. 
*timestamp* columns provide 1 microsecond resolution, use 8 Byte and high value is 294276 AD.
* numeric data type precision: 
    * *numeric(11,8)* for distances < 100m
    * *numeric(16,8)* for bigger distances
    * cost values are *numeric(16,8)*


## Tables

#### *tracks*

Contains track metadata, hash of track points (*data_hash*) and bounding box

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | bigserial UNIQUE | public track id | |
| created | timestamp | creation timestamp (send by device) | |
| uploaded | timestamp | upload timestamp (server-side evaluated) | |
| length | numeric(16,8) | length (in meter) fo track | |
| duration| bigint | duration (in milliseconds) of track | |
| num_points | bigint | number of points (coordinates) of track | |
| public | boolean | true if track is public visible | |
| name | text | track name | |
| comment | text | user's comment on track | |
| city | text | city where track starts (or ends?) | |
| data_hash |text | sha256 hash of track points (to remove duplicates) | |
| **extension_geom** | Geometry(Polygon) | geometry box bounding track | |
| track_geom | Geometry(Linestring) | track geometry as PostGIS Linestring | |


#### *track_points*

This table contains the track points, ordered by track id from *tracks* table.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | (bigserial) | track id | [tracks](#tracks) -> id |
| **geom** | geometry(POINT,4326) | coordinates of track point | |
| altitude | numeric(16,8) | optional altitude of track point | |
| accuracy | numeric(11,8) | optional accuracy of gps fix (in meter) | |
| time | timestamp | timestamp of track point | |
| velocity | numeric(11,8) | optional velocity at tracl point | |
| shock | numeric(16,8) | optional *shock* value to quantify street quality | |


#### *users*

User table with user *name* (table index), sha256 hashed password, rights and enabled flag.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **name** | text UNIQUE | unique user name | |
| password | text | hash (sha256?) of user password | |
| rights | bigint | user rights (0 is super user) | |
| enabled | boolean | true if user is enabled | |


#### *profiles*

This table contains one entry per Routing profile with an unique *id* and a name.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | bigserial UNIQUE | routing profile (unique) id | |
| name | text | name of routing profile | |


#### *profile_description*

Contains description(s in different languages) for every routing profile from *profiles* table.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | (bigserial) | routing profile id | [profiles](#profiles) -> id |
| language | text | profile description language | |
| description | text | profile description | |


#### *way_types*

Contains *OSM* way types.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | text | *OSM* way type id | |


#### *way_types_description*

Extended internationalized description for every OSM way type.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | text | static cost way type id | [way_types](#way_types) -> id |
| description | text | description of way type | |
| language | text | language of way name and description | |


#### *cost_static*

Static cost value are stored in this table.
For every way type from OSM and every routing profile a reverse and forward cost value is stored.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **id** | text | *OSM* way type id | [way_types](#way_types) -> id |
| cost_forward | numeric(16,8) | forward cost for way type | |
| cost_reverse | numeric(16,8) | reverse cost for way type | |
| **profile** | (bigserial) | routing profile | [profiles](#profiles) -> id |

##### Constraints

* ( *id*, *profile* ) tupel is unique and indexed.


#### *cost_dynamic*

Dynamic cost value are stored in this table.
For each way segment in the local *pgRouting* database a reverse and forward cost value is stored.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **segment_id** | bigint | *pgRouting* segment id (external) | |
| track_id | (bigserial) | source of calculated dynamic cost | [tracks](#tracks) -> id |
| cost_forward | numeric(16,8) | forward cost for way segment | |
| cost_reverse | numeric(16,8) | reverse cost for way segment | |


#### *cost_dynamic_precalculated*

In table *cost_dynamic* for every way segment may exist more than 1 rows, so average of cost columns must be calculated.
In table *cost_dynamic_precalculated* the average cost values will be frequently calculated for each segment.

| Name  | Type | Description | foreign key |
|-------|------|-------------|-------------|
| **segment_id** | bigint UNIQUE | *pgRouting* segment id (external) | |
| cost_forward | numeric(16,8) | forward cost for way segment | |
| cost_reverse | numeric(16,8) | reverse cost for way segment | |
| relevance | numeric(16,8) | relevance of dynamic cost value depending on number of segments | |

