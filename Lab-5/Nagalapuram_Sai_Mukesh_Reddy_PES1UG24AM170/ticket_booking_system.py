"""Movie theater ticket booking and seating management module."""

import hashlib
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Mark a seat as sold and record the reservation in order_history.

    Returns False if the seat does not exist or is already sold.
    """
    if order_history is None:
        order_history = []
    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False
    theater_seats[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Release a sold seat. Returns False if the seat does not exist."""
    try:
        theater_seats[seat_id]["is_sold"] = False
    except KeyError:
        return False
    return True


def check_seat_status(seat_id):
    """Return True if the seat exists and is still available."""
    if theater_seats.get(seat_id) is None:
        return False
    return not theater_seats[seat_id]["is_sold"]


def compute_discounted_price(seat_id, discount_percent):
    """Return the seat price after a discount of 0 to 100 percent."""
    base_price = theater_seats[seat_id]["price"]
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    return round(base_price * (100 - discount_percent) / 100, 2)


def generate_ticket_hash(ticket_code):
    """Return the SHA-256 hex digest of a ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a random four-digit booking PIN."""
    return 1000 + secrets.randbelow(9000)


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating chart to a text file."""
    with open(filename, "w", encoding="utf-8") as chart_file:
        chart_file.write(str(theater_seats))
    print("Seating chart exported to: " + filename)


def get_theater_summary(seats):
    """Return how many seats in the given seating chart are sold."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a short demonstration of the booking functions."""
    box_office_key = "BOX_OFFICE_SECRET_PASS_2026"
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))
    print("Box office token:", box_office_key)


main()
