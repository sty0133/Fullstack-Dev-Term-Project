from google.cloud import vision
import os
from google.cloud import storage
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
BUKET_NAME = os.getenv('BUCKET_NAME')
        
def detect_text_pdf_path(pdf_paths: list):
    client = vision.ImageAnnotatorClient()
    storage_client = storage.Client()
    
    try:
        bucket = storage_client.get_bucket(BUKET_NAME)
    except Exception:
        bucket = storage_client.create_bucket(BUKET_NAME)
    
    all_texts = []  # 모든 PDF의 텍스트를 저장할 리스트
    
    # 각 PDF 파일 처리
    for pdf_path in pdf_paths:
        if not isinstance(pdf_path, (str, bytes, os.PathLike)):
            print(f"[{__name__}] 잘못된 파일 경로 형식: {pdf_path}")
            continue
            
        file_name = os.path.basename(pdf_path)
        # print(f"처리 중인 파일: {file_name}")
        
        source_blob_name = f"temp_pdf/{file_name}"
        output_prefix = f"temp_pdf/output_{file_name}"
        
        try:
            # 로컬 PDF를 GCS에 업로드
            blob = bucket.blob(source_blob_name)
            blob.upload_from_filename(pdf_path)
            
            # GCS URI 생성
            gcs_source_uri = f"gs://{BUKET_NAME}/{source_blob_name}"
            gcs_destination_uri = f"gs://{BUKET_NAME}/{output_prefix}/"
            
            # OCR 설정
            feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
            gcs_source = vision.GcsSource(uri=gcs_source_uri)
            input_config = vision.InputConfig(
                gcs_source=gcs_source, 
                mime_type="application/pdf"
            )
            gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
            output_config = vision.OutputConfig(
                gcs_destination=gcs_destination, 
                batch_size=2
            )
            
            # OCR 요청 실행
            async_request = vision.AsyncAnnotateFileRequest(
                features=[feature],
                input_config=input_config,
                output_config=output_config
            )
            
            operation = client.async_batch_annotate_files(requests=[async_request])
            # print(f"OCR 처리 중: {file_name}")
            operation.result(timeout=420)
            
            # 결과 파일 가져오기
            blobs = list(bucket.list_blobs(prefix=output_prefix))
            
            for result_blob in blobs:
                if result_blob.name.endswith(".json"):
                    json_string = result_blob.download_as_bytes().decode("utf-8")
                    response = json.loads(json_string)
                    
                    for page_response in response.get("responses", []):
                        if "fullTextAnnotation" in page_response:
                            text = page_response["fullTextAnnotation"]["text"]
                            all_texts.append(text)
            
        except Exception as e:
            print(f"[{__name__}] 파일 처리 중 오류 발생 ({file_name}): {str(e)}")
        
        finally:
            # 임시 파일 정리
            try:
                bucket.blob(source_blob_name).delete()
                for blob in bucket.list_blobs(prefix=output_prefix):
                    blob.delete()
            except Exception as e:
                print(f"[{__name__}] 임시 파일 삭제 중 오류: {str(e)}")
    
    # 모든 텍스트를 하나의 문자열로 합쳐서 반환 (\n과 \n\n로 구분)
    all_texts = [text.replace("\n", " ") for text in all_texts]
    all_texts = [text.replace("\n\n", "\n") for text in all_texts]
    return all_texts[0]