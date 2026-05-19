import zipfile
import os
from datetime import datetime

class FileHandler:
    """Handle file operations including zip archiving"""
    
    @staticmethod
    def read_file(filename: str) -> str:
        """Read text from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    
    @staticmethod
    def save_results(filename: str, results: str) -> None:
        """Save analysis results to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(results)
    
    @staticmethod
    def create_zip(source_file: str, zip_name: str) -> dict:
        """
        Create zip archive and return file info
        """
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(source_file, os.path.basename(source_file))
            
            # Get file info
            info = zipf.getinfo(os.path.basename(source_file))
            
            return {
                'filename': zip_name,
                'file_size': os.path.getsize(zip_name),
                'compressed_size': info.compress_size,
                'compression_ratio': round((1 - info.compress_size / info.file_size) * 100, 2) if info.file_size > 0 else 0,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }