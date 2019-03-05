# Texada Challenge

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
