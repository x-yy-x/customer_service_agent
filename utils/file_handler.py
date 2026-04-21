import os, hashlib
from logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath:str):
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return None
    
    if not os.path.isfile(filepath):
        logger.error(f"Not a file: {filepath}")
        return None
    
    md5_obj = hashlib.md5()
    
    chunk_size = 8192
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
                
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"error calculating MD5 for {filepath}: {str(e)}")
        return None

    return md5_obj.hexdigest()

def listdir_with_allowed_type(path:str, allowed_types: tuple[str]): #返回文件夹内文件列表（允许的后缀）
    files = []
    
    if not os.path.isdir(path):
        logger.error(f"listdir_with_allowed_type: Not a directory: {path}")
        return allowed_types
    
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)

def pdf_loader(filepath:str, password:str = None) -> list[Document]:
    return PyPDFLoader(filepath, password=password).load()

def txt_loader(filepath:str) -> list[Document]:
    return TextLoader(filepath).load()
    