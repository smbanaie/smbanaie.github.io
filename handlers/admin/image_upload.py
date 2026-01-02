#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import uuid
import datetime
from urllib.parse import quote_plus
from handlers.index_handler import TornadoRequestBase
from user_area.smbanaie.smbanaie.userconf import USER_DIR
from utils.logger_setup import logger


class image_upload_Handler(TornadoRequestBase):
    """Handler for image upload operations."""

    def initialize(self):
        """Initialize handler with image directories."""
        self.temp_dir = pathlib.Path(USER_DIR) / 'images' / 'temp'
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Allowed image file extensions
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        # Maximum file size (5MB)
        self.max_file_size = 5 * 1024 * 1024

    def post(self, *args, **kwargs):
        """Handle image upload requests."""
        action = self.get_argument('action', 'upload')
        
        if action == 'upload':
            return self.upload_image()
        elif action == 'delete':
            return self.delete_temp_image()
        elif action == 'cleanup':
            return self.cleanup_temp_images()
        else:
            self.write({"error": "Invalid action"})
            self.set_status(400)

    def upload_image(self):
        """Upload a single image to the temporary directory."""
        try:
            # Check if file was uploaded
            if 'image' not in self.request.files:
                self.write({"error": "No image file uploaded"})
                self.set_status(400)
                return

            file_info = self.request.files['image'][0]
            filename = file_info['filename']
            content_type = file_info['content_type']
            body = file_info['body']

            # Validate file size
            if len(body) > self.max_file_size:
                self.write({"error": "File size exceeds maximum limit (5MB)"})
                self.set_status(400)
                return

            # Validate file extension
            file_ext = pathlib.Path(filename).suffix.lower()
            if file_ext not in self.allowed_extensions:
                self.write({"error": "Invalid file format. Only JPG, PNG, GIF, and WebP are allowed"})
                self.set_status(400)
                return

            # Validate content type
            if not content_type.startswith('image/'):
                self.write({"error": "Invalid file type"})
                self.set_status(400)
                return

            # Generate secure filename
            safe_filename = self._generate_safe_filename(filename, file_ext)
            temp_path = self.temp_dir / safe_filename

            # Save the file
            with open(temp_path, 'wb') as f:
                f.write(body)

            # Return file info
            file_info = {
                'filename': safe_filename,
                'original_name': filename,
                'size': len(body),
                'url': f"/admin/temp-image/{quote_plus(safe_filename)}",
                'path': str(temp_path)
            }

            self.write({"success": True, "file": file_info})
            logger.info(f"Image uploaded successfully: {safe_filename}")

        except Exception as e:
            logger.error(f"Error uploading image: {e}")
            self.write({"error": f"Upload failed: {str(e)}"})
            self.set_status(500)

    def delete_temp_image(self):
        """Delete a temporary image file."""
        filename = self.get_argument('filename', '')
        
        if not filename:
            self.write({"error": "No filename specified"})
            self.set_status(400)
            return

        # Security check - ensure filename is safe
        if not self._is_safe_filename(filename):
            self.write({"error": "Invalid filename"})
            self.set_status(400)
            return

        temp_path = self.temp_dir / filename
        
        if not temp_path.exists():
            self.write({"error": "File not found"})
            self.set_status(404)
            return

        try:
            temp_path.unlink()
            self.write({"success": True, "message": "File deleted successfully"})
            logger.info(f"Temporary image deleted: {filename}")
        except Exception as e:
            logger.error(f"Error deleting temporary image: {e}")
            self.write({"error": f"Delete failed: {str(e)}"})
            self.set_status(500)

    def cleanup_temp_images(self):
        """Clean up old temporary images (older than 24 hours)."""
        try:
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=24)
            deleted_count = 0
            
            for temp_file in self.temp_dir.iterdir():
                if temp_file.is_file():
                    file_mtime = datetime.datetime.fromtimestamp(temp_file.stat().st_mtime)
                    if file_mtime < cutoff_time:
                        temp_file.unlink()
                        deleted_count += 1
            
            self.write({"success": True, "deleted_count": deleted_count})
            logger.info(f"Cleaned up {deleted_count} old temporary images")
            
        except Exception as e:
            logger.error(f"Error cleaning up temporary images: {e}")
            self.write({"error": f"Cleanup failed: {str(e)}"})
            self.set_status(500)

    def _generate_safe_filename(self, original_filename, extension):
        """Generate a secure filename using UUID."""
        # Remove any path components from original filename
        safe_name = pathlib.Path(original_filename).name
        
        # Generate UUID-based filename
        unique_id = str(uuid.uuid4())
        safe_filename = f"{unique_id}{extension}"
        
        return safe_filename

    def _is_safe_filename(self, filename):
        """Check if filename is safe (contains only allowed characters)."""
        # Only allow alphanumeric characters, hyphens, underscores, and dots
        import re
        pattern = r'^[a-zA-Z0-9\-_.]+$'
        return bool(re.match(pattern, filename))


class temp_image_Handler(TornadoRequestBase):
    """Handler for serving temporary images."""

    def initialize(self):
        """Initialize handler with temp directory."""
        self.temp_dir = pathlib.Path(USER_DIR) / 'images' / 'temp'

    def get(self, filename):
        """Serve a temporary image file."""
        # Security check - ensure filename is safe
        if not self._is_safe_filename(filename):
            self.set_status(400)
            self.write("Invalid filename")
            return

        temp_path = self.temp_dir / filename
        
        if not temp_path.exists():
            self.set_status(404)
            self.write("File not found")
            return

        try:
            # Serve the file
            with open(temp_path, 'rb') as f:
                content = f.read()
            
            # Set appropriate content type
            file_ext = pathlib.Path(filename).suffix.lower()
            content_type = self._get_content_type(file_ext)
            
            self.set_header("Content-Type", content_type)
            self.set_header("Content-Length", str(len(content)))
            self.write(content)
            
        except Exception as e:
            logger.error(f"Error serving temporary image {filename}: {e}")
            self.set_status(500)
            self.write("Error serving file")

    def _is_safe_filename(self, filename):
        """Check if filename is safe (contains only allowed characters)."""
        import re
        pattern = r'^[a-zA-Z0-9\-_.]+$'
        return bool(re.match(pattern, filename))

    def _get_content_type(self, extension):
        """Get content type based on file extension."""
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return content_types.get(extension, 'application/octet-stream')