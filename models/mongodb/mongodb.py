from models.mongodb import DOCUMENT_COLLECTION
    
class Mongodb:
    def insert_document(documents, faiss_ids):
        try:
            for i in range(len(documents)):

                data = {
                    "faissID": faiss_ids[i],
                    "text": documents[i],
                }

                DOCUMENT_COLLECTION.insert_one(data)
            print(f"[{__name__}] {len(documents)}개의 문서 삽입 완료")
            return True
        except Exception as e:
            print(f"[{__name__}] 문서 삽입 실패: {e}")
            return False
    
    def find_documents_by_faiss_ids(faiss_ids):
        documents = []
        for faiss_id in faiss_ids:
            try:
                document = DOCUMENT_COLLECTION.find_one({"faissID": faiss_id}, {'_id': 0})
            except Exception as e:
                print(f"[{__name__}] 해당 문서를 찾을 수 없습니다: {e}")
                return False, f"{__name__}: {str(e)}"
            finally:
                if document is None:
                    print(f"[{__name__}] Faiss ID가 {faiss_id} 인것을 찾을 수 없습니다.")
                    continue
                documents.append(document['text'])
        return documents

        
