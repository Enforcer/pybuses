from decimal import Decimal

from pybuses import EventBus


class PaymentMade:
    amount: Decimal
    who: int

    def __init__(self, amount: Decimal, who: int) -> None:
        self.amount = amount
        self.who = who


def handler(payment_made: PaymentMade) -> None:
    print(f'Oh, cool! {payment_made.who} paid {payment_made.amount / 100}$!')


event_bus = EventBus()
event_bus.subscribe(handler)
event_bus.post(PaymentMade(Decimal('10.99'), 123))
