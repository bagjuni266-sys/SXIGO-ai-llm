"""DLTServer.py
Simple Flask proxy server for the DLT HTML client.
This server serves the DLT HTML page and proxies /api/chat requests to a local Ollama instance.
"""

import logging
import os
import requests
from flask import Flask, jsonify, request, Response, send_file, stream_with_context
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'), static_url_path='/static')
CORS(APP, supports_credentials=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s [DLTServer] %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_OLLAMA_HOST = os.environ.get('DLT_OLLAMA_HOST', 'http://localhost:11434').rstrip('/')
DEFAULT_PORT = int(os.environ.get('DLT_SERVER_PORT', '8080'))


def serve_html(filename: str):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        logger.error(f"Missing HTML file: {file_path}")
        return jsonify({'error': 'File not found'}), 404
    response = send_file(file_path, mimetype='text/html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@APP.route('/')
def index():
    return serve_html('DLT.html')


@APP.route('/DLT.html')
def dlt_html():
    return serve_html('DLT.html')


@APP.route('/api/chat', methods=['POST'])
def api_chat():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({'error': 'Invalid JSON body'}), 400

    url = f"{DEFAULT_OLLAMA_HOST}/api/chat"
    stream_enabled = bool(payload.get('stream', False))

    try:
        upstream = requests.post(url, json=payload, stream=stream_enabled, timeout=120)
    except requests.RequestException as exc:
        logger.exception('Failed to call Ollama API')
        return jsonify({'error': 'Ollama connection failed', 'details': str(exc)}), 502

    headers = {}
    for key, value in upstream.headers.items():
        if key.lower() in ['content-length', 'transfer-encoding', 'connection', 'content-encoding']:
            continue
        headers[key] = value

    if stream_enabled:
        return Response(
            stream_with_context(upstream.iter_content(chunk_size=4096)),
            status=upstream.status_code,
            headers=headers,
            content_type=upstream.headers.get('Content-Type', 'text/event-stream')
        )

    return Response(upstream.content, status=upstream.status_code, headers=headers, content_type=upstream.headers.get('Content-Type', 'application/json'))


@APP.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'server': 'DLTServer',
        'ollama_host': DEFAULT_OLLAMA_HOST,
        'timestamp': request.date
    })


if __name__ == '__main__':
    logger.info(f'Starting DLTServer on http://127.0.0.1:{DEFAULT_PORT}')
    APP.run(host='127.0.0.1', port=DEFAULT_PORT, debug=False)
