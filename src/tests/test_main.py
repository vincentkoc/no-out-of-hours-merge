import datetime
import unittest

from main import (  # isort:skip
    is_holiday,
    is_restricted_time,
    validate_custom_message,
    validate_restricted_times,
    validate_timezone,
)

import pytz  # isort:skip
from freezegun import freeze_time  # isort:skip


class TestMain(unittest.TestCase):
    def test_validate_timezone(self):
        valid_timezone = "Australia/Sydney"
        invalid_timezone = "Invalid/Timezone"
        self.assertIsNone(
            validate_timezone(valid_timezone), "Valid timezone should pass validation."
        )
        with self.assertRaises(
            ValueError, msg="Invalid timezone should raise ValueError."
        ):
            validate_timezone(invalid_timezone)

    def test_validate_custom_message(self):
        valid_message = "This is a valid message."
        invalid_message = "    "
        self.assertIsNone(
            validate_custom_message(valid_message),
            "Valid custom message should pass validation.",
        )
        with self.assertRaises(
            ValueError, msg="Invalid custom message should raise ValueError."
        ):
            validate_custom_message(invalid_message)

    def test_validate_restricted_times(self):
        valid_restricted_times = {
            "weekly": [
                {
                    "days": ["mon", "tue", "wed", "thu", "fri"],
                    "intervals": [(0, 7), (16.5, 24)],
                }
            ],
            "dates": [{"date": "2023-12-25", "intervals": [(0, 24)]}],
            "holidays": {"country": "US", "state": "CA", "intervals": [(0, 24)]},
        }
        invalid_restricted_times = {
            "weekly": [
                {
                    "days": ["invalid", "tue", "wed", "thu", "fri"],
                    "intervals": [(0, 7), (16.5, 24)],
                }
            ]
        }
        self.assertIsNone(
            validate_restricted_times(valid_restricted_times),
            "Valid restricted times should pass validation.",
        )
        with self.assertRaises(
            ValueError, msg="Invalid restricted times should raise ValueError."
        ):
            validate_restricted_times(invalid_restricted_times)

    def test_is_holiday(self):
        fixed_datetime = datetime.datetime(
            2023, 1, 1, tzinfo=pytz.UTC
        )  # New Year's Day
        holidays_config = {"country": "US", "state": "CA"}
        self.assertTrue(
            is_holiday(fixed_datetime, holidays_config),
            "New Year's Day should be recognized as a holiday.",
        )

        fixed_datetime = datetime.datetime(
            2023, 2, 2, tzinfo=pytz.UTC
        )  # New Year's Day
        self.assertFalse(
            is_holiday(fixed_datetime, holidays_config),
            "February 2nd should not be recognized as a holiday.",
        )

    def test_is_restricted_time(self):
        restricted_times = {
            "weekly": [
                {
                    "days": ["mon", "tue", "wed", "thu", "fri"],
                    "intervals": [(0, 7), (16.5, 24)],
                },
                {"days": ["sat", "sun"], "intervals": [(0, 24)]},
            ],
            "dates": [],
            "holidays": {"country": "US", "state": "CA", "intervals": [(0, 24)]},
        }
        timezone = "Australia/Sydney"

        # Test with a time outside the restricted hours
        fixed_datetime = datetime.datetime(2023, 1, 3, 12, 0)  # Tuesday, 12:00 PM

        with freeze_time(fixed_datetime):
            result = is_restricted_time(timezone, restricted_times, now=fixed_datetime)
            self.assertFalse(result, "This time should not be restricted.")

        # Test with a time inside the restricted hours
        fixed_datetime = datetime.datetime(2023, 1, 3, 6, 0)  # Tuesday, 6:00 AM
        with freeze_time(fixed_datetime):
            result = is_restricted_time(timezone, restricted_times, now=fixed_datetime)
            self.assertTrue(result, "This time should be restricted.")


if __name__ == "__main__":
    unittest.main()
