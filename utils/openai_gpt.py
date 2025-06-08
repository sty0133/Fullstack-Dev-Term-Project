from openai import AsyncOpenAI
from openai import APIError, RateLimitError, APIConnectionError
import os

class ChatGPT:
    def __init__(self):
        # OpenAI API 키 환경변수에서 가져오기
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"

    async def get_response(self, content: str) -> str:
        system_prompt = """
            당신은 업로드된 PDF 문서를 기반으로 사용자 질문에 정확하게 응답하는 PDF 봇 어시스턴트입니다. 사용자의 질문에 대해 관련 문서 내용을 바탕으로 대답하세요. 문서에 포함되지 않은 정보는 절대 임의로 추측하거나 생성하지 말고, “해당 문서에서 관련 정보를 찾을 수 없습니다”라고 답변하세요.

            응답은 아래 기준을 따릅니다:

            1. 가능한 한 간결하고 명확하게 답변합니다.
            2. 응답에는 관련 문서의 문맥이나 문장을 자연스럽게 포함시킵니다.
            3. 정보가 모호하거나 없을 경우, 거짓 정보를 생성하지 않고 정직하게 부족함을 알립니다.
            4. 질문이 명확하지 않거나 문서의 내용과 관련 없는 경우에는 정중히 안내합니다.
            5. 모든 응답은 한국어로 합니다.

            이 시스템은 법적·의학적·재무적 조언을 제공하지 않으며, 문서 내용만을 기반으로 정보적 응답을 제공합니다.
        """
            
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": content
            }
        ]
        
        try:
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=4096 # gpt-3.5-turbo 모델 최대 토큰 4096
            )

            return response.choices[0].message.content

        except RateLimitError:
            print(f"[{__name__}] OpenAI API 요청이 너무 많습니다. 잠시 후 다시 시도해주세요.")
            return "현재 요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
        except APIConnectionError:
            print(f"[{__name__}] OpenAI 서버와의 연결에 실패했습니다. 인터넷 연결을 확인해주세요.")
            return "서버와의 연결에 실패했습니다. 인터넷 연결을 확인해주세요."
        except APIError as e:
            print(f"[{__name__}] OpenAI API 오류가 발생했습니다: {str(e)}")
            return "API 오류가 발생했습니다."
        except Exception as e:
            print(f"[{__name__}] 예상치 못한 오류가 발생했습니다: {str(e)}")
            return "예상치 못한 오류가 발생했습니다."