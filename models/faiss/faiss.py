import faiss
import os
import numpy as np

class Faiss:
    def __init__(self):
        self.index = None

    def get_index_path(self):
        base_path = os.getenv('FAISS_INDEX_PATH')
        return f"{base_path}/faiss.index"
    
    def initialize(self):
        index_path = self.get_index_path()

        if self.index is None:
            if os.path.exists(index_path):
                self.index = faiss.read_index(index_path)
                print(f"[{__name__}] 기존 Faiss 인덱스 로드 완료 | 총 벡터: {self.index.ntotal}")
            else:
                self.index = faiss.IndexFlatL2(1024)
                print(f"[{__name__}] 새로운 Faiss 인덱스 생성 완료")
        return self.index
    
    # 벡터 추가
    def instert(self, vectors) -> list:
        vectors = np.array(vectors).astype('float32')

        # Faiss 인덱스 벡터 추가
        # 로드된 (메모리에 저장된) 인덱스에 벡터 추가
        try:
            self.index.add(vectors)

            faiss_ids = list(range(self.index.ntotal - len(vectors), self.index.ntotal))
            print(f"[{__name__}] {len(vectors)}개의 벡터 추가 | 총 벡터: {self.index.ntotal}")
        except Exception as e:
            print(f"[{__name__}] 벡터 추가 중 오류 발생: {e}")
            return []

        # Faiss 인덱스 저장
        # 메모리에 존재하는 벡터가 추가된 인덱스를 파일로 저장
        try:
            faiss.write_index(self.index, self.get_index_path())
            print(f"[{__name__}] Faiss 인덱스 저장 완료 | 총 벡터: {self.index.ntotal}")

            # 변수 초기화
            self.index = self.initialize()
            
            return faiss_ids
        except Exception as e:
            print(f"[{__name__}] Faiss 인덱스 저장 중 오류 발생: {e}")
            return []
    
    # 벡터 유사도 검색
    def similaraty_search(self, query_vector, top_k=3, threshold=1.5) -> list:
        if self.index.ntotal == 0:
            print(f"[{__name__}] Faiss 인덱스가 비어 있습니다. 벡터를 추가해주세요.")
            return []
        
        if query_vector is None:
            print(f"[{__name__}] 질문 벡터를 받지 못했습니다.")
            return []
        
        query_vector = np.array(query_vector).reshape(1, -1).astype('float32')
        
        distances, indices = self.index.search(query_vector, min(top_k * 2, self.index.ntotal))
        
        filtered_results = [
            (dist, idx) for dist, idx in zip(distances[0], indices[0]) 
            if dist <= threshold and idx != -1
        ]
        filtered_results.sort(key=lambda x: x[0])
        top_results = filtered_results[:top_k]
        top_indices_ids = [int(idx) for _, idx in top_results]
        return top_indices_ids