import json
import tempfile
from io import StringIO
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase


class DescribeCommandTestCase(TestCase):
    """Tests for the describe management command."""

    def test_describe_outputs_to_stdout(self):
        """Test that describe command outputs JSON to stdout by default."""
        out = StringIO()
        call_command('describe', stdout=out)
        output = out.getvalue()

        # Verify output is not empty
        self.assertGreater(len(output), 0)

        # Verify output is valid JSON
        data = json.loads(output)
        self.assertIsInstance(data, dict)

    def test_describe_includes_settings(self):
        """Test that describe command includes Django settings."""
        out = StringIO()
        call_command('describe', stdout=out)
        output = out.getvalue()
        data = json.loads(output)

        # Verify settings are included
        self.assertIn('settings', data)
        self.assertIsInstance(data['settings'], dict)

        # Verify common Django settings are present
        self.assertIn('DEBUG', data['settings'])
        self.assertIn('INSTALLED_APPS', data['settings'])

    def test_describe_outputs_to_file(self):
        """Test that describe command can write output to a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            # Call command with --output option
            call_command('describe', output=temp_path)

            # Verify file was created
            self.assertTrue(Path(temp_path).exists())

            # Read and verify content
            with open(temp_path, 'r') as f:
                content = f.read()

            # Verify content is valid JSON
            data = json.loads(content)
            self.assertIsInstance(data, dict)

            # Verify settings are included
            self.assertIn('settings', data)

        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_describe_file_output_is_valid_json(self):
        """Test that file output contains valid, parseable JSON."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            # Call command with output option
            call_command('describe', output=temp_path)

            # Verify file was created and contains valid JSON
            self.assertTrue(Path(temp_path).exists())

            with open(temp_path, 'r') as f:
                data = json.loads(f.read())

            self.assertIsInstance(data, dict)
            self.assertIn('settings', data)

        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)

    def test_describe_output_is_formatted(self):
        """Test that JSON output is properly formatted with indentation."""
        out = StringIO()
        call_command('describe', stdout=out)
        output = out.getvalue()

        # Verify output has indentation (not minified)
        self.assertIn('\n', output)
        self.assertIn('    ', output)

        # Verify it's still valid JSON
        data = json.loads(output)
        self.assertIsInstance(data, dict)

    def test_describe_file_content_matches_stdout(self):
        """Test that file output matches stdout output."""
        # Get stdout output
        stdout_out = StringIO()
        call_command('describe', stdout=stdout_out)
        stdout_data = json.loads(stdout_out.getvalue())

        # Get file output
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name

        try:
            call_command('describe', output=temp_path)

            with open(temp_path, 'r') as f:
                file_data = json.loads(f.read())

            # Compare the data structures
            self.assertEqual(stdout_data, file_data)

        finally:
            Path(temp_path).unlink(missing_ok=True)
