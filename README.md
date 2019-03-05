# Flask example app

## Install dependencies
```
$ pip install -e .
```

## Run Flask dev server
```
$ export FLASK_APP=api
$ export FLASK_ENV=development  # optional
$ python -m flask init-db       # initialize Sqlite database instance/db.sqlite with api/schema.sql
$ python -m flask run
```

## Run tests
`$ python setup.py test`

## Configuration
Optional configuration file `instance/config.py`:
```
DATABASE=/i/want/to/put/database/to/somewhere/else
```

## API
Accept and response with `Content-Type: application/json`.

### Create a product
```
POST /products
```
Example request body:
```
{
  "description": "Fancy 2000"
}
```
Example response body:
```
{
  "id": 1,
  "description": "Fancy 2000"
}
```

### List products
```
GET /products?mark=0&limit=1000
```
Example response body:
```
{
  "pagination": {"next_mark": 3},
  "products": [
    {
      "id": 1,
      "description": "Fancy 2000"
    },
    ...
  ]
}
```

### Get a product
```
GET /products/1
```
Example response body:
```
{
  "id": 1,
  "description": "Fancy 2000"
}
```

### Update a product
```
PUT /products/1
```
Example request body:
```
{
  "id":1,
  "description": "Fancy 2001"
}
```

### Delete a product
```
DELETE /products/1
```

### Create a location
```
POST /locations
```
Example request body:
```
{
  "product_id": 1,
  "datetime": "2010-10-10T08:00:00-04:00",
  "longitude": 33,
  "latitude": -33,
  "elevation": 33
}
```
Example response body:
```
{
  "id": 1,
  "product_id": 1,
  "datetime": "2010-10-10T08:00:00-04:00",
  "longitude": 33,
  "latitude": -33,
  "elevation": 33
}
```

### Get a location
```
GET /locations/1
```
Example response body:
```
{
  "id": 1,
  "product_id": 1,
  "datetime": "2010-10-10T08:00:00-04:00",
  "longitude": 33,
  "latitude": -33,
  "elevation": 33
}
```

### List locations
```
GET /locations?mark=0&limit=1000&product_id=1&from=2016-10-12T17:00:00&to=2016-10-13T17:00:00
```
Example response body:
```
{
  "pagination": {"next_mark": 3},
  "locations": [
    {
      "id": 1,
      "product_id": 1,
      "datetime": "2010-10-10T08:00:00-04:00",
      "longitude": 33,
      "latitude": -33,
      "elevation": 33
    },
    ...
  ]
}
```

### Update a location
```
PUT /locations/1
```
Example request body:
```
{
  "id": 1,
  "datetime": "2010-10-19T08:00:00-04:00",
  "longitude": 3,
  "latitude": -3,
  "elevation": 3
}
```

### Delete a location
```
DELETE /locations/1
```
