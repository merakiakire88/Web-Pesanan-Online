import streamlit as st
from datetime import datetime
from utils import simpan_ke_json

def render_halaman_bayar():
    st.title("💳 Metode Pembayaran")
    st.divider()
    
    total_tagihan = st.session_state.get('total_akhir', 0)
    st.metric(label="Total Tagihan Akhir Anda:", value=f"Rp {total_tagihan:,}")
    
    kategori_bayar = st.radio("Pilih Kategori Pembayaran:", ["Tunai (Bayar di Kasir/Kurir)", "Digital (E-Wallet / Transfer)"])
    st.write("---")
    
    if kategori_bayar == "Tunai (Bayar di Kasir/Kurir)":
        st.info("ℹ️ Anda memilih opsi Tunai. Silakan lakukan pembayaran langsung saat menerima pesanan atau di meja kasir.")
        
        if st.button("Selesai & Buat Pesanan", type="primary", use_container_width=True):
            nama_final = st.session_state.get("nama_penerima", "") if st.session_state.jenis_layanan == "antar" else st.session_state.get("nama_pelanggan", "")
            no_telp_final = st.session_state.get("no_telp", "")
            total_final = st.session_state.get("total_akhir", 0)
            waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M")

            data_final = {
                "waktu": waktu_sekarang,
                "nama": nama_final,
                "no_telp": no_telp_final,
                "jenis_layanan": st.session_state.jenis_layanan,
                "metode_pembayaran": kategori_bayar,
                "catatan_khusus": st.session_state.catatan_pesanan,
                "subtotal": st.session_state.get("subtotal", 0),
                "ongkir": st.session_state.get("ongkir", 0),
                "diskon": st.session_state.get("potongan_diskon", 0),
                "total_bayar": total_final,
                "status": "Diterima",
                "detail_item": st.session_state.keranjang
            }
            
            simpan_ke_json(data_final)
            st.toast("Pesanan Berhasil Dibuat!", icon="✅")
            st.session_state.halaman = "monitoring"
            st.rerun()
            
    else:
        metode_digital = st.selectbox(
            "Pilih Metode Pembayaran Digital:",
            ["Transfer Bank (VA)", "DANA", "OVO", "GoPay", "ShopeePay"]
        )
        pin_input = st.text_input("Masukkan PIN Keamanan Anda :", type="password", help="Ketik angka bebas untuk simulasi")
        
        if st.button("💳 Konfirmasi Pembayaran", type="primary", use_container_width=True):
            if pin_input:
                st.success(f"🎉 Pembayaran via {metode_digital} Berhasil Dikonfirmasi!")
                nama_final = st.session_state.get("nama_penerima", "") if st.session_state.jenis_layanan == "antar" else st.session_state.get("nama_pelanggan", "")
                no_telp_final = st.session_state.get("no_telp", "")
                total_final = st.session_state.get("total_akhir", 0)
                waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M")

                data_final = {
                    "waktu": waktu_sekarang,
                    "nama": nama_final,
                    "no_telp": no_telp_final,
                    "jenis_layanan": st.session_state.jenis_layanan,
                    "metode_pembayaran": f"Digital - {metode_digital}", 
                    "catatan_khusus": st.session_state.catatan_pesanan,
                    "subtotal": st.session_state.get("subtotal", 0),
                    "ongkir": st.session_state.get("ongkir", 0),
                    "diskon": st.session_state.get("potongan_diskon", 0),
                    "total_bayar": total_final,
                    "status": "Diterima",
                    "detail_item": st.session_state.keranjang
                }
                
                simpan_ke_json(data_final)
                st.session_state.halaman = "monitoring"
                st.rerun()
            else:
                st.error("⚠️ Harap masukkan PIN Anda terlebih dahulu sebelum membayar.")