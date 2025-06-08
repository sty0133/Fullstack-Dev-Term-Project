# 📘 Fullstack-Dev-Term-Project

이 프로젝트는 웹 기반으로 PDF 파일을 업로드하고, Google Cloud Vision API로 OCR 처리를 한 뒤 HuggingFace 임베딩 모델(`nlpai-lab/KURE-v1`)을 이용하여 텍스트를 벡터화하고 MongoDB 및 FAISS에 저장합니다. 이후 업로드된 PDF 파일의 정보를 기반으로 질의응답이 가능한 RAG(Retrieval-Augmented Generation) 시스템을 제공합니다.

---

## ✅ 환경 및 실행 정보

- **Python 버전**: 3.11.10
- **의존성 설치**: `requirements.txt` 파일 사용
- **실행 프레임워크**: Flask
- **데이터 저장소**:
  - MongoDB (문서/메타 정보 저장)
  - FAISS (벡터 검색)
- **OCR**: Google Cloud Vision API 사용
- **임베딩 모델**: HuggingFace `nlpai-lab/KURE-v1` (첫 실행 시 자동 다운로드)
- **챗 응답 모델**: OpenAI GPT API

---

## 📦 프로젝트 구조

```
Fullstack-Dev-Term-Project/
├── app.py                        # Flask 앱의 메인 엔트리포인트
├── faiss.index                   # FAISS 벡터 인덱스 파일
├── README.md                     # 프로젝트 설명 파일
├── requirements.txt              # Python 패키지 의존성 목록
│
├── models/                       # 데이터/벡터/DB 모델 관련 폴더
│   ├── faiss/                    # FAISS 벡터 검색 관련 코드
│   │   ├── __init__.py
│   │   └── faiss.py
│   └── mongodb/                  # MongoDB 관련 코드
│       ├── __init__.py
│       └── mongodb.py
│
├── services/                     # 비즈니스 로직(서비스 계층)
│   ├── pdf_process.py            # PDF 업로드/임베딩/DB저장 처리
│   └── pdf_rag.py                # RAG(질의응답) 체인 처리
│
├── static/                       # 정적 파일(css, js 등)
│   └── css/
│       └── chat.css              # 채팅 UI 스타일
│
├── templates/                    # HTML 템플릿(Jinja2)
│   └── index.html                # 메인 채팅/업로드 페이지
│
├── uploads/                      # 업로드된 PDF 파일 임시 저장 폴더
│
└── utils/                        # 유틸리티 함수/클래스
    ├── embedding.py              # 임베딩 모델 및 텍스트 분할 함수
    ├── google_cld_vision.py      # 구글 OCR 연동 함수
    └── openai_gpt.py             # OpenAI GPT API 연동 함수
```

---

## ⚙️ 실행 방법

### 1. Python 가상환경 생성 및 패키지 설치

```bash
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. .env 파일 설정

`.env` 파일에 아래와 같은 환경변수만 설정하면 됩니다.

```
MONGODB_URI=your_mongodb_uri
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_flask_secret_key
GOOGLE_APPLICATION_CREDENTIALS=your_google_cld_credentials_path
BUCKET_NAME=your_google_cld_bucket_name
```

- `MONGODB_URI`: MongoDB 접속 URI
- `OPENAI_API_KEY`: OpenAI API 키 (챗봇 응답에 필요)
- `SECRET_KEY`: Flask 세션용 시크릿 키
- `GOOGLE_APPLICATION_CREDENTIALS`: Google Cloud 프로젝트 증명서
- `BUCKET_NAME`: Google Cloud 버킷 이름

### 3. Google Cloud 프로젝트 및 버킷 생성

- Google Cloud Console에서 **프로젝트를 생성**하고 **Vision API**를 활성화하세요.
- **Cloud Storage 버킷**을 생성하여 PDF 파일을 저장할 수 있습니다(필요시).
- 서비스 계정 키(JSON)를 생성해 `.env` 파일에 설정합니다.

### 4. MongoDB 실행

- 로컬 또는 Atlas MongoDB 인스턴스를 실행합니다.
- 연결 문자열은 `.env` 파일에 설정합니다.

### 5. FAISS 인덱스 초기화

- PDF 업로드 및 처리 후 자동 생성되며,
- 새로운 정보를 담고 싶은 경우 기존 `faiss.index` 파일 삭제 후 재생성 가능합니다.

### 6. Flask 앱 실행

```bash
python app.py
```

* 기본 접속 주소: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✅ 주요 기능 요약

* 📄 PDF 업로드 및 OCR 처리 (Google Vision API)
* ✂️ 텍스트 분할 및 벡터화 (HuggingFace KURE-v1)
* 🔍 FAISS 기반 유사 문서 검색
* 🧾 MongoDB에 문서 메타/내용 저장
* 💬 웹 기반 RAG 질의응답 UI
* 💾 LocalStorage 기반 채팅 세션 저장

---

## 📝 사전 준비 체크리스트

* [ ] Python 3.11.10 설치 및 가상환경 설정
* [ ] `requirements.txt` 패키지 설치 완료
* [ ] `.env` 파일에 환경변수 설정 완료
* [ ] Google Cloud Vision API 키 파일 존재 (`gcp_credentials.json`)
* [ ] Google Cloud 프로젝트 및 버킷 생성
* [ ] MongoDB 실행 중이며 접속 정보 설정
* [ ] OpenAI API 키 준비

---

## 📬 문의

본 프로젝트는 풀스택 개발 강의의 Term Project 과제 제출을 위해 제작되었습니다.