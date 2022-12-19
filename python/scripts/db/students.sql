CREATE TABLE IF NOT EXISTS :students_table_full_name
(
    id       INTEGER     NOT NULL
        CONSTRAINT :students_table_pk
            PRIMARY KEY,
    name     VARCHAR(30) NOT NULL,
    birthday DATE        NOT NULL,
    sex      CHAR        NOT NULL,
    room     INTEGER     NOT NULL
        CONSTRAINT :students_rooms_id_fk
            REFERENCES :rooms_table_full_name
            ON UPDATE CASCADE ON DELETE CASCADE
);

ALTER TABLE :students_table_full_name
    OWNER TO :username;

CREATE INDEX :students_room_index
    ON :students_table_full_name (room);

