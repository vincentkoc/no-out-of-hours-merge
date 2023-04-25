import unittest
from unittest.mock import MagicMock, patch

import requests

from main import post_comment_on_pr


class TestPostCommentOnPR(unittest.TestCase):
    @patch("src.main.Github")
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "fake_owner/fake_repo"})
    def test_post_comment_on_pr(self, mock_github):
        # Disable SSL verification for testing purposes
        original_send = requests.Session.send

        def send_no_verify(self, request, **kwargs):
            kwargs["verify"] = False
            return original_send(self, request, **kwargs)

        requests.Session.send = send_no_verify

        # Set up mock objects
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_comment = MagicMock()
        mock_comments = [mock_comment]

        # Set up mock object attributes and return values
        mock_github.return_value.get_repo.return_value = mock_repo
        mock_repo.get_pull.return_value = mock_pr
        mock_pr.get_issue_comments.return_value = mock_comments
        mock_comment.body = "Existing comment text"

        # Call the function with the mock objects
        github_token = "fake_token"  # noqa: S105 # nosec
        pr_number = 42
        message = "New comment text"
        check_existing_comment = True

        post_comment_on_pr(github_token, pr_number, message, check_existing_comment)

        # Check that the create_issue_comment method was called with the correct message
        mock_pr.create_issue_comment.assert_called_with(message)

        # Revert back to the original 'send' method
        requests.Session.send = original_send


if __name__ == "__main__":
    unittest.main()
