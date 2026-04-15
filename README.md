# Claude Chat Extractor & Viewer

Questo progetto permette di esportare le conversazioni di Claude (da file JSON) in singoli file Markdown e di visualizzarle attraverso un'interfaccia web locale elegante e funzionale.

## Funzionalità

- **Conversione Automatica**: Trasforma il file `conversations.json` esportato da Claude in singoli file `.md`.
- **Dashboard Web**: Interfaccia sviluppata in Flask per elencare tutte le chat.
- **Filtraggio Dinamico**: Possibilità di filtrare le chat per titolo o data direttamente dalla pagina principale.
- **Doppia Visualizzazione**: Ogni chat può essere visualizzata come HTML renderizzato (per una lettura agevole) o come sorgente Markdown originale.
- **Slugification**: I nomi dei file vengono generati automaticamente dai titoli delle chat per una facile gestione nel file system.

## Struttura del Progetto

- `converter.py`: Script per processare il JSON e generare i file Markdown e l'indice dei metadati.
- `app.py`: Web server Flask per la navigazione delle chat.
- `chats/`: Cartella (generata) contenente i file Markdown.
- `templates/`: Cartella contenente i template HTML (`index.html` e `viewer.html`).

## Installazione

1. Assicurati di avere Python installato.
2. Installa le dipendenze necessarie:
   ```bash
   pip install flask markdown
   ```

## Utilizzo

1. Posiziona il tuo file `conversations.json` (ottenuto dall'export di Claude) nella cartella radice del progetto.
2. Esegui lo script di conversione:
   ```bash
   python converter.py
   ```
3. Avvia l'applicazione web:
   ```bash
   python app.py
   ```
4. Apri il browser all'indirizzo `http://127.0.0.1:5000`.

## Requisiti

- Python 3.x
- Flask
- Markdown (libreria Python)
- Bootstrap 5 (via CDN)

---
*Sviluppato per la gestione della conoscenza personale tramite chat AI.*