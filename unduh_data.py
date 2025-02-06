import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import yfinance as yf
import pandas as pd
from datetime import datetime

# Pastikan file credentials.json ada
with open('credentials.json') as f:
    firebase_cred = json.load(f)

# Cek apakah Firebase sudah diinisialisasi sebelumnya
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred)


# Inisialisasi Firestore
db = firestore.client()

# Daftar ticker saham LQ45
lq45_tickers = [
    'ACES.JK', 'ADRO.JK', 'AKRA.JK', 'AMMN.JK', 'AMRT.JK',
    'ANTM.JK', 'ARTO.JK', 'ASII.JK', 'BBCA.JK', 'BBNI.JK',
    'BBRI.JK', 'BBTN.JK', 'BMRI.JK', 'BRIS.JK', 'BRPT.JK',
    'BUKA.JK', 'CPIN.JK', 'ESSA.JK', 'EXCL.JK', 'GGRM.JK',
    'GOTO.JK', 'HRUM.JK', 'ICBP.JK', 'INCO.JK', 'INDF.JK',
    'INKP.JK', 'INTP.JK', 'ISAT.JK', 'ITMG.JK', 'KLBF.JK',
    'MAPI.JK', 'MBMA.JK', 'MDKA.JK', 'MEDC.JK', 'MTEL.JK',
    'PGAS.JK', 'PGEO.JK', 'PTBA.JK', 'SIDO.JK', 'SMGR.JK',
    'SRTG.JK', 'TLKM.JK', 'TOWR.JK', 'UNTR.JK', 'UNVR.JK'
]

# Mengunduh data per jam dan menyimpannya di Firestore
for ticker in lq45_tickers:
    stock_data = yf.download(ticker, period="1d", interval="60m")  # Data per jam

    # Simpan data di Firestore
    for date_time, row in stock_data.iterrows():
        date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')

        # Referensi ke dokumen yang sesuai di Firestore
        doc_ref = db.collection("stocks").document(ticker).collection("daily_data").document(date_time_str)

        if doc_ref.get().exists:
            doc_ref.delete()  

        # Simpan data harga saham ke Firestore
        doc_ref.set({
            "Adj Close": float(row['Adj Close']) if 'Adj Close' in row else None,
            "Close": float(row['Close']),
            "High": float(row['High']),
            "Low": float(row['Low']),
            "Open": float(row['Open']),
            "Volume": int(row['Volume'])
        })

print("Data saham per jam berhasil diperbarui di Firestore.")
