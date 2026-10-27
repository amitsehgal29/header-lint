import unittest
from header_lint import lint, snake

class T(unittest.TestCase):
    def kinds(self, hs):
        return {(i["header"], i["issue"]) for i in lint(hs)}
    def test_clean(self):
        self.assertEqual(lint(["order_id", "amount", "created_at"]), [])
    def test_problems(self):
        k = self.kinds(["id", "ID", " name", "", "Order Date", "user"])
        self.assertIn(("id", "duplicate (case-insensitive)"), k)
        self.assertIn((" name", "leading/trailing whitespace"), k)
        self.assertIn(("", "blank"), k)
        self.assertIn(("Order Date", "not snake_case"), k)
        self.assertIn(("user", "SQL reserved word"), k)
    def test_snake(self):
        self.assertEqual(snake("Order Date"), "order_date")
        self.assertEqual(snake("customerID"), "customer_id")
        self.assertEqual(snake("1st-col"), "c_1st_col")

if __name__ == "__main__":
    unittest.main()
