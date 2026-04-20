import psycopg2
import hashlib

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="frisk_expense",
        user="postgres",
        password="9825"
    )

def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


# USER MANAGEMENT CODE
# 🔹 Register User
def register_user(name, email, password, phone):
    try:
        conn = get_connection()
        cur = conn.cursor()

        hashed_password = hash_password(password)

        cur.execute(
            'INSERT INTO "Users" (name, email, password, phone) VALUES (%s, %s, %s, %s)',
            (name, email, hashed_password, phone)
        )

        conn.commit()
        cur.close()
        conn.close()

        return True   # ✅ important
    except Exception as e:
        print(e)
        return False


# 🔹 Login User
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    cur.execute(
        'SELECT * FROM "Users" WHERE email=%s AND password=%s',
        (email, hashed_password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


# 🔹 Update Password
def update_password(email, new_password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(new_password)

    cur.execute(
        'UPDATE "Users" SET password=%s WHERE email=%s',
        (hashed_password, email)
    )

    conn.commit()

    cur.close()
    conn.close()

    return True


#INCOME MANAGEMENT CODE
def add_income(user_id, amount, source, date):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO income (user_id, amount, source, date)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, amount, source, date))
    conn.commit()

    cursor.close()
    conn.close()

    return True


# 🔹 Get All Income
def get_all_income(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, amount, source, date FROM income WHERE user_id = %s AND is_deleted = FALSE ORDER BY date DESC"
    cursor.execute(query, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_all_income(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, amount, source, date FROM income WHERE user_id = %s AND is_deleted = FALSE ORDER BY date DESC"
    cursor.execute(query, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_all_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, amount, category, date FROM expense WHERE user_id = %s AND is_deleted = FALSE ORDER BY date DESC"
    cursor.execute(query, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# 🔹 Delete Income
def delete_income(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE income SET is_deleted = TRUE WHERE id = %s"
    cursor.execute(query, (income_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return True

def delete_expense(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE expense SET is_deleted = TRUE WHERE id = %s"
    cursor.execute(query, (income_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return True


def update_income(income_id, amount, source, date):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE income
    SET amount = %s, source = %s, date = %s
    WHERE id = %s
    """

    cursor.execute(query, (amount, source, date, income_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True


def update_expense(expense_id, amount, category, date):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE expense
    SET amount = %s, category = %s, date = %s
    WHERE id = %s
    """

    cursor.execute(query, (amount, category, date, expense_id))
    conn.commit()

    cursor.close()
    conn.close()
    return True

def add_expense(amount,category,date,user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expense (amount, category, date,user_id) VALUES (%s, %s, %s,%s)",
        (amount, category, date,user_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return True