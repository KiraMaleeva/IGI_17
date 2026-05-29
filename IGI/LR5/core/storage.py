from django.core.files.storage import Storage
from django.core.files.base import File
import cloudinary
import cloudinary.uploader


class MediaCloudinaryStorage(Storage):
    
    def _open(self, name, mode='rb'):
        return File(open(name, mode))
    
    def _save(self, name, content):
        response = cloudinary.uploader.upload(content)
        return response['public_id']
    
    def url(self, name):
        return cloudinary.CloudinaryImage(name).build_url()
    
    def exists(self, name):
        return False
    
    def delete(self, name):
        try:
            cloudinary.uploader.destroy(name)
        except:
            pass