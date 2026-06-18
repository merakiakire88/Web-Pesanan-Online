import pandas as pd
import requests
import json
import os
import streamlit as st

def get_menu():
    try:
        df = pd.read_excel("menu.xlsx")
        return df.set_index('id').to_dict('index')
    except Exception:
        return None

def simpan_ke_json(data_pesanan):
    daftar_pesanan = []
    if os.path.exists("pesanan.json"):
        with open("pesanan.json", "r") as file:
            try:
                data_lama = json.load(file)
                if isinstance(data_lama, list):
                    daftar_pesanan = data_lama
                elif isinstance(data_lama, dict):
                    daftar_pesanan = [data_lama] 
            except json.JSONDecodeError:
                daftar_pesanan = []
                
    daftar_pesanan.append(data_pesanan)
    with open("pesanan.json", "w") as file:
        json.dump(daftar_pesanan, file, indent=4)

    st.session_state["indeks_pesanan_saya"] = len(daftar_pesanan) - 1

def baca_status_json():
    if os.path.exists("pesanan.json") and "indeks_pesanan_saya" in st.session_state:
        with open("pesanan.json", "r") as file:
            try:
                data = json.load(file)
                idx = st.session_state["indeks_pesanan_saya"]
                if isinstance(data, list) and idx < len(data):
                    return data[idx].get("status", "Diterima")
            except:
                return "Diterima"
    return "Diterima"

def baca_pesanan_json():
    if os.path.exists("pesanan.json"):
        with open("pesanan.json", "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return [data]
            except json.JSONDecodeError:
                return []
    return []

def update_status_json(index_pesanan, status_baru):
    daftar_pesanan = baca_pesanan_json()
    if daftar_pesanan and index_pesanan < len(daftar_pesanan):
        daftar_pesanan[index_pesanan]["status"] = status_baru
        with open("pesanan.json", "w") as file:
            json.dump(daftar_pesanan, file, indent=4)

@st.cache_data
def get_kecamatan(kabupaten_id):
    try:
        url = f"https://emsifa.github.io/api-wilayah-indonesia/api/districts/{kabupaten_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def hitung_estimasi_jarak(kabupaten_id, nama_kecamatan):
    base_jarak = {
        "3674": 4,  # Tangsel
        "3603": 12, # Kab Tangerang
        "3201": 22  # Kab Bogor
    }
    variasi = len(nama_kecamatan) % 6 
    return base_jarak[kabupaten_id] + variasi