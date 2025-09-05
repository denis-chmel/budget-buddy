from yoyo import step

steps = [
    step("""
        CREATE TABLE transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            type VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE INDEX idx_transactions_user_id ON transactions(user_id);
        CREATE INDEX idx_transactions_date ON transactions(date);
        CREATE INDEX idx_transactions_type ON transactions(type);
    """,
    # Rollback SQL
    """
        DROP INDEX IF EXISTS idx_transactions_date;
        DROP INDEX IF EXISTS idx_transactions_user_id;
        DROP INDEX IF EXISTS idx_transactions_type;
        DROP TABLE transactions;
    """)
]
