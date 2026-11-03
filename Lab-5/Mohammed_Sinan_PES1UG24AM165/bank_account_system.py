"""Bank account management module."""

import ast
import hashlib
import operator
import os
import secrets

account_data = {}

_SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _evaluate_node(node, variables):
    """Recursively evaluate allowed AST nodes safely."""
    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body, variables)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        raise ValueError(f"Undefined variable: {node.id}")
    if isinstance(node, ast.BinOp):
        operation = _SAFE_OPS.get(type(node.op))
        if operation is None:
            raise ValueError(f"Unsupported operator: {type(node.op)}")
        left_val = _evaluate_node(node.left, variables)
        right_val = _evaluate_node(node.right, variables)
        return operation(left_val, right_val)
    raise ValueError(f"Unsupported expression: {type(node)}")


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create a new bank account with an initial deposit."""
    if transactions is None:
        transactions = []
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    log_msg = f"Created {acc_id} with initial balance {initial_deposit}"
    transactions.append(log_msg)
    return True


def deposit(acc_id, amount):
    """Deposit a given amount into the specified account."""
    if acc_id not in account_data:
        return False
    account_data[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw an amount from account if balance is sufficient."""
    if account_data.get(acc_id) is None:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
    account_data[acc_id]["balance"] -= amount
    return True


def compute_bonus(acc_id, expr):
    """Safely compute promotional bonus for an account balance."""
    bal = account_data[acc_id]["balance"]
    parsed = ast.parse(expr, mode="eval")
    bonus = _evaluate_node(parsed, {"bal": bal})
    return bonus


def get_hash(pin):
    """Compute secure SHA-256 hash digest for a given PIN string."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def generate_temp_pin():
    """Generate a cryptographically secure 4-digit temporary PIN."""
    return secrets.SystemRandom().randint(1000, 9999)


def backup_data(filename="backup.txt"):
    """Backup the account ledger data to a file securely."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(account_data))
    print(f"Backup complete: {filename}")


def main():
    """Run bank account system sample operations."""
    admin_token = os.getenv("ADMIN_TOKEN", "SUPER_SECRET_BANK_TOKEN_2026")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


if __name__ == "__main__":
    main()
