import csv
import io
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


class CSVUploadView(APIView):
    """API view for handling CSV file uploads.

    This view processes CSV files containing user data and validates
    each record before saving to the database. It handles various
    validation scenarios including file format, required fields,
    and data integrity.
    """

    def post(self, request):
        """Handle POST requests for CSV file uploads.

        Args:
            request: The HTTP request object containing the CSV file.

        Returns:
            Response: A JSON response containing the number of successful
                     and rejected records, along with any error messages.
        """
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']

        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'File must have .csv extension'},
                status=status.HTTP_400_BAD_REQUEST
            )

        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))

        successful_records = 0
        rejected_records = 0
        errors = []

        for row_number, row in enumerate(csv_reader, start=2):
            if not all(field in row for field in ['name', 'email', 'age']):
                errors.append({
                    'row': row_number,
                    'errors': 'Missing required fields (name, email, age)'
                })
                rejected_records += 1
                continue

            try:
                row['age'] = int(row['age'])
            except ValueError:
                errors.append({
                    'row': row_number,
                    'errors': 'Age must be a valid integer'
                })
                rejected_records += 1
                continue

            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                try:
                    serializer.save()
                    successful_records += 1
                except IntegrityError:
                    errors.append({
                        'row': row_number,
                        'errors': 'Email already exists'
                    })
                    rejected_records += 1
            else:
                errors.append({
                    'row': row_number,
                    'errors': serializer.errors
                })
                rejected_records += 1

        return Response({
            'successful_records': successful_records,
            'rejected_records': rejected_records,
            'errors': errors
        })
