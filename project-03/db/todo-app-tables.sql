DROP      TABLE IF EXISTS users;

CREATE    TABLE users (
          id SERIAL,
          email VARCHAR(200) DEFAULT NULL,
          username VARCHAR(45) DEFAULT NULL,
          first_name VARCHAR(45) DEFAULT NULL,
          last_name VARCHAR(45) DEFAULT NULL,
          hashed_password BYTEA DEFAULT NULL,
          is_active BOOLEAN DEFAULT NULL,
          phone_number VARCHAR(45) DEFAULT NULL,
          role VARCHAR(45) DEFAULT NULL,
          PRIMARY KEY (id)
          );

DROP      TABLE IF EXISTS todos;

CREATE    TABLE todos (
          id SERIAL,
          title VARCHAR(200) DEFAULT NULL,
          description VARCHAR(200) DEFAULT NULL,
          priority INTEGER DEFAULT NULL,
          complete BOOLEAN DEFAULT NULL,
          owner_id INTEGER DEFAULT NULL,
          PRIMARY KEY (id),
          FOREIGN KEY (owner_id) REFERENCES users (id)
          );