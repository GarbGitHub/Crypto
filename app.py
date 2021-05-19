from flask import Flask, render_template, request
from cryptography.fernet import Fernet
from menu import page_menu

app = Flask(__name__)


@app.route('/', methods=["GET"])
def main():
    # ip = request.headers.get('X-Real-IP')
    ip = request.environ['REMOTE_ADDR']
    print(ip)
    menu = page_menu()
    title = 'Text cryptographer'
    return render_template('index.html',
                           ip=ip,
                           menu=menu,
                           title=title)


@app.route('/encrypt/', methods=["POST", "GET"])
def encrypt():
    menu = page_menu()
    start = True
    title = 'Encrypt text'
    if request.method == 'POST':
        my_str = request.form['text']
        type_key = int(request.form['flexRadioDefault'])  # 1 or 2

        # Key (bytecode)
        if type_key == 1:
            byte_key = Fernet.generate_key()
        else:
            byte_key = str.encode(request.form['UserKey'])

        cipher = Fernet(byte_key)

        # Convert text to bytecode
        text = str.encode(my_str)

        # Encode text
        encrypted_text = cipher.encrypt(text)

        # Result
        text = encrypted_text.decode()
        key = byte_key.decode()
        start = False
        title = 'Cipher text and key'

        return render_template('encrypt.html',
                               menu=menu,
                               text=text,
                               key=key,
                               title=title,
                               start=start)

    return render_template('encrypt.html',
                           menu=menu,
                           start=start,
                           title=title)


@app.route('/decrypt/', methods=["POST", "GET"])
def decrypt():
    title = 'Decrypt text'
    menu = page_menu()
    if request.method == 'POST':
        byte_key = str.encode(request.form['UserKey'])
        text = str.encode(request.form['text'])
        cipher = Fernet(byte_key)

        # Result
        text = cipher.decrypt(text).decode()
        key = byte_key.decode()
        title = 'Decrypted text and key'

        return render_template('decrypt.html',
                               menu=menu,
                               text=text,
                               key=key,
                               title=title)

    return render_template('decrypt.html',
                           menu=menu,
                           title=title)


if __name__ == '__main__':  # Запуск сервера на локальном устройстве
    app.run(debug=True)  # отображение ошибок
