# app.py

import os

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

ACCOUNTS_TABLE = os.environ['ACCOUNTS_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/accounts/<string:account_id>")
def get_account(account_id):
    resp = client.get_item(
        TableName=ACCOUNTS_TABLE,
        Key={
            'accountId': {'S': account_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Account does not exist'}), 404

    return jsonify({
        'accountId': item.get('accountId').get('S'),
        'name': item.get('name').get('S'),
        'balance': item.get('balance').get('N')
    })


@app.route("/accounts", methods=["POST"])
def create_account():
    account_id = request.json.get('accountId')
    name = request.json.get('name')
    balance = request.json.get('balance')
    if not account_id or not name:
        return jsonify({'error': 'Please provide accountId and name'}), 400

    resp = client.put_item(
        TableName=ACCOUNTS_TABLE,
        Item={
            'accountId': {'S': account_id},
            'name': {'S': name},
            'balance': {'N': balance}
        }
    )

    return jsonify({
        'accountId': account_id,
        'name': name,
        'balance': balance
    })
