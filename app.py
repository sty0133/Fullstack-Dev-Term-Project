import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

def create_app():
    from services.pdf_rag import rag_chain
    from services.pdf_process import pdf_process

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads/pdf')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers="*")

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    # 채팅 질문 처리
    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.get_json()
        question = data.get('question', '')
        if not question:
            return jsonify({'success': False, 'message': '질문이 비어 있습니다.'}), 400

        response = rag_chain(question)
        return jsonify({'success': True, 'response': response})

    # PDF 업로드 처리
    @app.route('/upload_pdf', methods=['POST'])
    def upload_pdf():
        if 'files' not in request.files:
            return jsonify({"success": False, "message": "파일이 포함되어 있지 않습니다."}), 400

        files = request.files.getlist('files')
        file_paths = []

        for file in files:
            if file.filename == '':
                continue
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({"success": False, "message": f"{file.filename}은 PDF 파일이 아닙니다."}), 400

            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)
            file_paths.append(save_path)

        if not file_paths:
            return jsonify({"success": False, "message": "업로드된 PDF 파일이 없습니다."}), 400

        result = pdf_process(file_paths)
        if result:
            return jsonify({"success": True, "message": "PDF 처리 및 저장이 완료되었습니다."})
        else:
            return jsonify({"success": False, "message": "PDF 처리 중 오류가 발생했습니다."}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)