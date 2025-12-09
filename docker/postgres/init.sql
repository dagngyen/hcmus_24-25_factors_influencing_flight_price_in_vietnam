CREATE TABLE IF NOT EXISTS flight_prices (
    timestamp TIMESTAMP,
    id_departure VARCHAR(10),
    id_arrival VARCHAR(10),
    departure_datetime TIMESTAMP,
    arrival_datetime TIMESTAMP,
    airline_name VARCHAR(100),
    travel_class VARCHAR(50),
    is_nonstop BOOLEAN,
    price DECIMAL(10, 2)
);