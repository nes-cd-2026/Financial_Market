CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    asset_id INT REFERENCES assets(id),
    date DATE NOT NULL,
    price FLOAT NOT NULL
);
