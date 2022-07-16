from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'a'

@app.route('/')
def home():
    if not session.get('loggedin'):
        return render_template('signup.html')
    else:
        return render_template('welcome.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)