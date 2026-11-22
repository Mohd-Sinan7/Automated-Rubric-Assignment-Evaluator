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
wallet = {"balance": 0.0}
daily_limit = 1000
transactions = []


def hashPin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def addMoney(amount, source="UPI", log=[]):
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def setDailyLimit(newLimit):
    global daily_limit
    daily_limit = newLimit


def payMerchant(merchant, amount, pin):
    if not hmac.compare_digest(hashPin(pin), WALLET_PIN_HASH):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def miniStatement(count=3):
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashbackFor(amount, merchantType):
    return round(amount * 0.02, 2)


def checkGateway(secret):
    return bool(GATEWAY_SECRET) and hmac.compare_digest(secret, GATEWAY_SECRET)


def receiptPath():
    # Helper kept for the lab: not called by the demo
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    return path


def main():
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    addMoney(2000)
    addMoney(500, "Card")
    addMoney(-10)
    setDailyLimit(1500)
    payMerchant("Coffee Corner", 180, "4321")
    payMerchant("Book Store", 5000, "4321")
    payMerchant("Grocery Mart", 350, "0000")
    payMerchant("Pharmacy", 420, "4321")
    miniStatement()
    print("Cashback on 420:", cashbackFor(420, "health"))
    print("Gateway check:", checkGateway("wrong")) # should be False
    print("Final balance: Rs.", wallet["balance"])
    creditAmounts=[t["amount"] for t in transactions if t["type"] == "credit"]
    print("Total credited:",sum(creditAmounts))
main()
