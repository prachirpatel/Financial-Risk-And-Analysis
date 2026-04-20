from flask import Flask, request, jsonify, render_template,session,redirect
from config.connection import register_user, login_user, update_password
import smtplib
import random
import string
from config.connection import add_income, get_all_income, delete_income, update_income,add_expense,get_all_expense,delete_expense,update_expense
app = Flask(__name__)
app.secret_key = "P1234"

@app.route('/')
def main():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
     
        return redirect('/home')     
    
# Register API routes
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # 🔥 destroy session
    return redirect('/login')

@app.route('/forgot-password', methods=['GET'])
def forgot_page():
    return render_template('forgot.html')

@app.route('/home')
def home_page():
    if 'user_id' not in session:
        return redirect('/login')  # 🔒 protect page

    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    success = register_user(
        data['name'],
        data['email'],
        data['password'],
        data['phone']
    )

    if success:
        return jsonify({
                "message": "Registered Successfully",
                "redirect": "/login"
    }) 
    else:
        return jsonify({"message": "Error registering user"}), 500

# 🔹 Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = login_user(data['email'], data['password'])
    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_email'] = user[2]
        return jsonify({
          "message": "Login Success",
           "redirect": "/home"
        })
    else:
     return jsonify({
        "message": "Invalid Email or Password"
    }), 401

@app.route('/add-income', methods=['POST'])
def add_income_api():
    data = request.get_json()

    user_id = session['user_id']
    amount = data['amount']
    source = data['source']
    date = data['date']

    success = add_income(user_id, amount, source, date)

    if success:
        return jsonify({"message": "Income added successfully"})
    else:
        return jsonify({"message": "Error adding income"}), 500

@app.route('/get-income', methods=['GET'])
def get_income_api():
    user_id =session['user_id']
    rows = get_all_income(user_id)

    income_list = []
    for r in rows:
        income_list.append({
            "id": r[0],
            "amount": float(r[1]),
            "source": r[2],
            "date": str(r[3])
        })

    return jsonify(income_list)

@app.route('/get-expense', methods=['GET'])
def get_expense_api():
    user_id =session['user_id']
    rows = get_all_expense(user_id)

    income_list = []
    for r in rows:
        income_list.append({
            "id": r[0],
            "amount": float(r[1]),
            "category": r[2],
            "date": str(r[3])
        })

    return jsonify(income_list)

@app.route('/delete-income/<int:id>', methods=['DELETE'])
def delete_income_api(id):
    success = delete_income(id)

    if success:
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"message": "Error deleting"}), 500
    
@app.route('/delete-expense/<int:id>', methods=['DELETE'])
def delete_expense_api(id):
    success = delete_expense(id)

    if success:
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"message": "Error deleting"}), 500
        
# 🔹 Edit Income API
@app.route('/update-income/<int:id>', methods=['PUT'])
def update_income_api(id):
    data = request.get_json()

    amount = data['amount']
    source = data['source']
    date = data['date']

    success = update_income(id, amount, source, date)

    if success:
        return jsonify({"message": "Income updated successfully"})
    else:
        return jsonify({"message": "Error updating income"}), 500    


@app.route('/update-expense/<int:id>', methods=['PUT'])
def update_expense_api(id):
    data = request.get_json()

    amount = data['amount']
    category = data['category']
    date = data['date']

    success = update_expense(id, amount, category, date)

    if success:
        return jsonify({"message": "Expense updated successfully"})
    else:
        return jsonify({"message": "Error updating income"}), 500    

@app.route("/add-expense", methods=["POST"])
def add_expense_api():
    data = request.json
    user_id = session['user_id']
    amount = data.get("amount")
    category = data.get("category")
    date = data.get("date")
    success=add_expense(amount,category,date,user_id)
    if success:
        return jsonify({"message": "Expense added successfully"})
    else:
        return jsonify({"message": "Error adding expense"}), 500

@app.route('/analysis', methods=['GET'])
def get_analysis():
    user_id = session['user_id']

    income_rows = get_all_income(user_id)
    expense_rows = get_all_expense(user_id)

    total_income = sum(float(i[1]) for i in income_rows)
    total_expense = sum(float(e[1]) for e in expense_rows)

    category_expense_data = {}
    for e in expense_rows:
        category = e[2]
        amount = float(e[1])

        if category in category_expense_data:
            category_expense_data[category] += amount
        else:
            category_expense_data[category] = amount

    category_income_data = {}
    for e in income_rows:
        category = e[2]
        amount = float(e[1])

        if category in category_income_data:
            category_income_data[category] += amount
        else:
            category_income_data[category] = amount

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "category_expense_data": category_expense_data,
        "category_income_data": category_income_data,
    })


@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    user_id = session['user_id']

    income_rows = get_all_income(user_id)
    expense_rows = get_all_expense(user_id)

    total_income = sum(float(i[1]) for i in income_rows)
    total_expense = sum(float(e[1]) for e in expense_rows)
    transactions = []

    # 🔹 Income Data
    for i in income_rows:
        transactions.append({
            "type": "income",   # 🔥 flag
            "amount": float(i[1]),
            "category": i[2],
            "date": str(i[3])
        })

    # 🔹 Expense Data
    for e in expense_rows:
        transactions.append({
            "type": "expense",  # 🔥 flag
            "amount": float(e[1]),
            "category": e[2],
            "date": str(e[3])
        })

    # 🔥 SORT by latest date
    transactions.sort(
        key=lambda x: x["date"], 
        reverse=True
    )
   
    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "transaction": transactions,
    })

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data["email"]
    new_password = generate_password()
    print(new_password)
    update_password(email, new_password)
    send_new_password(email,new_password)
    return jsonify({"message": "New password sent to your email"})

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def send_new_password(email, new_password):
    sender_email = "patelprachi8141@gmail.com"
    app_password = "bxkj kekl xefm vyul"

    subject = "Your New Password"
    message = f"Your new password is: {new_password}"

    email_text = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, email, email_text)
    server.quit()


@app.route('/risk-analysis', methods=['GET'])
def risk_analysis():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']

    income_rows = get_all_income(user_id)
    expense_rows = get_all_expense(user_id)

    total_income = sum(float(i[1]) for i in income_rows)
    total_expense = sum(float(e[1]) for e in expense_rows)

    savings = total_income - total_expense

    # Avoid division error
    if total_income == 0:
        risk_score = 100
    else:
        expense_ratio = total_expense / total_income
        risk_score = round(expense_ratio * 100, 2)

    # Risk classification
    if risk_score < 50:
        risk_level = "Low"
    elif risk_score < 80:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "risk_score": risk_score,
        "risk_level": risk_level
    })


if __name__ == "__main__":
  app.run(debug=True)