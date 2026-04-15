from flask import Flask, render_template, abort
import json
import markdown
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(r"C:\PERSONALE\Miei progetti Python\claude_chat_extractor")
CHATS_DIR = BASE_DIR / "chats"

def load_metadata():
    meta_path = BASE_DIR / "metadata.json"
    if not meta_path.exists():
        return []
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    chats = load_metadata()
    # Ordina per data decrescente
    chats.sort(key=lambda x: x['date'], reverse=True)
    return render_template('index.html', chats=chats)

@app.route('/chat/<filename>')
def view_chat(filename):
    chat_path = CHATS_DIR / filename
    if not chat_path.exists():
        abort(404)
        
    with open(chat_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Conversione Markdown in HTML con estensioni per tabelle e blocchi di codice
    html_content = markdown.markdown(
        md_text, 
        extensions=['fenced_code', 'codehilite', 'tables']
    )
    return render_template('viewer.html', content=html_content, raw=md_text, filename=filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)