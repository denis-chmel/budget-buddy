from yoyo import step

steps = [
    step("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(64) NOT NULL UNIQUE,
            email VARCHAR(256) UNIQUE,
            full_name VARCHAR(256),
            hashed_password VARCHAR(256) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    # Rollback SQL
    "DROP TABLE users")
]
