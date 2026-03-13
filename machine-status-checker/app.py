from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>CloudHarem - Machine Status Checker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #00d4ff; }
        input[type="text"] {
            width: 100%%; padding: 12px;
            background: #16213e; border: 1px solid #00d4ff;
            color: #fff; border-radius: 4px; font-size: 16px;
        }
        button {
            padding: 12px 24px; background: #00d4ff; margin-top: 10px;
            border: none; color: #1a1a2e; cursor: pointer;
            border-radius: 4px; font-weight: bold; font-size: 14px;
        }
        button:hover { background: #00a8cc; }
        .result {
            margin-top: 20px; padding: 20px;
            background: #16213e; border-radius: 4px;
            white-space: pre-wrap; font-family: monospace;
            max-height: 400px; overflow-y: auto;
        }
        .footer { margin-top: 40px; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CloudHarem - Machine Status Checker</h1>
        <p>Internal monitoring tool - Check the status of cloud machines</p>
        <form id="f">
            <input type="text" id="h" placeholder="http://example.com/status" required>
            <button type="submit">Check Status</button>
        </form>
        <div class="result" id="r" style="display:none;"></div>
        <div class="footer">
            <p>CloudHarem Industries - Internal DevOps Tool v2.3.1</p>
        </div>
    </div>
    <script>
    document.getElementById('f').onsubmit = async(e) => {
        e.preventDefault();
        const r = document.getElementById('r');
        r.style.display = 'block';
        r.textContent = 'Checking...';
        try {
            const res = await fetch('/api/check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: document.getElementById('h').value})
            });
            r.textContent = await res.text();
        } catch(err) { r.textContent = 'Error: ' + err; }
    };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/api/check', methods=['POST'])
def check():
    url = request.json.get('url', '')
    if not url:
        return "Error: No URL provided", 400
    try:
        # VULNERABLE: SSRF - No URL validation
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return resp.text
    except requests.exceptions.Timeout:
        return "Error: Connection timeout"
    except requests.exceptions.ConnectionError as e:
        return f"Error: Connection failed - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
