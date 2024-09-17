import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.database.user_db_requests import (
    get_user_id,
    get_transaction_history,
    get_user_transactions,
    get_user_balance,
    process_transactions,
    calculate_profit,
    get_symbol_transactions,
    check_balance,
    update_balance,
    insert_transaction,
    buy_sell_stock,
    get_ranking,
    calculate_total_profit
)

class TestUserDbRequests(unittest.TestCase):

    def setUp(self):
        self.db_mock = MagicMock()
        self.username = "test_user"
        self.user_id = 1
        self.stock_symbol = "AIR.DE"
        self.current_price = 150
        self.quantity = 10
        self.price_per_stock = 140
        self.total_cost = 1500.00
        self.transaction_data = [
            (1, self.stock_symbol, self.quantity, 1500.00, 145.00, datetime.now())
        ]
        self.user_balance = 5000.00

    def test_get_user_id(self):
        self.db_mock.execute.return_value.fetchone.return_value = (self.user_id,)
        result = get_user_id(self.username, self.db_mock)
        self.assertEqual(result, self.user_id)
        self.db_mock.execute.assert_called_with((
        '''
        SELECT id FROM user WHERE username = ?
        '''
     ) , (self.username,))

    def test_get_transaction_history(self):
        self.db_mock.execute.return_value.fetchall.return_value = self.transaction_data
        result = get_transaction_history(self.username, self.db_mock)
        expected_result = {
            self.stock_symbol: [{
                'id': 1,
                'quantity': self.quantity,
                'amount': "{:.2f}".format(1500.00),
                'price': "{:.2f}".format(145.00),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }]
        }
        self.assertEqual(result, expected_result)
        query = ('''SELECT t.id, t.symbol, t.quantity, t.amount, t.price, t.t_timestamp FROM transactionHistory t JOIN user u on t.user_id = u.id WHERE u.username = ? ORDER BY t.t_timestamp DESC''')
        self.db_mock.execute.assert_called_with(query, (self.username,))
              

    def test_get_user_transactions(self):
        self.db_mock.execute.return_value.fetchall.return_value = [
            (self.stock_symbol, self.quantity, self.price_per_stock)
        ]
        result = get_user_transactions(self.username, self.db_mock)
        expected_result = [(self.stock_symbol, self.quantity, self.price_per_stock)]
        self.assertEqual(result, expected_result)
        self.db_mock.execute.assert_called_with(
        """SELECT t.symbol, SUM(t.quantity) AS total_quantity, AVG(t.price) AS average_price 
        FROM transactionHistory t 
        JOIN user u ON t.user_id = u.id 
        WHERE u.username = ? 
        GROUP BY t.symbol 
        HAVING total_quantity > 0"""
        , (self.username,)
        )

    def test_get_user_balance(self):
        self.db_mock.execute.return_value.fetchone.return_value = (self.user_balance,)
        result = get_user_balance(self.username, self.db_mock)
        self.assertEqual(result, str(self.user_balance))
        self.db_mock.execute.assert_called_with(
        "SELECT balance " 
        "FROM account "
        "WHERE user_id = (SELECT id FROM user WHERE username = ?) "
        , (self.username,)
        )


    def test_calculate_profit(self):
        result = calculate_profit(self.current_price, self.price_per_stock)
        expected_result = ((self.current_price / self.price_per_stock) - 1) * 100
        self.assertEqual(result, round(expected_result, 2))

    @patch('app.database.user_db_requests.process_transactions')
    def test_get_symbol_transactions(self, mock_process_transactions):
        mock_process_transactions.return_value = [{
            "symbol": self.stock_symbol,
            "name": "Airbus SE",
            "amount": self.quantity,
            "price": "{:.2f}".format(self.current_price),
            "total": "{:.2f}".format(self.total_cost),
            "profit": calculate_profit(self.current_price, self.price_per_stock)
        }]
        result = get_symbol_transactions(self.username, self.stock_symbol, self.db_mock)
        expected_result = {
            "symbol": self.stock_symbol,
            "name": "Airbus SE",
            "amount": self.quantity,
            "price": "{:.2f}".format(self.current_price),
            "total": "{:.2f}".format(self.total_cost),
            "profit": calculate_profit(self.current_price, self.price_per_stock)
        }
        self.assertEqual(result, expected_result)
        mock_process_transactions.assert_called_with(get_user_transactions(self.username, self.db_mock))

    def test_check_balance(self):
        result = check_balance(self.user_balance, self.total_cost)
        self.assertTrue(result)
        result = check_balance(self.total_cost - 10, self.total_cost)
        self.assertFalse(result)


    def test_get_ranking(self):
        self.db_mock.execute.return_value.fetchall.return_value = [(self.username,)]
        with patch('app.database.user_db_requests.calculate_total_profit') as mock_calculate_total_profit:
            mock_calculate_total_profit.return_value = 100.00
            result = get_ranking(self.db_mock)
            expected_result = [{
                "username": self.username,
                "profit": 100.00,
                "rank": 1
            }]
            self.assertEqual(result, expected_result)
            mock_calculate_total_profit.assert_called_with(self.username, self.db_mock)

    @patch('app.database.user_db_requests.process_transactions')
    def test_calculate_total_profit(self, mock_process_transactions):
        mock_process_transactions.return_value = [{
            "profit": 100.00
        }]
        result = calculate_total_profit(self.username, self.db_mock)
        self.assertEqual(result, 100.00)
        mock_process_transactions.assert_called_with(get_user_transactions(self.username, self.db_mock))

if __name__ == '__main__':
    unittest.main()
