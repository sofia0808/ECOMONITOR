# EcoMonitor — Relazione tecnica

**Gruppo:** Awan Ali Atta, Singh Gurtjpreet, Cristiano Sofia  
**Classe:** 4E ITIS Informatica  
**Data:** Maggio 2026

---

## 1. Introduzione

EcoMonitor è un sistema di monitoraggio ambientale basato su architettura client-server sviluppato in Python. L'obiettivo è raccogliere dati ambientali (luminosità e rumore) tramite dispositivi mobili con l'app phyphox, trasmetterli a un server centrale, salvarli in un file CSV e analizzarli tramite una dashboard interattiva realizzata con Streamlit.

Il sistema simula un contesto IoT (Internet of Things), in cui più dispositivi inviano dati a un server centralizzato per l'elaborazione e la visualizzazione.

---

## 2. Obiettivi del progetto

- Raccogliere dati ambientali in tempo reale tramite smartphone
- Gestire la comunicazione tra più dispositivi e un server centrale usando socket TCP
- Salvare i dati in modo strutturato su file CSV
- Analizzare i dati tramite grafici e statistiche
- Visualizzare le informazioni in una dashboard interattiva con filtri

---

## 3. Tecnologie utilizzate

| Tecnologia | Utilizzo |
|-----------|---------|
| Python 3 | Linguaggio principale |
| socket TCP/IP | Comunicazione client-server |
| threading | Gestione connessioni concorrenti |
| queue | Coda condivisa thread-safe |
| csv | Persistenza dati su file |
| Streamlit | Dashboard interattiva |
| Matplotlib | Grafici e visualizzazioni |
| phyphox | Acquisizione dati da smartphone |

---

## 4. Architettura del sistema

Il sistema è composto da tre componenti principali:

### 4.1 Server (server.py)

Il server è il componente centrale del sistema. Utilizza i thread per gestire più connessioni simultanee: ogni client che si connette ottiene un thread dedicato. I dati in arrivo vengono inseriti in una coda condivisa (thread-safe grazie a `threading.Lock`), elaborati e salvati nel file CSV. Il server risponde a ogni richiesta con la data e l'ora correnti come conferma di ricezione.

**Funzioni principali:**
- `avvia_server()` — inizializza il socket e accetta connessioni
- `gestisci_client()` — eseguita in un thread separato per ogni client
- `salva_su_csv()` — aggiunge una riga al file misure.csv
- `inizializza_csv()` — crea il file con intestazione se non esiste

### 4.2 Client (client.py)

Il client si connette al server tramite socket TCP, si identifica con il nome dello studente e invia misure ambientali. Supporta più misure nella stessa sessione senza disconnettersi. I comandi disponibili sono:

- `INVIA` — avvia la procedura di invio di una misura
- `CODA` — richiede lo stato della coda al server
- `ESCI` — chiude la connessione in modo pulito

Il client gestisce gli errori di connessione (server non raggiungibile, disconnessione improvvisa) e valida i dati prima dell'invio.

### 4.3 Dashboard (dashboard.py)

La dashboard è sviluppata con Streamlit e offre:

**Versione base:**
- Tabella completa dei dati raccolti
- Numero totale di misure
- Valore medio
- Grafico a barre delle misure per luogo
- Conteggio misure per studente

**Versione avanzata:**
- Filtri per sensore, luogo e studente nella sidebar
- Statistiche separate per ciascun sensore
- Grafico a linee comparativo tra luoghi
- Grafico a torta per distribuzione tra sensori
- Classifica luoghi per valore medio
- Export CSV dei dati filtrati

---

## 5. Protocollo di comunicazione

La comunicazione avviene tramite socket TCP sulla porta 5000. Il formato dei messaggi è testuale:

```
Client → Server: INVIA
Server → Client: "Formato: SENSORE|VALORE|LUOGO\nInserisci i dati: "
Client → Server: luce|312|aula_4A
Server → Client: "Dato salvato! Data e ora: 2026-05-19 08:15:22"
```

---

## 6. Formato del file CSV

```
studente,sensore,valore,luogo,data_ora
Awan Ali Atta,luce,312,aula_4A,2026-05-19 08:15:22
Singh Gurpreet,rumore,0.062,corridoio,2026-05-19 08:19:45
```

---

## 7. Sensori utilizzati

Sono stati utilizzati due sensori, scelti perché rappresentano grandezze ambientali diverse e facilmente confrontabili:

**Luminosità (luce)**
- App phyphox: *Light*
- Unità: lux (approssimativi)
- Uso: confrontare l'illuminazione di ambienti diversi (aula, laboratorio, corridoio, cortile)

**Rumore (ampiezza audio)**
- App phyphox: *Audio Amplitude*
- Unità: ampiezza relativa (adimensionale)
- Uso: confrontare il livello sonoro in momenti o ambienti diversi
- Nota: i valori non sono misure professionali certificate, ma indicatori relativi utili per il confronto

---

## 8. Scelte tecniche — versione avanzata

- **Due sensori:** permette confronti più ricchi e una dashboard più informativa
- **Filtri multipli:** l'utente può analizzare sottoinsiemi dei dati in modo interattivo
- **Grafico a linee comparativo:** evidenzia le differenze tra luoghi per ogni sensore
- **Validazione input lato client:** il valore numerico viene verificato prima dell'invio per evitare dati corrotti nel CSV
- **Cache Streamlit con TTL=10s:** i dati si aggiornano automaticamente ogni 10 secondi senza ricaricare manualmente la pagina

---

## 9. Istruzioni per l'esecuzione

```bash
# 1. Installare le dipendenze
pip install streamlit matplotlib pandas

# 2. Avviare il server
python server.py

# 3. Avviare il client (altro terminale)
python client.py

# 4. Avviare la dashboard
streamlit run dashboard.py
```

---

## 10. Conclusioni

Il progetto EcoMonitor ha permesso di applicare concretamente concetti fondamentali dell'informatica di rete: socket TCP, multithreading, sincronizzazione con lock e code condivise. L'aggiunta di phyphox ha reso il progetto concreto, collegando il codice a misure reali dell'ambiente scolastico. La dashboard Streamlit ha dimostrato come i dati grezzi possano essere trasformati in informazioni utili e accessibili tramite visualizzazioni interattive.
