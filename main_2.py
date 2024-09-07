from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

class FinanceManager:
    def __init__(self):
        self.balance = 0
        self.reserve = 0  # Недоторканний запас (НЗ)
        self.incomes = {}
        self.expenses = {}

    def add_income(self, source, amount):
        self.incomes[source] = self.incomes.get(source, 0) + amount
        self.balance += amount

    def add_expense(self, category, amount):
        if self.balance - amount < self.reserve:
            return False
        self.expenses[category] = self.expenses.get(category, 0) + amount
        self.balance -= amount
        return True

    def get_sorted_incomes(self):
        return dict(sorted(self.incomes.items(), key=lambda x: x[1], reverse=True))

    def get_sorted_expenses(self):
        return dict(sorted(self.expenses.items(), key=lambda x: x[1]))

    def total_income(self):
        return sum(self.incomes.values())

    def total_expense(self):
        return sum(self.expenses.values())

    def get_balance(self):
        return self.balance

    def get_reserve(self):
        return self.reserve

manager = FinanceManager()

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/add_income", methods=["POST"])
def add_income():
    source = request.form.get("source")
    amount = float(request.form.get("amount"))
    manager.add_income(source, amount)
    flash(f"Income of {amount} added from {source}!", "success")
    return redirect(url_for("index"))

@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    if not manager.add_expense(category, amount):
        flash("Operation denied! Balance would be below reserve.", "error")
        return redirect(url_for("index"))
    flash(f"Expense of {amount} added to {category}!", "success")
    return redirect(url_for("index"))

@app.route("/get_data")
def get_data():
    return jsonify({
        "incomes": manager.get_sorted_incomes(),
        "expenses": manager.get_sorted_expenses(),
        "total_income": manager.total_income(),
        "total_expense": manager.total_expense(),
        "balance": manager.get_balance(),
        "reserve": manager.get_reserve()
    })

if __name__ == "__main__":
    app.run(debug=True)
