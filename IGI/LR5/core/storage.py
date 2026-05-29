from django.core.files.storage import Storage
from django.core.files.base import File
from django.conf import settings
import cloudinary
import cloudinary.uploader


class MediaCloudinaryStorage(Storage):
    
    def __init__(self):
        if hasattr(settings, 'CLOUDINARY_CONFIG'):
            cloudinary.config(**settings.CLOUDINARY_CONFIG)
    
    def _open(self, name, mode='rb'):
        raise NotImplementedError("Cloudinary storage doesn't support direct file opening")
    
    def _save(self, name, content):
        upload_result = cloudinary.uploader.upload(content)
        return upload_result['public_id']
    
    def url(self, name):
        return cloudinary.CloudinaryImage(name).build_url()
    
    def exists(self, name):
        return False
    
    def delete(self, name):
        try:
            cloudinary.uploader.destroy(name)
        except:
            pass