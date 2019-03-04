CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT NOT NULL
);

CREATE TABLE location (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL REFERENCES product (id) ON DELETE CASCADE ON UPDATE RESTRICT,
  datetime TEXT NOT NULL CHECK (DATETIME(datetime) IS NOT NULL),
  longitude REAL NOT NULL,
  latitude REAL NOT NULL,
  elevation INTEGER NOT NULL
);
