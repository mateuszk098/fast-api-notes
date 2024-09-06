# **Quick Start**

Consider `full_stack_todo/` directory as the current working directory.

1. Create `.env` file. It should look as follows:

   ```bash
    SECRET_KEY = "YOUR_SECRET_KEY"
    ALGORITHM = "HS256"

    POSTGRES_USER = "admin" 
    POSTGRES_PASSWORD = "password"
    POSTGRES_DB = "TodoAppDB"

    PGADMIN_DEFAULT_EMAIL = "admin@gmail.com"
    PGADMIN_DEFAULT_PASSWORD = "password"
    ```

    Create `SECRET_KEY` with `openssl`, for example: `openssl rand -hex 32` and paste it above.

2. Go to `db/` directory and run `docker compose up --env-file ../.env -d`
3. Go to `localhost:80` and login to pgAdmin 4 using `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD`.
4. Register a new server. You can name it "TodoApp". Connection host can be found within container inspection, i.e. `docker inspect postgres`. In this case it should be `172.16.0.2`.
5. Create a new database with the name of `POSTGRES_DB` environment variable, paste the content of `todo-app-tables.sql` file into Query Tool and execute it. Now, there should be two new tables, i.e. `users` and `todos`.
6. Run application in reload mode `uvicorn app.app:app --reload` or using python script `python3 main.py` without reloading.
7. Go to `localhost:8000` to interact with the application or `localhost:8000/docs` to play with the Swagger UI.
