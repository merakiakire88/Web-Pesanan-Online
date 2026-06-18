import streamlit as st

def render_halaman_ambil(MENU_ITEMS):
    st.title("🛍️ Ambil Sendiri Warteg")
    st.write("Silakan isi data Anda. Pesanan dapat diambil di Warteg kami (**Kec. Serpong, Kota Tangerang Selatan**) setelah pembayaran dikonfirmasi.")
    st.divider()

    st.subheader("Data Pengambil Pesanan")
    nama_pelanggan = st.text_input("Nama Lengkap:")
    no_telp = st.text_input("Nomor Telepon / WhatsApp:")
    
    st.divider()
    st.subheader("Ringkasan Pembayaran")
    total_belanja = sum([MENU_ITEMS[m_id]["harga"] * qty for m_id, qty in st.session_state.keranjang.items()])
    
    kode_input = st.text_input("🎟️ Punya Kode Diskon?", key="diskon_ambil", placeholder="Masukkan kode promo di sini...").strip().lower()
    
    persen_diskon = 0
    if kode_input == "qwerty123":
        persen_diskon = 0.10
        st.success("✅ Kode berhasil diterapkan! Anda mendapat diskon **10%**.")
    elif kode_input == "aswd567":
        persen_diskon = 0.15
        st.success("✅ Kode berhasil diterapkan! Anda mendapat diskon **15%**.")
    elif kode_input != "":
        st.error("❌ Kode diskon tidak valid atau tidak ditemukan.")
        
    potongan_diskon = int(total_belanja * persen_diskon)
    total_semua = total_belanja - potongan_diskon

    with st.container(border=True):
        col_label1, col_val1 = st.columns([3, 1])
        with col_label1:
            st.write(f"🛍️ **Total Pesanan** ({sum(st.session_state.keranjang.values())} item)")
        with col_val1:
            st.write(f"Rp {total_belanja:,}")
            
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
        if st.button("⬅️ Kembali ke Menu", key="btn_back_ambil", use_container_width=True):
            st.session_state.halaman = "katalog"
            st.rerun()
            
    with c_pay:
        if nama_pelanggan and no_telp:
            if st.button("💳 Lanjut ke Pembayaran", key="btn_pay_ambil", type="primary", use_container_width=True):
                st.session_state.nama_pelanggan = nama_pelanggan
                st.session_state.no_telp = no_telp
                st.session_state.total_akhir = total_semua
                st.session_state.jenis_layanan = "ambil"
                st.session_state.subtotal = total_belanja
                st.session_state.ongkir = 0
                st.session_state.potongan_diskon = potongan_diskon
                st.session_state.halaman = "bayar"
                st.rerun()
        else:
            st.button("💳 Lanjut ke Pembayaran", key="btn_pay_ambil_disabled", type="primary", use_container_width=True, disabled=True)
            st.caption("⚠️ Harap lengkapi Nama dan Nomor Telepon Anda.")