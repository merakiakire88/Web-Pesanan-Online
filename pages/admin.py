import streamlit as st
import json
import os

st.set_page_config(page_title="Dashboard Admin - Cafe Order", layout="wide")

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

st.title("👨‍💻 Dashboard Admin & Dapur")
st.write("Pantau pesanan masuk dan perbarui status pengerjaan secara real-time.")
st.divider()

password_input = st.text_input("Masukkan Password Admin:", type="password")

if password_input == "admin123": # Ganti dengan password pilihanmu
    st.success("Akses Diterima!")
    st.write("### Daftar Pesanan Masuk Saat Ini:")

    if st.button("🔄 Segarkan Data Pesanan Masuk"):
        st.rerun()

    semua_pesanan = baca_pesanan_json()
    pesanan_aktif = []
    pesanan_selesai = []

    for idx, psn in enumerate(semua_pesanan):
        if psn.get("status") == "Selesai":
            pesanan_selesai.append((idx, psn))
        else:
            pesanan_aktif.append((idx, psn))

    tab_aktif, tab_riwayat = st.tabs(["⏳ Antrean Pesanan Aktif", "📜 Riwayat & Pemasukan Hari Ini"])

    with tab_aktif:
        st.subheader(f"🗂️ Total Antrean: {len(pesanan_aktif)} Pesanan")
        
        if not pesanan_aktif:
            st.info("Bersih! Belum ada antrean pesanan aktif saat ini.")
        else:
            for idx, data_aktif in pesanan_aktif:
                with st.container(border=True):
                    col_info, col_aksi = st.columns([2, 1])
                    
                    with col_info:
                        st.markdown(f"### 📋 Pesanan Atas Nama: **{data_aktif['nama']}**")
                        st.write(f"📞 **No Telp:** {data_aktif['no_telp']}")
                        st.write(f"🛵 **Metode:** {data_aktif['jenis_layanan'].upper()}")
                        st.write(f"📝 **Catatan Khusus:** *{data_aktif['catatan_khusus'] if data_aktif['catatan_khusus'] else '-'}*")
                        st.write(f"💰 **Total Transaksi:** Rp {data_aktif['total_bayar']:,}")
                        st.write("---")
                        st.write("**Daftar Menu yang Dipesan (ID & Qty):**")
                        st.json(data_aktif['detail_item'])

                    with col_aksi:
                        st.markdown("### ⚙️ Kendali Status")
                        status_saat_ini = data_aktif['status']
                        
                        if status_saat_ini == "Diterima":
                            st.warning(f"Status: **{status_saat_ini}**")
                        elif status_saat_ini == "Disiapkan":
                            st.info(f"Status: **{status_saat_ini}**")
                        elif status_saat_ini == "Sampai":
                            st.info(f"Status: **{status_saat_ini}**")
                        else:
                            st.info(f"Status: **{status_saat_ini}**")
                        
                        is_tunai = "Tunai" in data_aktif.get('metode_pembayaran', 'Tunai')
                        total_harga = data_aktif.get('total_bayar', 0)

                        if status_saat_ini == "Diterima":
                            if st.button("👨‍🍳 Proses & Siapkan di Dapur", type="primary", use_container_width=True, key=f"btn_proses_{idx}"):
                                update_status_json(idx, "Disiapkan")
                                st.rerun()
                                
                        elif status_saat_ini == "Disiapkan":
                            label_tombol = "🛵 Serahkan ke Kurir (Antar)" if data_aktif['jenis_layanan'] == "antar" else "🛍️ Siap Diambil Customer"
                            status_target = "Diantar" if data_aktif['jenis_layanan'] == "antar" else "Sampai"
                            
                            if st.button(label_tombol, type="primary", use_container_width=True, key=f"btn_siap_{idx}"):
                                update_status_json(idx, status_target)
                                st.rerun()
                        
                        elif status_saat_ini == "Diantar":
                            if st.button("📦 Konfirmasi Kurir Sampai di Tujuan", type="primary", use_container_width=True, key=f"btn_kurir_{idx}"):
                                update_status_json(idx, "Sampai")
                                st.rerun()
                        
                        elif status_saat_ini == "Sampai":
                            tombol_ready = True
                            
                            if is_tunai:
                                st.markdown("---")
                                st.subheader("Kasir untuk Pembayaran Tunai")
                                uang_diterima = st.number_input("Masukkan Uang Diterima (Rp):", min_value=0, value=0, step=1000, key=f"cash_input_{idx}")
                                
                                if uang_diterima > 0:
                                    kembalian = uang_diterima - total_harga
                                    if kembalian < 0:
                                        st.error(f"⚠️ Uang kurang sebesar: Rp {abs(kembalian):,}")
                                        tombol_ready = False
                                    else:
                                        st.success(f"Kembalian: **Rp {kembalian:,}**")
                                else:
                                    tombol_ready = False
                                    st.warning("Masukkan nominal uang yang diterima terlebih dahulu.")

                            if st.button("✅ Tandai Selesai & Tutup Transaksi", type="primary", use_container_width=True, disabled=not tombol_ready, key=f"btn_selesai_{idx}"):
                                update_status_json(idx, "Selesai")
                                st.rerun()

    with tab_riwayat:
        total_pemasukan = sum(data_selesai.get("total_bayar", 0) for _, data_selesai in pesanan_selesai)
        
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric(label="💰 Total Omzet / Pemasukan Hari Ini", value=f"Rp {total_pemasukan:,}")
        with col_metric2:
            st.metric(label="✅ Jumlah Pesanan Selesai", value=f"{len(pesanan_selesai)} Transaksi")
            
        st.write("---")
        st.subheader("📋 Detail Laporan Transaksi Selesai")
        
        if not pesanan_selesai:
            st.info("Belum ada riwayat transaksi yang diselesaikan hari ini.")
        else:
            for _, data_selesai in pesanan_selesai:
                with st.expander(f"🟢 Selesai: {data_selesai['nama']} — (Rp {data_selesai['total_bayar']:,})"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.write(f"📞 **No Telp:** {data_selesai['no_telp']}")
                        st.write(f"🛵 **Layanan:** {data_selesai['jenis_layanan'].upper()}")
                        st.write(f"💳 **Pembayaran:** {data_selesai.get('metode_pembayaran', 'Tunai')}")
                    with col_r2:
                        st.write("**Item Terjual:**")
                        st.json(data_selesai['detail_item'])
else:
    if password_input != "":
        st.error("Password Salah!")
    st.warning("Halaman ini dilindungi. Silakan masukkan password untuk melihat pesanan.")                        