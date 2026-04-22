from langchain_chroma import Chroma
from utils.config_handler  import chroma_conf
from model.factory import chat_model, embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from langchain_core.documents import Document
from utils.logger_handler import logger
import os

class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            persist_directory=chroma_conf["persist_directory"],
            embedding_function=embed_model,
            )  # You can specify your embedding function here
        
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function = len
        )
        
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
    
    def load_document(self):
        def check_md5_hex(md5_for_check: str) -> bool:
            # 这里可以实现你的MD5校验逻辑，返回True或False
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()  # 创建空文件
                return False
            
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                    
                return False
        
        def save_md5_hex(md5_for_check: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")
                
        def get_file_documents(read_path: str):
            # 这里可以实现你的文件读取逻辑，返回一个文档列表
            # 例如，你可以使用Python的文件操作来读取文本文件，并将其内容作为文档返回
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            
            return[]
        
        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]), 
            tuple(chroma_conf["allowed_knowledge_file_types"]))
        
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            
            if check_md5_hex(md5_hex):
                logger.info(f"File {path} has been processed before, skipping.")
                continue
            
            try:
                documents: list[Document] = get_file_documents(path)
                
                if not documents:
                    logger.warning(f"No documents found in file: {path}")
                    continue
                
                split_documents = self.spliter.split_documents(documents)
                
                if not split_documents:
                    logger.warning(f"No split documents generated from file: {path}")
                    continue
                
                self.vector_store.add_documents(split_documents)
                save_md5_hex(md5_hex)
                logger.info(f"File {path} processed and added to vector store successfully.")
            except Exception as e:
                logger.error(f"Error processing file {path}: {str(e)}", exc_info=True)
                continue
            
                
if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    # 这里可以继续使用retriever进行查
    # 询等操作
    res = retriever.invoke("如何查询机器人的保修期限？")
    
    for r in res:
        print(r.page_content)
        print("-"*20)