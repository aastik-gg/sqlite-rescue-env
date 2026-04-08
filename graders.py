import sqlite3

def grade_easy_task(db_path: str) -> float:
    """Agent must trim whitespace from names and standardize dates to YYYY-MM-DD."""
    actual_score = 0.0
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT name, signup_date FROM customers ORDER BY id")
            rows = c.fetchall()
            
            if rows:
                correct_rows = 0
                expected = [
                    ('Alice', '2022-12-31'),
                    ('Bob', '2023-01-15'),
                    ('Charlie', '2023-05-14'),
                    ('David', '2023-11-01')
                ]
                
                for actual, exp in zip(rows, expected):
                    if actual[0] == exp[0] and actual[1] == exp[1]:
                        correct_rows += 1
                        
                actual_score = float(correct_rows) / len(expected)
    except sqlite3.Error:
        actual_score = 0.0

    # THE VALIDATOR CLAMP
    if actual_score >= 1.0: return 0.99
    if actual_score <= 0.0: return 0.01
    return actual_score


def grade_medium_task(db_path: str) -> float:
    """Agent must create 'customers' and 'orders' tables with proper references."""
    score = 0.0
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            
            # Check if target tables exist (0.4 points)
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('customers', 'orders')")
            tables = [row[0] for row in c.fetchall()]
            if 'customers' in tables and 'orders' in tables:
                score += 0.4
                
                # Check if customers are deduplicated correctly (0.3 points)
                c.execute("SELECT COUNT(*) FROM customers")
                if c.fetchone()[0] == 2: # Alice and Bob
                    score += 0.3
                    
                # Check if orders map correctly to customers (0.3 points)
                c.execute("SELECT COUNT(*) FROM orders")
                if c.fetchone()[0] == 3:
                    score += 0.3
    except sqlite3.Error:
        pass
        
    # THE VALIDATOR CLAMP
    if score >= 1.0: return 0.99
    if score <= 0.0: return 0.01
    return score


def grade_hard_task(db_path: str) -> float:
    """Agent must create a view 'account_balances' calculating net balance (credit - debit)."""
    actual_score = 0.0
    try:
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            # Check if the view exists and has the correct logic
            c.execute("SELECT account_id, net_balance FROM account_balances ORDER BY account_id")
            rows = c.fetchall()
            
            expected = [(101, 250.0), (102, 1000.0)]
            if rows == expected:
                actual_score = 1.0
    except sqlite3.Error:
        actual_score = 0.0

    # THE VALIDATOR CLAMP
    if actual_score >= 1.0: return 0.99
    if actual_score <= 0.0: return 0.01
    return actual_score
