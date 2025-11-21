from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 프론트엔드와 백엔드 통신 허용

# 임시 데이터베이스
users = {}        # 회원정보 저장
lost_items = []   # 분실물 게시글 저장
found_items = []  # 습득물 게시글 저장
queries = []      # 문의사항 저장

# 1. 회원가입 API
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    email = data.get('email') 
    
    if user_id in users:
        return jsonify({"message": "이미 존재하는 아이디입니다."}), 400
    
    users[user_id] = password
    print(f"✅ 회원가입 완료: {user_id}") 
    return jsonify({"message": "회원가입 성공"}), 200

# 2. 로그인 API
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    if user_id in users and users[user_id] == password:
        print(f"🔑 로그인 성공: {user_id}")
        return jsonify({"message": "로그인 성공"}), 200
    else:
        print(f"❌ 로그인 실패 시도: {user_id}")
        return jsonify({"message": "아이디 또는 비밀번호 오류"}), 401

# 3. 분실물(잃어버렸어요) 관리 API
@app.route('/api/lost', methods=['GET', 'POST'])
def lost_manage():
    if request.method == 'POST':
        data = request.get_json()
        lost_items.append(data)
        return jsonify({"message": "분실물 등록 성공"}), 200
    return jsonify(lost_items), 200

# 4. 습득물(찾았어요) 관리 API
@app.route('/api/found', methods=['GET', 'POST'])
def found_manage():
    if request.method == 'POST':
        data = request.get_json()
        found_items.append(data)
        return jsonify({"message": "습득물 등록 성공"}), 200
    return jsonify(found_items), 200

# 5. 1대1 문의 API
@app.route('/api/query', methods=['POST'])
def query_manage():
    data = request.get_json()
    queries.append(data)
    print(f"📩 문의 접수: {data}")
    return jsonify({"message": "문의가 등록되었습니다."}), 200

# 서버 실행
if __name__ == '__main__':
    print("🚀 서버가 시작되었습니다! http://127.0.0.1:5000")
    app.run(debug=True, port=5000)