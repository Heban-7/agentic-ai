import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account("test_user", 1000.00)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.00)

    def test_deposit(self):
        self.account.deposit(500.00)
        self.assertEqual(self.account.balance, 1500.00)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.00)

    def test_withdraw(self):
        self.account.withdraw(300.00)
        self.assertEqual(self.account.balance, 700.00)

    def test_withdraw_negative(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.00)

    def test_withdraw_exceed_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1100.00)

    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.assertEqual(self.account.balance, 700.00)
        self.assertEqual(self.account.holdings['AAPL'], 2)

    def test_buy_shares_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 10)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 2)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.balance, 850.00)
        self.assertEqual(self.account.holdings['AAPL'], 1)

    def test_sell_shares_insufficient(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 2)

    def test_calculate_portfolio_value(self):
        self.account.buy_shares('AAPL', 2)
        value = self.account.calculate_portfolio_value()
        self.assertEqual(value, 700.00 + 300.00)

    def test_calculate_profit_loss(self):
        self.account.buy_shares('AAPL', 2)
        profit_loss = self.account.calculate_profit_loss()
        self.assertEqual(profit_loss, 0.00)

    def test_get_holdings(self):
        self.account.buy_shares('AAPL', 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 2})

    def test_get_transactions(self):
        self.account.deposit(500.00)
        self.account.withdraw(300.00)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 3)

if __name__ == '__main__':
    unittest.main()