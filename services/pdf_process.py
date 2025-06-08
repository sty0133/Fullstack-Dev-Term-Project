import os

from models.faiss import FAISS

from utils.google_cld_vision import detect_text_pdf_path
from utils.embedding import load_and_retrieve_docs_sliding_window

from models.mongodb.mongodb import Mongodb

def pdf_process(file_paths):

    # PDF 파일 OCR 처리 -> 리스트 반환
    texts = detect_text_pdf_path(file_paths)
    
    # OCR 처리된 텍스트 임베딩 -> 리스트 반환
    embedded_vectors, documents = load_and_retrieve_docs_sliding_window(texts)

    # FAISS 인덱스 초기화 및 벡터 저장 -> 리스트 반환
    faiss_ids = FAISS.instert(embedded_vectors)
    if faiss_ids :

        # MongoDB에 문서 저장
        result = Mongodb.insert_document(documents, faiss_ids)

        if result:
            
            # 사용된 PDF 파일 로컬에서 삭제
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"[{__name__}] 파일 삭제 실패: {file_path} - {e}")
            return True
        
    return False