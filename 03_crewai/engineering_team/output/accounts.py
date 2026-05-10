class Account:
    def __init__(self, username: str, initial_deposit: float):
        self.username = username
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount})

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Withdrawal would result in a negative balance.")
        self.balance -= amount
        self.transactions.append({"type": "withdraw", "amount": amount})

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        price = get_share_price(symbol)
        total_cost = price * quantity
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append({"type": "buy", "symbol": symbol, "quantity": quantity, "price": price, "total": total_cost})

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")
        price = get_share_price(symbol)
        total_earnings = price * quantity
        self.balance += total_earnings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({"type": "sell", "symbol": symbol, "quantity": quantity, "price": price, "total": total_earnings})

    def calculate_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_profit_loss(self) -> float:
        return self.calculate_profit_loss()

    def get_transactions(self) -> list:
        return self.transactions


def get_share_price(symbol: str) -> float:
    if symbol == 'AAPL':
        return 150.00
    elif symbol == 'TSLA':
        return 750.00
    elif symbol == 'GOOGL':
        return 2800.00
    else:
        raise ValueError("Unrecognized symbol.")