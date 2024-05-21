import datetime


class Event:
    def __init__(self, id):
        self.id = id
        self.timestamp = datetime.datetime.now()


class AccountCreated(Event):
    def __init__(self, id, owner):
        super().__init__(id)
        self.owner = owner


class MoneyDeposited(Event):
    def __init__(self, id, amount):
        super().__init__(id)
        self.amount = amount


class MoneyWithdrawn(Event):
    def __init__(self, id, amount):
        super().__init__(id)
        self.amount = amount


class EventStore:
    def __init__(self):
        self.events = {}

    def add_event(self, event):
        if event.id not in self.events:
            self.events[event.id] = []
        self.events[event.id].append(event)

    def get_events(self, id):
        return self.events.get(id, [])


class Account:
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        return MoneyDeposited(self.id, amount)

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return MoneyWithdrawn(self.id, amount)
        else:
            raise ValueError("Insufficient balance")


class AccountCommandHandler:
    def __init__(self, event_store):
        self.event_store = event_store

    def handle_create_account(self, id, owner):
        account_created = AccountCreated(id, owner)
        self.event_store.add_event(account_created)

    def handle_deposit(self, id, amount):
        events = self.event_store.get_events(id)
        account = Account(id, None)
        for event in events:
            if isinstance(event, AccountCreated):
                account.owner = event.owner
            elif isinstance(event, MoneyDeposited):
                account.balance += event.amount
            elif isinstance(event, MoneyWithdrawn):
                account.balance -= event.amount
        new_event = account.deposit(amount)
        self.event_store.add_event(new_event)

    def handle_withdraw(self, id, amount):
        events = self.event_store.get_events(id)
        account = Account(id, None)
        for event in events:
            if isinstance(event, AccountCreated):
                account.owner = event.owner
            elif isinstance(event, MoneyDeposited):
                account.balance += event.amount
            elif isinstance(event, MoneyWithdrawn):
                account.balance -= event.amount
        new_event = account.withdraw(amount)
        self.event_store.add_event(new_event)


if __name__ == "__main__":
    event_store = EventStore()
    command_handler = AccountCommandHandler(event_store)

    # Create an account
    command_handler.handle_create_account("acc-123", "Alice")

    # Deposit money
    command_handler.handle_deposit("acc-123", 100)

    # Withdraw money
    command_handler.handle_withdraw("acc-123", 50)

    # Print balance
    events = event_store.get_events("acc-123")
    account = Account("acc-123", None)
    for event in events:
        if isinstance(event, AccountCreated):
            account.owner = event.owner
        elif isinstance(event, MoneyDeposited):
            account.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            account.balance -= event.amount

    print(f"Account Owner: {account.owner}")
    print(f"Account Balance: {account.balance}")
