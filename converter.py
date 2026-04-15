import json
import os
import re
from pathlib import Path

def slugify(text):
    """Converte il titolo in un formato valido per i nomi dei file."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text).strip('-')

def process_claude_export(json_path, output_dir="chats"):
    base_path = Path(r"C:\PERSONALE\Miei progetti Python\claude_chat_extractor")
    chats_path = base_path / output_dir
    chats_path.mkdir(parents=True, exist_ok=True)
    
    json_full_path = base_path / json_path
    if not json_full_path.exists():
        print(f"Errore: Il file {json_full_path} non esiste.")
        return

    with open(json_full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    index_data = []

    for chat in data:
        title = chat.get('name') or "Chat senza titolo"
        created_at = chat.get('created_at', 'N/D')
        chat_id = chat.get('uuid', 'unknown')
        
        # Creazione nome file univoco
        clean_title = slugify(title[:50])
        filename = f"{clean_title}-{chat_id[:8]}.md"
        filepath = chats_path / filename
        
        # Generazione contenuto Markdown
        md_content = f"# {title}\n\n"
        md_content += f"**Data Creazione:** {created_at}\n\n"
        md_content += "---\n\n"
        
        for msg in chat.get('chat_messages', []):
            sender = "Claude" if msg.get('sender') == 'assistant' else "User"
            text = msg.get('text', '')
            md_content += f"### {sender}\n\n{text}\n\n---\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f_md:
            f_md.write(md_content)
        
        # Salvataggio metadati per il frontend
        index_data.append({
            'id': chat_id,
            'title': title,
            'date': created_at[:10] if created_at != 'N/D' else 'N/D',
            'filename': filename
        })

    # Salvataggio indice metadati
    with open(base_path / 'metadata.json', 'w', encoding='utf-8') as f_idx:
        json.dump(index_data, f_idx, indent=4, ensure_ascii=False)

    print(f"Conversione completata. {len(index_data)} chat processate.")

if __name__ == "__main__":
    process_claude_export('conversations.json')