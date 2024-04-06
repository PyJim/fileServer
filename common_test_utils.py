import os
from django.conf import settings

class CommonTestUtils:
    uploaded_files = []

    @classmethod
    def create_test_file(cls):
        file_content = b"Hello, this is a test file content."
        file_name = "test.txt"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        
        # Write the file content to the filesystem with UTF-8 encoding
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        cls.uploaded_files.append(file_path)  # Store file path for cleanup
        return file_path  # Return file path for reference

    @classmethod
    def cleanup_uploaded_files(cls):
        for file_path in cls.uploaded_files:
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass  # File may have been already deleted or not exist
        cls.uploaded_files.clear()
