"""Digital Wallet & Payment Tracker.

A small payment wallet demo: sends a one-time password, tops up the balance,
pays merchants after a PIN check and a daily limit, prints a mini statement,
works out cashback and verifies a payment-gateway key.
"""
import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

# Secrets are read from the environment instead of being hardcoded (B105).
GATEWAY_SECRET = os.environ.get("WALLET_GATEWAY_SECRET", "")
WALLET_PIN_HASH = os.environ.get(
    "WALLET_PIN_HASH",
    # SHA-256 of the demo PIN, so the plain PIN is not stored in source.
    "fe2592b42a727e977f055947385b709cc82b16b9a87f88c6abf3900d65d0cdc3")
CASHBACK_RATE = 0.02

wallet = {"balance": 0.0, "daily_limit": 1000}
transactions = []


def hash_pin(pin):
    """Return the SHA-256 hex digest of a PIN."""
    return hashlib.sha256(pin.encode()).hexdigest()


def add_money(amount, source="UPI", log=None):
    """Credit the wallet; returns False for non-positive amounts."""
    if log is None:
        log = []
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Change the maximum amount allowed for a single payment."""
    wallet["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Pay a merchant after verifying the PIN, balance and daily limit."""
    if not hmac.compare_digest(hash_pin(pin), WALLET_PIN_HASH):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > wallet["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def mini_statement(count=3):
    """Print the last `count` transactions."""
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type=None):
    """Return the cashback earned on a payment (flat 2% for every type)."""
    _ = merchant_type  # kept for API compatibility; rate is the same today
    return round(amount * CASHBACK_RATE, 2)


def check_gateway(secret):
    """Verify a payment-gateway key in constant time."""
    return bool(GATEWAY_SECRET) and hmac.compare_digest(secret, GATEWAY_SECRET)


def receipt_path():
    """Create a private temporary file for a receipt and return its path."""
    # Helper kept for the lab: not called by the demo
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    return path


def main():
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts = [t["amount"] for t in transactions
                      if t["type"] == "credit"]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
