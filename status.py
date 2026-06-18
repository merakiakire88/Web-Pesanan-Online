import streamlit as st
from utils import baca_status_json, baca_pesanan_json
from css import generate_struk_html

def render_halaman_monitoring(MENU_ITEMS):
    st.title("⏳ Monitoring Pesanan Anda")
    st.write("Halaman ini memperbarui status pembuatan makanan Anda secara berkala.")
    st.divider()
    
    semua_pesanan = baca_pesanan_json()
    jenis_layanan = st.session_state.get("jenis_layanan", "ambil")
    nama_target = st.session_state.get("nama_penerima") if jenis_layanan == "antar" else st.session_state.get("nama_pelanggan")
    no_telp_target = st.session_state.get("no_telp")

    pesanan_saya = None
    if isinstance(semua_pesanan, list):
        for p in reversed(semua_pesanan):
            if p.get("nama") == nama_target and p.get("no_telp") == no_telp_target:
                pesanan_saya = p
                break
    elif isinstance(semua_pesanan, dict):
        if semua_pesanan.get("nama") == nama_target and semua_pesanan.get("no_telp") == no_telp_target:
            pesanan_saya = semua_pesanan

    status_sekarang = pesanan_saya.get("status", "Diterima") if pesanan_saya else "Diterima"

    if pesanan_saya:
        st.subheader("🧾 Struk Pesanan Anda")
        
        html_items = ""
        total_qty = 0
        for m_id, qty in pesanan_saya.get('detail_item', {}).items():
            if qty > 0:
                nama_menu = MENU_ITEMS[m_id]["nama"]
                harga_total_item = MENU_ITEMS[m_id]["harga"] * qty
                total_qty += qty
                html_items += f"<div style='margin-bottom: 4px;'>{nama_menu} x{qty} <span style='float: right;'>Rp {harga_total_item:,}</span></div>"

        ongkir_val = pesanan_saya.get('ongkir', 0)
        diskon_val = pesanan_saya.get('diskon', 0)
        subtotal_val = pesanan_saya.get('subtotal', 0)
        waktu_val = pesanan_saya.get('waktu', 'Waktu tidak tercatat')
        metode_bayar_val = pesanan_saya.get('metode_pembayaran', 'Tunai/Digital')

        struk_html = generate_struk_html(
            pesanan_saya, total_qty, html_items, 
            ongkir_val, diskon_val, subtotal_val, 
            waktu_val, metode_bayar_val
        )
        st.html(struk_html)
    else:
        st.info("Belum ada data pesanan aktif untuk nama Anda saat ini.")
    
    if st.session_state.jenis_layanan == "antar":
        daftar_status = ["Diterima", "Disiapkan", "Diantar", "Sampai", "Selesai"]
        status_display = {
            "Diterima": "📥 Pesanan Diterima oleh Sistem",
            "Disiapkan": "👨‍🍳 Pesanan Sedang Disiapkan di Dapur",
            "Diantar": "🛵 Pesanan Sedang Diantar oleh Kurir",
            "Sampai": "👉 Pesanan Telah Sampai di Lokasi Anda",
            "Selesai": "✅ Pesanan Telah Selesai"
        }
    else:
        daftar_status = ["Diterima", "Disiapkan", "Sampai", "Selesai"]
        status_display = {
            "Diterima": "📥 Pesanan Diterima oleh Sistem",
            "Disiapkan": "👨‍🍳 Pesanan Sedang Disiapkan di Dapur",
            "Sampai": "🛍️ Pesanan Siap Diambil",
            "Selesai": "✅ Pesanan Telah Selesai"
        }
    
    try:
        current_step = daftar_status.index(status_sekarang)
    except ValueError:
        current_step = 0

    st.subheader("📋 Status Terkini:")
    with st.container(border=True):
        for index, kuncian_status in enumerate(daftar_status):
            text_tampil = status_display[kuncian_status]
            if index < current_step:
                st.write(f"~~{text_tampil}~~ (Selesai)")
            elif index == current_step:
                st.info(f"👉 **{text_tampil}**")
            else:
                st.write(f"⚪ {text_tampil}")
                
    if st.button("🔄 Cek Update Status Terbaru"):
        st.rerun()
    
    st.divider()
    if st.button("🔄 Kembali ke Halaman Utama (Pesan Baru)"):
        st.session_state.keranjang = {}
        st.session_state.catatan_pesanan = ""
        st.session_state.halaman = "katalog"
        st.rerun()
