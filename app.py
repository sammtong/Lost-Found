import os
import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# 사진 저장 경로 설정
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 임시 데이터베이스
users = {}
lost_items = []
found_items = []
queries = []

# --- 인증 API ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if data.get('user_id') in users:
        return jsonify({"message": "ID 중복"}), 400
    users[data.get('user_id')] = data.get('password')
    return jsonify({"message": "가입 성공"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if users.get(data.get('user_id')) == data.get('password'):
        return jsonify({"message": "성공"}), 200
    return jsonify({"message": "실패"}), 401

# --- 분실물 관리 ---
@app.route('/api/lost', methods=['GET', 'POST'])
def lost_manage():
    if request.method == 'GET':
        keyword = request.args.get('q', '').lower()
        results = []
        for idx, item in enumerate(lost_items):
            if not item: continue
            # 제목(title) 대신 물품명(item_name)으로 검색
            if not keyword or (keyword in item.get('item_name', '').lower()):
                item_with_id = item.copy()
                item_with_id['id'] = idx
                results.append(item_with_id)
        return jsonify(results), 200

    if request.method == 'POST':
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                new_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                image_filename = new_filename
        
        # [수정] title 입력이 없으므로 item_name을 title로 사용
        item_name = request.form.get('item_name')
        
        new_item = {
            'title': item_name,  # 제목 대신 물품명 사용
            'item_name': item_name,
            'date': request.form.get('date'),
            'place': request.form.get('place'),
            'phone': request.form.get('phone'),
            'content': request.form.get('content'),
            'author': request.form.get('author'),
            'image': image_filename,
            'is_solved': False
        }
        lost_items.append(new_item)
        return jsonify({"message": "등록 성공"}), 200

# --- 습득물 관리 ---
@app.route('/api/found', methods=['GET', 'POST'])
def found_manage():
    if request.method == 'GET':
        keyword = request.args.get('q', '').lower()
        results = []
        for idx, item in enumerate(found_items):
            if not item: continue
            if not keyword or (keyword in item.get('item_name', '').lower()):
                item_with_id = item.copy()
                item_with_id['id'] = idx
                results.append(item_with_id)
        return jsonify(results), 200

    if request.method == 'POST':
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                new_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                image_filename = new_filename

        # [수정] title 입력이 없으므로 item_name을 title로 사용
        item_name = request.form.get('item_name')

        new_item = {
            'title': item_name, # 제목 대신 물품명 사용
            'item_name': item_name,
            'date': request.form.get('date'),
            'place': request.form.get('place'),
            'phone': request.form.get('phone'),
            'content': request.form.get('content'),
            'author': request.form.get('author'),
            'image': image_filename,
            'is_solved': False
        }
        found_items.append(new_item)
        return jsonify({"message": "등록 성공"}), 200

@app.route('/api/lost/<int:index>', methods=['GET'])
def get_lost_detail(index):
    if 0 <= index < len(lost_items) and lost_items[index]:
        return jsonify(lost_items[index]), 200
    return jsonify({"message": "없음"}), 404

@app.route('/api/found/<int:index>', methods=['GET'])
def get_found_detail(index):
    if 0 <= index < len(found_items) and found_items[index]:
        return jsonify(found_items[index]), 200
    return jsonify({"message": "없음"}), 404

@app.route('/api/query', methods=['POST'])
def query_manage():
    queries.append(request.get_json())
    return jsonify({"message": "성공"}), 200

@app.route('/')
def home(): return render_template('index.html')

@app.route('/<path:filename>')
def serve_html(filename): return render_template(filename)

if __name__ == '__main__':
    print("🚀 서버 실행: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)