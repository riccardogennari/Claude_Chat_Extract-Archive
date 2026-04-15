from flask import Flask, render_template, abort, request, jsonify, send_from_directory
import json
import markdown
from pathlib import Path
from datetime import datetime

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

@app.route('/export_offline', methods=['POST'])
def export_offline():
    data = request.get_json()
    selected_filenames = data.get('filenames', [])
    export_title = data.get('title', '').strip()
    export_filename_input = data.get('filename', '').strip()
    export_description = data.get('description', '').strip()

    if not selected_filenames:
        return jsonify({'success': False, 'message': 'Nessuna chat selezionata per l\'esportazione.'}), 400

    # Genera un nome per la cartella di esportazione
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_export_filename = f"export_{timestamp}"
    
    if export_filename_input:
        # Semplice slugification per il nome del file/cartella
        export_folder_name = re.sub(r'[\W_]+', '-', export_filename_input.lower()).strip('-')
    else:
        export_folder_name = default_export_filename

    export_dir = BASE_DIR / "offline_exports" / export_folder_name
    export_dir.mkdir(parents=True, exist_ok=True)

    # Metadati per l'esportazione
    export_metadata = {
        'export_title': export_title if export_title else f"Esportazione Chat Claude ({timestamp})",
        'export_description': export_description,
        'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'source_file': 'conversations.json', # Assumiamo che sia sempre questo
        'exported_chats_count': len(selected_filenames)
    }

    offline_chats_data = []
    for filename in selected_filenames:
        original_chat_path = CHATS_DIR / filename
        if not original_chat_path.exists():
            continue

        # Copia il file MD nella cartella di esportazione
        offline_md_path = export_dir / filename
        with open(original_chat_path, 'r', encoding='utf-8') as f_orig, \
             open(offline_md_path, 'w', encoding='utf-8') as f_dest:
            f_dest.write(f_orig.read())

        # Prepara i dati per il template offline_index.html
        # Recupera i metadati originali della chat per l'indice offline
        original_metadata = next((chat for chat in load_metadata() if chat['filename'] == filename), None)
        if original_metadata:
            offline_chats_data.append({
                'title': original_metadata['title'],
                'date': original_metadata['date'],
                'filename': filename # Questo sarà il link al viewer offline
            })

        # Genera il viewer HTML per la chat
        with open(original_chat_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        html_content = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite', 'tables'])
        
        offline_viewer_html_path = export_dir / f"viewer_{filename.replace('.md', '.html')}"
        with open(offline_viewer_html_path, 'w', encoding='utf-8') as f_viewer:
            f_viewer.write(render_template('offline_viewer.html', content=html_content, raw=md_text, filename=filename, export_metadata=export_metadata))

    # Genera l'indice HTML per l'esportazione
    offline_index_html_path = export_dir / "index.html"
    with open(offline_index_html_path, 'w', encoding='utf-8') as f_index:
        f_index.write(render_template('offline_index.html', chats=offline_chats_data, export_metadata=export_metadata))

    return jsonify({'success': True, 'message': f'Esportazione completata in {export_dir.name}', 'download_link': f'/offline_exports/{export_folder_name}/index.html'})

@app.route('/offline_exports/<path:filename>')
def serve_offline_exports(filename):
    return send_from_directory(BASE_DIR / "offline_exports", filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)