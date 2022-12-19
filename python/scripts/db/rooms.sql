CREATE TABLE IF NOT EXISTS :rooms_table_full_name
(
    id   INTEGER     NOT NULL
        CONSTRAINT :rooms_table_pk
            PRIMARY KEY,
    name VARCHAR(15) NOT NULL
);

ALTER TABLE :rooms_table_full_name
    OWNER TO :username;
