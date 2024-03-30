CREATE TABLE log_data (
    id SERIAL PRIMARY KEY,
    entry_date DATE NOT NULL
);

CREATE TABLE food (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    protein INTEGER NOT NULL,
    carbohydrate INTEGER NOT NULL,
    fat INTEGER NOT NULL,
    calories INTEGER NOT NULL
);

CREATE TABLE food_log (
    food_id INTEGER,
    log_date_id INTEGER,
    PRIMARY KEY (food_id, log_date_id),
    FOREIGN KEY (food_id) REFERENCES food (id),
    FOREIGN KEY (log_date_id) REFERENCES log_data (id)
);
