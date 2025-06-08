import asyncio

# from models.mongodb.mg_pdf_model import MongodbPDF
# from models.faiss.process import FindTopSimilarVectors

from models.faiss import FAISS

from models.mongodb.mongodb import Mongodb

from utils.embedding import embedding_model
from utils.openai_gpt import ChatGPT

def rag_chain(question):

    # 질의를 임베딩 후 유사도 검색을 통해 관련 문서의 원문을 찾는다.
    def pipeline() -> str:
        query_vector = embedding_model([question])

        faiss_ids = FAISS.similaraty_search(query_vector)   # 벡터 ID 가 추출된다.

        if not faiss_ids:
            return "보다 정확한 정보를 위해 질문을 구체적으로 말씀해 주세요."
        
        find_docs = Mongodb.find_documents_by_faiss_ids(faiss_ids)

        formatted_prompt = str(f"사용자 질문: {question}\n참고자료: {find_docs}")
        return formatted_prompt

    # 최종적으로 ChatGPT 모델을 사용하여 답변을 생성한다.
    async def async_function():
        chat_gpt = ChatGPT()
        response = await chat_gpt.get_response(formatted_prompt)
        return response

    try:
        formatted_prompt = pipeline()
        response = asyncio.run(
            asyncio.wait_for(async_function(), timeout=30.0)
        )

    except asyncio.TimeoutError:
        print(f"[{__name__}] 요청 시간이 초과되었습니다. 30초 내에 응답을 받지 못했습니다.")
        response = "요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."

    except RuntimeError as e:
        if "Event loop is closed" in str(e):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(async_function())
            except Exception as inner_e:
                print(f"[{__name__}] 이벤트 루프 실행 중 오류가 발생했습니다: {str(inner_e)}")
                response = "이벤트 루프 실행 중 오류가 발생했습니다."
        else:
            print(f"[{__name__}] 실행 중 오류가 발생했습니다: {str(e)}")
            response = "실행 중 오류가 발생했습니다."

    except Exception as e:
        print(f"[{__name__}] 예상치 못한 오류가 발생했습니다: {str(e)}.")
        response = "예상치 못한 오류가 발생했습니다."

    return response