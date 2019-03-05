CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT NOT NULL CHECK (description != '')
);

CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL REFERENCES product (id) ON DELETE CASCADE ON UPDATE RESTRICT,
  datetime TEXT NOT NULL CHECK (DATETIME(datetime) IS NOT NULL AND DATETIME(datetime) == datetime),
  longitude REAL NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
  latitude REAL NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
  elevation INTEGER NOT NULL
);
