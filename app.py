from flask import Flask, render_template, request, session

from cryptography.fernet import Fernet
from menu import page_menu
from function import session_creation, check_session, session_del
from dict_words import words
app = Flask(__name__)
app.config.from_object('config_local')


@app.route('/', methods=["GET"])
def main():
    if not check_session():
        session_creation()
    language = session['language']
    menu = page_menu(language)
    return render_template('index.html',
                           menu=menu,
                           words=words,
                           title=words['site_name'][language],
                           description=words['site_description'][language],
                           language=language)


@app.route('/encrypt/', methods=["POST", "GET"])
def encrypt():
    if not check_session():
        session_creation()
    language = session['language']
    menu = page_menu(language)
    start = True
    title = words['encrypt_text'][language]
    description = words['encrypt_description'][language]
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
        title = words['encrypted_text_and_key'][session['language']]

        return render_template('encrypt.html',
                               menu=menu,
                               text=text,
                               key=key,
                               words=words,
                               title=title,
                               description=description,
                               language=language,
                               start=start,
                               )

    return render_template('encrypt.html',
                           menu=menu,
                           words=words,
                           title=title,
                           description=description,
                           language=language,
                           start=start
                           )


@app.route('/decrypt/', methods=["POST", "GET"])
def decrypt():
    if not check_session():
        session_creation()

    language = session['language']
    title = words['decrypt_text'][session['language']]
    description = words['decrypt_description'][language]

    menu = page_menu(language)

    if request.method == 'POST':
        byte_key = str.encode(request.form['UserKey'])
        text = str.encode(request.form['text'])
        cipher = Fernet(byte_key)

        # Result
        text = cipher.decrypt(text).decode()
        key = byte_key.decode()
        title = words['decrypted_text_and_key'][session['language']]

        return render_template('decrypt.html',
                               menu=menu,
                               text=text,
                               key=key,
                               words=words,
                               language=language,
                               description=description,
                               title=title)

    return render_template('decrypt.html',
                           menu=menu,
                           words=words,
                           language=language,
                           description=description,
                           title=title)


@app.route('/del/', methods=["GET"])
def dell():
    return session_del()


if __name__ == '__main__':  # Запуск сервера на локальном устройстве
    app.run(debug=True)  # отображение ошибок
