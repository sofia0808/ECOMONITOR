# 🌿 EcoMonitor

**Sistema di monitoraggio ambientale basato su architettura client-server in Python**

> Progetto UDA Sostenibilità Ambientale — Classe 4A ITIS Informatica  
> **Gruppo:** Awan Ali Atta, Singh Gurpreet, Cristiano Sofia

---

## 📋 Descrizione

EcoMonitor è un sistema distribuito che permette di raccogliere dati ambientali (luminosità e rumore) tramite smartphone con **phyphox**, inviarli a un server centrale tramite **socket TCP**, salvarli in un file CSV e visualizzarli in una dashboard interattiva con **Streamlit**.

Il sistema simula un contesto IoT (Internet of Things) in cui più dispositivi inviano dati a un server centralizzato.

---

## 🏗️ Architettura

```
[Smartphone + phyphox]
        │
        ▼
  [client.py]  ──── TCP/IP ────►  [server.py]
                                       │
                                       ▼
                                 [misure.csv]
                                       │
                                       ▼
                              [dashboard.py (Streamlit)]
```

---

## 📁 Struttura del progetto

```
EcoMonitor/
├── server.py        # Server multithreading con coda condivisa
├── client.py        # Client con supporto multi-sensore e multi-sessione
├── dashboard.py     # Dashboard Streamlit avanzata con filtri
├── misure.csv       # Database CSV delle misure raccolte
└── README.md        # Questo file
```

---

## 🚀 Come avviare il progetto

### Prerequisiti

```bash
pip install streamlit matplotlib pandas
```

### 1. Avvia il server

```bash
python server.py
```

Il server sarà in ascolto su `localhost:5000`.

### 2. Avvia il client (in un altro terminale)

```bash
python client.py
```

Segui le istruzioni a schermo. I comandi disponibili sono:

| Comando | Descrizione |
|---------|-------------|
| `INVIA` | Invia una nuova misura al server |
| `CODA`  | Visualizza lo stato della coda condivisa |
| `ESCI`  | Chiude la connessione |

### 3. Avvia la dashboard

```bash
streamlit run dashboard.py
```

Apri il browser su `http://localhost:8501`

---

## 📊 Sensori utilizzati

| Sensore | App phyphox | Unità | Descrizione |
|---------|------------|-------|-------------|
| **Luce** | Light | lux | Luminosità ambientale |
| **Rumore** | Audio Amplitude | ampiezza | Livello sonoro relativo |

---

## 🌐 Funzionalità

### Versione base ✅
- Server multithreading con coda condivisa
- Client con comandi INVIA / CODA / ESCI
- Salvataggio dati su CSV
- Dashboard con tabella, statistiche e grafico per luogo

### Versione avanzata ✅
- Due sensori: luce e rumore
- Filtri per sensore, luogo e studente
- Statistiche separate per sensore
- Classifica luoghi più illuminati/rumorosi
- Grafico a linee comparativo
- Export CSV dei dati filtrati
- Gestione errori di connessione e validazione input

---

## 📝 Formato CSV

```
studente,sensore,valore,luogo,data_ora
Awan Ali Atta,luce,312,aula_4A,2026-05-19 08:15:22
Singh Gurpreet,rumore,0.062,corridoio,2026-05-19 08:19:45
```

---

## 🛠️ Tecnologie

- **Python 3.x**
- **socket** — comunicazione TCP/IP
- **threading** — gestione connessioni concorrenti
- **queue** — coda condivisa thread-safe
- **csv** — persistenza dei dati
- **Streamlit** — dashboard interattiva
- **Matplotlib** — grafici
- **phyphox** — acquisizione dati reali da smartphone

---

## 👥 Gruppo di lavoro

| Nome | Ruolo |
|------|-------|
| Awan Ali Atta | Sviluppo server e gestione coda |
| Singh Gurtjpreet | Sviluppo client e integrazione phyphox |
| Cristiano Sofia | Dashboard Streamlit e relazione |

---

*EcoMonitor v2.0 — Progetto UDA Sostenibilità Ambientale*