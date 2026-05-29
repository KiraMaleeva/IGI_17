"""
Кастомный Cloudinary storage backend
"""

from django.core.files.storage import Storage
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import cloudinary.api
from urllib.parse import urlparse


class CloudinaryStorage(Storage):
    
    def __init__(self):
        pass
    
    def _save(self, name, content):
        """
        Загружает файл на Cloudinary
        """
        # Загружаем файл
        result = cloudinary.uploader.upload(
            content,
            public_id=name.split('.')[0],
            folder='media',
            resource_type='auto'
        )
        
        return result['public_id']
    
    def exists(self, name):
        try:
            cloudinary.api.resource(name)
            return True
        except cloudinary.api.NotFound:
            return False
    
    def url(self, name):
        if not name:
            return ''
        
        # Генерируем URL
        return cloudinary.CloudinaryImage(name).build_url()
    
    def delete(self, name):
        try:
            cloudinary.uploader.destroy(name)
        except Exception:
            pass
    
    def size(self, name):
        try:
            resource = cloudinary.api.resource(name)
            return resource.get('bytes', 0)
        except Exception:
            return 0