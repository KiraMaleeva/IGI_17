from django.core.files.storage import Storage
import cloudinary
import cloudinary.uploader
import cloudinary.api


class CloudinaryStorage(Storage):
    
    def _save(self, name, content):
        public_id = name.rsplit('.', 1)[0]
        
        # Загружаем файл
        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            folder='media',
            resource_type='auto',
            overwrite=True
        )
        
        return result['public_id']
    
    def exists(self, name):
        try:
            public_id = f"media/{name.rsplit('.', 1)[0]}"
            cloudinary.api.resource(public_id)
            return True
        except:
            return False
    
    def url(self, name):
        if not name:
            return ''
        
        if name.startswith('media/'):
            public_id = name
        else:
            public_id = f"media/{name.rsplit('.', 1)[0]}"
        
        # Генерируем URL
        return cloudinary.CloudinaryImage(public_id).build_url()
    
    def delete(self, name):
        try:
            public_id = f"media/{name.rsplit('.', 1)[0]}"
            cloudinary.uploader.destroy(public_id)
        except:
            pass
    
    def size(self, name):
        try:
            public_id = f"media/{name.rsplit('.', 1)[0]}"
            resource = cloudinary.api.resource(public_id)
            return resource.get('bytes', 0)
        except:
            return 0
    
    def get_available_name(self, name, max_length=None):
        return name