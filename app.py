from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 임시 데이터베이스
users = {}
lost_items = []
found_items = []
queries = []

# ==========================================
#  [1] API 영역 (데이터 처리 - 기존 기능)
# ==========================================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    email = data.get('email')
    
    if user_id in users:
        return jsonify({"message": "이미 존재하는 아이디입니다."}), 400
    
    users[user_id] = password
    print(f"회원가입 완료: {user_id}")
    return jsonify({"message": "회원가입 성공"}), 200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    if user_id in users and users[user_id] == password:
        print(f"로그인 성공: {user_id}")
        return jsonify({"message": "로그인 성공"}), 200
    else:
        print(f"로그인 실패 시도: {user_id}")
        return jsonify({"message": "아이디 또는 비밀번호 오류"}), 401

@app.route('/api/lost', methods=['GET', 'POST'])
def lost_manage():
    if request.method == 'POST':
        data = request.get_json()
        lost_items.append(data)
        return jsonify({"message": "분실물 등록 성공"}), 200
    return jsonify(lost_items), 200

@app.route('/api/found', methods=['GET', 'POST'])
def found_manage():
    if request.method == 'POST':
        data = request.get_json()
        found_items.append(data)
        return jsonify({"message": "습득물 등록 성공"}), 200
    return jsonify(found_items), 200

@app.route('/api/query', methods=['POST'])
def query_manage():
    data = request.get_json()
    queries.append(data)
    print(f"문의 접수: {data}")
    return jsonify({"message": "문의가 등록되었습니다."}), 200

@app.route('/api/lost/<int:index>', methods=['GET'])
def get_lost_detail(index):
    if 0 <= index < len(lost_items):
        return jsonify(lost_items[index]), 200
    return jsonify({"message": "찾을 수 없습니다."}), 404

@app.route('/api/found/<int:index>', methods=['GET'])
def get_found_detail(index):
    if 0 <= index < len(found_items):
        return jsonify(found_items[index]), 200
    return jsonify({"message": "찾을 수 없습니다."}), 404


# ==========================================
#  [2] 페이지 영역 (HTML 서빙 - 새로 추가됨!)
# ==========================================

# 메인 페이지 접속 시 (http://127.0.0.1:5000/)
@app.route('/')
def home():
    return render_template('index.html')

# 다른 모든 HTML 파일 접속 시 (예: /login.html, /report_lost.html 등)
@app.route('/<path:filename>')
def serve_html(filename):
    return render_template(filename)


if __name__ == '__main__':
    print("🚀 서버가 시작되었습니다! http://127.0.0.1:5000")
    app.run(debug=True, port=5000)