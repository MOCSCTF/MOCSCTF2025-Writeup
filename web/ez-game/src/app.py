from flask import Flask,render_template_string ,render_template, request, redirect, url_for, jsonify, session, flash
import os
import random
import json
import python_jwt as jwt
from datetime import datetime, timedelta
import re
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 生成RSA密钥对
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwcrypto.jwk as jwk
# 生成私钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# 序列化私钥
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
private_key_jwk=jwk.JWK.from_pem(pem_private_key)

# 获取公钥
public_key = private_key.public_key()

# 序列化公钥
pem_public_key = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
public_key_jwk=jwk.JWK.from_pem(pem_public_key)
# 用户数据存储
users = {
    'admin': {
        'password': '@dmIn_s3cr3t_pAssw0rd',
        'coins': 100,
        'is_admin': True
    }
}

# Flag
FLAG = open('/flag.txt', 'r').read().strip()

# JWT验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            flash('未登录，请先登录', 'danger')
            return redirect(url_for('login'))
        
        try:
            data = jwt.verify_jwt(token, public_key_jwk,['RS512'])
            current_user = data[1]['username']
            if current_user not in users:
                flash('用户不存在', 'danger')
                return redirect(url_for('login'))
        except:
            flash('Token无效，请重新登录', 'danger')
            return redirect(url_for('login'))
            
        return f(current_user, *args, **kwargs)
    
    return decorated

# 管理员验证装饰器
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            flash('未登录，请先登录', 'danger')
            return redirect(url_for('login'))
        
        try:
            data = jwt.verify_jwt(token, public_key_jwk, ['RS512'])
            current_user = data[1]['username']
            if current_user not in users:
                flash('用户不存在', 'danger')
                return redirect(url_for('login'))
                
            if not users[current_user].get('is_admin', False):
                flash('需要管理员权限', 'danger')
                return redirect(url_for('index'))
        except:
            flash('Token无效，请重新登录', 'danger')
            return redirect(url_for('login'))
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/')
def index():
    token = request.cookies.get('token')
    if token:
        try:
            data = jwt.verify_jwt(token, public_key_jwk, ['RS512'])
            current_user = data[1]['username']
            return render_template('index.html', username=current_user, coins=users[current_user]['coins'])
        except:
            pass
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 验证用户名长度和字符
        if not username or not password:
            flash('用户名和密码不能为空', 'danger')
            return redirect(url_for('register'))
            
        if len(username) > 8:
            flash('用户名长度不能超过8个字符', 'danger')
            return redirect(url_for('register'))
            
        if not re.match('^[a-zA-Z0-9]+$', username):
            flash('用户名只能包含字母和数字', 'danger')
            return redirect(url_for('register'))
            
        if username in users:
            flash('用户名已存在', 'danger')
            return redirect(url_for('register'))
            
        # 创建新用户
        users[username] = {
            'password': password,
            'coins': 100,
            'is_admin': False
        }
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            # 生成JWT token
            token = jwt.generate_jwt(
                {
                    'username': username,
                    'exp': int((datetime.now() + timedelta(hours=1)).timestamp())*10
                },
                private_key_jwk,
                algorithm='RS512'
            )
            
            response = redirect(url_for('index'))
            response.set_cookie('token', token)
            flash('登录成功', 'success')
            return response
        else:
            flash('用户名或密码错误', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = redirect(url_for('index'))
    response.delete_cookie('token')
    flash('已退出登录', 'success')
    return response

@app.route('/game')
@token_required
def game(current_user):
    return render_template('game.html', username=current_user, coins=users[current_user]['coins'])

@app.route('/play', methods=['POST'])
@token_required
def play(current_user):
    user_coins = users[current_user]['coins']
    
    # 检查金币是否足够
    if user_coins < 10:
        return jsonify({'status': 'error', 'message': '金币不足，无法游戏'})
    
    # 扣除10个金币
    users[current_user]['coins'] -= 10
    
    # 获取用户猜的数字
    guess = int(request.form.get('guess'))
    
    # 生成随机数 (1-10)
    if user_coins == 20:  # 当用户只剩20金币时必定猜对
        correct_number = guess
    elif user_coins > 500:  # 超过500金币时必定猜错
        possible_numbers = [i for i in range(1, 11) if i != guess]
        correct_number = random.choice(possible_numbers)
    else:  # 正常情况下随机生成
        correct_number = random.randint(1, 10)
    
    # 判断是否猜对
    if guess == correct_number:
        users[current_user]['coins'] += 20  # 猜对奖励20金币
        return jsonify({
            'status': 'success', 
            'message': f'恭喜你猜对了！数字是{correct_number}，获得20金币', 
            'correct': True,
            'coins': users[current_user]['coins']
        })
    else:
        return jsonify({
            'status': 'success', 
            'message': f'很遗憾，猜错了。正确数字是{correct_number}', 
            'correct': False,
            'coins': users[current_user]['coins']
        })

@app.route('/buy_flag')
@token_required
def buy_flag(current_user):
    if users[current_user]['coins'] >= 10000:
        users[current_user]['coins'] -= 10000
        return render_template('flag.html', flag=FLAG)
    else:
        flash('金币不足，无法购买flag', 'danger')
        return redirect(url_for('game'))

@app.route('/admin')
@admin_required
def admin(current_user):
    return render_template('admin.html', users=users)

@app.route('/admin/update_coins', methods=['POST'])
@admin_required
def update_coins(current_user):
    username = request.form.get('username')
    coins_str = request.form.get('coins')
    if coins_str is None:
        flash('金币数不能为空', 'danger')
        return redirect(url_for('admin'))
    try:
        coins = int(coins_str)
    except ValueError:
        flash('金币数必须为数字', 'danger')
        return redirect(url_for('admin'))
    
    if username in users:
        users[username]['coins'] = coins
        flash(f'已更新用户 {username} 的金币为 {coins}', 'success')
    else:
        flash('用户不存在', 'danger')
        
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999,use_reloader=False)