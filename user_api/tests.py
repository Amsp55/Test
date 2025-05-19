import io
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class CSVUploadTests(TestCase):
    """Test cases for CSV file upload functionality.

    This test suite covers various scenarios including valid uploads,
    invalid data handling, file format validation, and duplicate
    email detection.
    """

    def setUp(self):
        """Set up test client and URL for all test methods."""
        self.client = APIClient()
        self.url = reverse('upload-csv')

    def test_upload_valid_csv(self):
        """Test successful upload of a valid CSV file."""
        csv_content = (
            "name,email,age\n"
            "John Doe,john@example.com,30\n"
            "Jane Smith,jane@example.com,25"
        )
        csv_file = io.StringIO(csv_content)
        csv_file.name = 'test.csv'

        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['successful_records'], 2)
        self.assertEqual(response.data['rejected_records'], 0)
        self.assertEqual(User.objects.count(), 2)

    def test_upload_invalid_csv(self):
        """Test handling of CSV file with invalid data."""
        csv_content = (
            "name,email,age\n"
            "John Doe,invalid-email,200\n"
            ",jane@example.com,25"
        )
        csv_file = io.StringIO(csv_content)
        csv_file.name = 'test.csv'

        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['successful_records'], 0)
        self.assertEqual(response.data['rejected_records'], 2)
        self.assertEqual(User.objects.count(), 0)

    def test_upload_non_csv_file(self):
        """Test rejection of non-CSV file uploads."""
        file_content = "This is not a CSV file"
        file = io.StringIO(file_content)
        file.name = 'test.txt'

        response = self.client.post(
            self.url,
            {'file': file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        """Test handling of duplicate email addresses."""
        User.objects.create(
            name="Existing User",
            email="existing@example.com",
            age=40
        )

        csv_content = (
            "name,email,age\n"
            "Duplicate User,existing@example.com,35"
        )
        csv_file = io.StringIO(csv_content)
        csv_file.name = 'test.csv'

        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['successful_records'], 0)
        self.assertEqual(response.data['rejected_records'], 1)
        self.assertEqual(User.objects.count(), 1)
