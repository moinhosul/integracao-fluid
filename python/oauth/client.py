from flask import Flask, jsonify, url_for, render_template, request, redirect, session
from oauthlib.oauth2 import WebApplicationClient
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from urllib3 import HTTPSConnectionPool
import hashlib
import base64
import os
import re
import random
import string
import pycurl
import requests
import urllib
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = 'chavesupersecreta'

BASE_URL = 'https://localhost:9444'

class Client(db.Model):
    client_id = db.Column(db.String(2048), primary_key=True)
    code_verifier = db.Column(db.String(2048))
    code_challenge = db.Column(db.String(2048))
    jwt = db.Column(db.String(2048))
    access_token = db.Column(db.String(2048))
    refresh_token = db.Column(db.String(2048))


@app.route('/')
def main():
    return render_template('authenticate.html')

@app.route('/autenticar', methods=['POST'])
def login():
    client_id = request.form.get('client_id')
    escopos = []

    if request.form.get('criar'):
        escopos.append('criar')
    if request.form.get('preencher'):
        escopos.append('preencher')
    if request.form.get('protocolar'):
        escopos.append('protocolar')

    state = hashlib.sha256(random_string(24)).hexdigest()    
    cliente_servico = Client.query.get(client_id)
    session['state'] = state
    session['client_id'] = client_id
    if not cliente_servico:
        code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
        code_challenge = code_challenge.replace('=', '')
        scope = ['criar', 'preencher', 'protocolar']
        client_db = Client(
            client_id=client_id,
            code_verifier=code_verifier,
            code_challenge=code_challenge
        )
        db.session.add(client_db)
        db.session.commit()
    else:
        code_verifier = cliente_servico.code_verifier
        code_challenge = cliente_servico.code_challenge
    
    client = WebApplicationClient(client_id)
        
    uri = client.prepare_request_uri(
        BASE_URL + '/oauth2/oauth/autorizacao',
        redirect_uri='https://localhost:5000/callback',
        scope=escopos,
        code_challenge_method='S256',
        code_challenge=code_challenge,
        state=state
        )
    return redirect(uri)

@app.route('/callback')
def callback():
    if request.args.get('code'):
        if request.args.get('state') == session['state']:
            cliente_servico = Client.query.get(session['client_id'])
            client = WebApplicationClient(session['client_id'])
            post_data = {
                "grant_type":"authorization_code",
                "client_id":cliente_servico.client_id,
                "code":request.args.get('code'),
                "redirect_uri":"https://localhost:5000/callback",
                "code_verifier": cliente_servico.code_verifier
            }
            # pool = HTTPSConnectionPool('https://centrolesters.websicredi.com.br', port=9444, cert_reqs='CERT_NONE', assert_hostname=False, retries=False)
            # response = pool.request('POST', url='/oauth2/oauth/access-token', fields=post_data, retrues=0)
            # print(response)
            r = requests.post(BASE_URL + '/oauth2/oauth/access-token', data=post_data, verify=False)
            if(r.status_code == 200):
                response = json.loads(r.text)
                cliente_servico.access_token = response['access_token']
                cliente_servico.refresh_token = response['refresh_token']
                cliente_servico.access_token = request.args.get('code')
                cliente_servico.jwt = response['access_token']
                db.session.add(cliente_servico)
                db.session.commit()
                return jsonify(r.text)
            else:
                return redirect('/error')
        else:
            return redirect('/error')

@app.route('/erro')
def error():
    return render_template('error.html')

@app.route('/procurar', methods = ['GET'])
def procurar_get():
    return render_template('procurar.html')

@app.route('/procurar', methods = ['POST'])
def procurar_post():
    client_id = request.form.get('client_id')
    cliente_servico = Client.query.get(client_id)
    cliente_to_return = {
        "client_id": cliente_servico.client_id,
        "code_verifier": cliente_servico.code_verifier,
        "code_challenge": cliente_servico.code_challenge,
        "jwt": cliente_servico.jwt,
        "access_token": cliente_servico.access_token,
        "refresh_token": cliente_servico.refresh_token
    }
    return jsonify(cliente_to_return)

def random_string(n):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(n)).encode('utf-8')