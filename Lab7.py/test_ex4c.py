import io
import unittest
from contextlib import redirect_stdout

from Ex4c import check_purchases


class CheckPurchasesTests(unittest.TestCase):
    def test_budget_exceeded_stops_at_over_limit(self):
        purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
        budget = 50
        output = io.StringIO()

        with redirect_stdout(output):
            result = check_purchases(purchases, budget)

        self.assertEqual(
            result,
            ["This 36.13 is within budget.", "This 23.87 is over budget!"],
        )
        self.assertEqual(
            output.getvalue().strip().splitlines(),
            ["This 36.13 is within budget.", "This 23.87 is over budget!"],
        )

    def test_all_purchases_are_within_budget(self):
        purchases = [10, 20, 30]
        budget = 100
        output = io.StringIO()

        with redirect_stdout(output):
            result = check_purchases(purchases, budget)

        self.assertEqual(
            result,
            [
                "This 10 is within budget.",
                "This 20 is within budget.",
                "This 30 is within budget.",
            ],
        )
        self.assertEqual(
            output.getvalue().strip().splitlines(),
            [
                "This 10 is within budget.",
                "This 20 is within budget.",
                "This 30 is within budget.",
            ],
        )

    def test_empty_list_has_no_output(self):
        output = io.StringIO()

        with redirect_stdout(output):
            result = check_purchases([], 50)

        self.assertEqual(result, [])
        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
