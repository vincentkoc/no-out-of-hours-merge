import unittest

from main import validate_custom_message, validate_restricted_times, validate_timezone


class TestMain(unittest.TestCase):
    def test_validate_timezone(self):
        with self.assertRaises(ValueError):
            validate_timezone("Invalid/Timezone")
        validate_timezone("Australia/Sydney")

    def test_validate_restricted_times(self):
        with self.assertRaises(ValueError):
            validate_restricted_times({"invalid_day": [(0, 7), (16.5, 24)]})
        with self.assertRaises(ValueError):
            validate_restricted_times({"mon": "invalid_value"})
        with self.assertRaises(ValueError):
            validate_restricted_times({"mon": [(0, "invalid"), (16.5, 24)]})
        with self.assertRaises(ValueError):
            validate_restricted_times({"mon": [(0, 7, 9), (16.5, 24)]})
        with self.assertRaises(ValueError):
            validate_restricted_times({"mon": [(0,)]})
        validate_restricted_times({"mon": [(0, 7), (16.5, 24)]})

    def test_validate_custom_message(self):
        with self.assertRaises(ValueError):
            validate_custom_message("   ")
        validate_custom_message(
            "⚠️ **PR merging is not allowed outside business hours.** ⚠️"
        )


if __name__ == "__main__":
    unittest.main()
