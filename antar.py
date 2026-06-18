import streamlit as st
from utils import get_kecamatan, hitung_estimasi_jarak

def render_halaman_antar(MENU_ITEMS):
    st.title("🛵 Form Pengiriman Pesanan")
    st.write("Silakan lengkapi data pengiriman Anda. Warteg kami berada di **Cempaka Putih, Jakarta Pusat**.")
    st.divider()

    st.subheader("Data Penerima")
    nama_penerima = st.text_input("Nama Lengkap:")
    no_telp = st.text_input("Nomor Telepon / WhatsApp:")
    
    st.divider()
    st.subheader("Alamat Pengiriman")
    
    WILAYAH_LAYANAN = {
        "Jakarta Pusat": "3173",
        "Jakarta Barat": "3174",
        "Jakarta Utara": "3175",
        "Jakarta Selatan": "3171",
        "Jakarta Timur": "3172"
    }
    
    pilihan_kabupaten = st.selectbox("Pilih Kota/Kabupaten:", list(WILAYAH_LAYANAN.keys()))
    kab_id = WILAYAH_LAYANAN[pilihan_kabupaten]
    
    data_kecamatan = get_kecamatan(kab_id)
    
    if data_kecamatan:
        list_nama_kecamatan = [kec['name'] for kec in data_kecamatan]
        pilihan_kecamatan = st.selectbox("Pilih Kecamatan:", list_nama_kecamatan)
        alamat_khusus = st.text_area("Detail Alamat Khusus (Jalan, RT/RW, Patokan):", placeholder="Contoh: Perumahan Anggrek No. 2, cat rumah warna putih")
        
        jarak_km = hitung_estimasi_jarak(kab_id, pilihan_kecamatan)
        TARIF_PER_KM = 500
        ongkir = jarak_km * TARIF_PER_KM
        
        st.divider()
        st.subheader("Ringkasan Pembayaran")
        
        total_belanja = sum([MENU_ITEMS[m_id]["harga"] * qty for m_id, qty in st.session_state.keranjang.items()])
        total_awal = total_belanja + ongkir
        
        kode_input = st.text_input("🎟️ Punya Kode Diskon?", placeholder="Masukkan kode promo di sini...").strip().lower()
        persen_diskon = 0
        if kode_input == "qwerty123":
            persen_diskon = 0.10
            st.success("✅ Kode berhasil diterapkan! Anda mendapat diskon **10%**.")
        elif kode_input == "aswd567":
            persen_diskon = 0.15
            st.success("✅ Kode berhasil diterapkan! Anda mendapat diskon **15%**.")
        elif kode_input != "":
            st.error("❌ Kode diskon tidak valid atau tidak ditemukan.")
            
        potongan_diskon = int(total_awal * persen_diskon)
        total_semua = total_awal - potongan_diskon

        with st.container(border=True):
            col_label1, col_val1 = st.columns([3, 1])
            with col_label1:
                st.write(f"🛍️ **Total Pesanan** ({sum(st.session_state.keranjang.values())} item)")
            with col_val1:
                st.write(f"Rp {total_belanja:,}")
                
            col_label2, col_val2 = st.columns([3, 1])
            with col_label2:
                st.write("🛵 **Ongkos Kirim** (Serpong ➡️ " + pilihan_kecamatan.title() + ")")
            with col_val2:
                st.write(f"Rp {ongkir:,}")
                
            if persen_diskon > 0:
                col_label_disc, col_val_disc = st.columns([3, 1])
                with col_label_disc:
                    st.write(f"🎟️ **Diskon Promo** ({int(persen_diskon * 100)}%)")
                with col_val_disc:
                    st.markdown(f"<span style='color: #ef4444; font-weight: bold;'>- Rp {potongan_diskon:,}</span>", unsafe_allow_html=True)
            
            catatan = st.session_state.catatan_pesanan if st.session_state.catatan_pesanan else "Tidak ada catatan khusus."
            st.caption(f"📝 *Catatan:* {catatan}")
            
            st.divider()
            col_total_label, col_total_val = st.columns([2, 1])
            with col_total_label:
                st.markdown("### Total Akhir:")
            with col_total_val:
                st.markdown(f"### Rp {total_semua:,}")
            
        st.write("---")
        c_back, c_pay = st.columns(2)
        with c_back:
            if st.button("⬅️ Kembali ke Menu", use_container_width=True):
                st.session_state.halaman = "katalog"
                st.rerun()
        with c_pay:
            if nama_penerima and no_telp and alamat_khusus:
                if st.button("💳 Lanjut ke Pembayaran", type="primary", use_container_width=True):
                    st.session_state.nama_penerima = nama_penerima
                    st.session_state.no_telp = no_telp
                    st.session_state.total_akhir = total_semua 
                    st.session_state.jenis_layanan = "antar"
                    st.session_state.subtotal = total_belanja
                    st.session_state.ongkir = ongkir
                    st.session_state.potongan_diskon = potongan_diskon
                    st.session_state.halaman = "bayar" 
                    st.rerun()
            else:
                st.button("💳 Lanjut ke Pembayaran", type="primary", use_container_width=True, disabled=True)
                st.caption("⚠️ Harap lengkapi Nama, No Telp, dan Detail Alamat Khusus.")
    else:
        st.error("Gagal mengambil data wilayah. Periksa koneksi internet Anda.")
