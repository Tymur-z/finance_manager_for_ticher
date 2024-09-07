from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"


class FinanceManager:
    def __init__(self):
        self.balance = 0
        self.reserve = 1000
        self.incomes = []
        self.expenses = []

    def add_income(self, source, amount):
        self.incomes.append({"source": source, "amount": amount})
        self.balance += amount

    def add_expense(self, category, amount):
        if self.balance - amount < self.reserve:
            return False
        self.expenses.append({"category": category, "amount": amount})
        self.balance -= amount
        return True

    def get_sorted_incomes(self):
        income_dict = {}
        for income in self.incomes:
            income_dict[income['source']] = income_dict.get(income['source'], 0) + income['amount']
        return dict(sorted(income_dict.items(), key=lambda x: x[1], reverse=True))

    def get_sorted_expenses(self):
        expense_dict = {}
        for expense in self.expenses:
            expense_dict[expense['category']] = expense_dict.get(expense['category'], 0) + expense['amount']
        return dict(sorted(expense_dict.items(), key=lambda x: x[1]))

    def total_income(self):
        return sum(income['amount'] for income in self.incomes)

    def total_expense(self):
        return sum(expense['amount'] for expense in self.expenses)

    def get_balance(self):
        return self.balance

    def get_reserve(self):
        return self.reserve


manager = FinanceManager()


@app.route("/")
def index():
    return render_template("index3.html", manager=manager)


@app.route("/add_income", methods=["POST"])
def add_income():
    source = request.form.get("source")
    amount = float(request.form.get("amount"))
    manager.add_income(source, amount)
    flash(f"Income of ${amount:.2f} added from {source}!", "success")
    return redirect(url_for("index"))


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    if not manager.add_expense(category, amount):
        flash("Operation denied! Balance would be below reserve.", "error")
        return redirect(url_for("index"))
    flash(f"Expense of ${amount:.2f} added to {category}!", "success")
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
