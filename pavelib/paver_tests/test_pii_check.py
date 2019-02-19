"""
Tests for Paver's PII checker task.
"""
import unittest

import six
from mock import patch
from paver.easy import call_task

import pavelib.quality


class TestPaverPiiCheck(unittest.TestCase):
    """
    For testing run_pii_check
    """

    def setUp(self):
        """
        Set-up for the PII check tests.
        """
        super(TestPaverPiiCheck, self).setUp()

        # Mock the paver @needs decorator
        self._mock_paver_needs = patch.object(pavelib.quality.run_pii_check, 'needs').start()
        self._mock_paver_needs.return_value = 0

        # Cleanup mocks
        self.addCleanup(self._mock_paver_needs.stop)

    @patch('pavelib.quality.sh')
    def test_pii_check_report_dir_override(self, mock_paver_sh):
        """
        run_pii_check succeeds with proper report dir
        """
        call_task('pavelib.quality.run_pii_check', options={"report_dir": "test_report_dir/"})
        mock_calls = [six.text_type(call) for call in mock_paver_sh.mock_calls]
        assert len(mock_calls) == 2
        assert any(['lms.envs.test' in call for call in mock_calls])
        assert any(['cms.envs.test' in call for call in mock_calls])
        assert all(['test_report_dir/' in call for call in mock_calls])
