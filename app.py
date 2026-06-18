from datetime import datetime
import streamlit as st
from css import inject_custom_css
from utils import get_menu
from ambil import render_halaman_ambil
from antar import render_halaman_antar
from bayar import render_halaman_bayar
from status import render_halaman_monitoring

st.set_page_config(page_title=" Warteg Digital Order", layout="centered")
inject_custom_css()

jam_sekarang = datetime.now().hour
if jam_sekarang >= 22:
    st.warning("🌙 Mohon maaf, warteg kami sudah tutup.")
    st.error("Kami melayani pesanan hingga pukul 22.00 WIB. Silakan datang kembali esok hari!")
    st.stop()

excel_menu = get_menu()
if excel_menu is not None:
    MENU_ITEMS = excel_menu
else:
    st.warning("⚠️ Gagal memuat database Excel.")
    st.stop()


# 3. INISIALISASI SESSION STATE
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}
if "halaman" not in st.session_state:
    st.session_state.halaman = "katalog" 
if "catatan_pesanan" not in st.session_state:
    st.session_state.catatan_pesanan = ""
if "status_pesanan" not in st.session_state:
    st.session_state.status_pesanan = 0
if "jenis_layanan" not in st.session_state:
    st.session_state.jenis_layanan = "ambil"

if st.session_state.halaman == "katalog":
    st.title("Warteg Digital Order")
    st.write("Pilih menu favoritmu, dan pesan langsung secara online tanpa perlu mengantre!")
    st.divider()

    cols = st.columns(3)
    for i, (menu_id, detail) in enumerate(MENU_ITEMS.items()):
        with cols[i % 3]:
            st.image(detail['foto'], use_container_width=True)
            st.markdown(f"<div class='menu-title'>{detail['nama']}</div>", unsafe_allow_html=True)
            
            col_harga, col_ikon = st.columns([3, 1])
            with col_harga:
                st.markdown(f"<div class='price-container'><p class='price-tag'>Rp {detail['harga']:,}</p></div>", unsafe_allow_html=True)
                
            with col_ikon:
                with st.popover("🔍", use_container_width=True):
                    st.subheader(detail['nama'])
                    st.image(detail['foto'], caption=detail['nama'], use_container_width=True)
                    st.write("**Deskripsi Lengkap:**")
                    st.info(detail['deskripsi'])
            
            if st.button(f"➕ Tambahkan", key=f"btn_{menu_id}", use_container_width=True):
                if menu_id in st.session_state.keranjang:
                    st.session_state.keranjang[menu_id] += 1
                else:
                    st.session_state.keranjang[menu_id] = 1
                st.toast(f"Berhasil menambahkan {detail['nama']}!", icon="🍽️")

    st.divider()
    st.header("Piring Pesanan Anda")

    if not st.session_state.keranjang:
        st.info("Piring Pesanan Anda masih kosong. Silakan pilih menu di atas!")
    else:
        total_belanja = 0
        with st.container(border=True):
            for menu_id, jumlah in list(st.session_state.keranjang.items()):
                if jumlah > 0:
                    nama_menu = MENU_ITEMS[menu_id]["nama"]
                    harga_satuan = MENU_ITEMS[menu_id]["harga"]
                    subtotal = jumlah * harga_satuan
                    total_belanja += subtotal
                    
                    col_info, col_kontrol = st.columns([2, 1])
                    with col_info:
                        st.write(f"**{nama_menu}**")
                        st.caption(f"Rp {harga_satuan:,}  |  Sub: **Rp {subtotal:,}**")
                        
                    with col_kontrol:
                        new_qty = st.number_input(
                            "Qty", min_value=0, max_value=99, value=jumlah, 
                            key=f"qty_{menu_id}", label_visibility="collapsed"
                        )
                        if new_qty != jumlah:
                            if new_qty == 0:
                                del st.session_state.keranjang[menu_id]
                            else:
                                st.session_state.keranjang[menu_id] = new_qty
                            st.rerun()
                            
        st.divider()
        col_total_label, col_total_val = st.columns([2, 1])
        with col_total_label:
             st.subheader("Total Pembayaran:")
        with col_total_val:
             st.subheader(f"Rp {total_belanja:,}")
             
        if st.button("Kosongkan Piring Pesanan", type="secondary", use_container_width=True):
            st.session_state.keranjang = {}
            st.rerun()

        st.write("---")
        st.session_state.catatan_pesanan = st.text_area(
            "📝 Pesan Tambahan untuk Outlet:", value=st.session_state.catatan_pesanan,
            placeholder="Contoh: Es tehnya yang manis ya..."
        )

        st.write("### Pilih Metode Pengambilan:")
        col_antar, col_ambil = st.columns(2)
        with col_antar:
            if st.button("🛵 Diantar ke Lokasi", type="primary", use_container_width=True):
                st.session_state.halaman = "antar"
                st.rerun()
        with col_ambil:
            if st.button("🛍️ Ambil di Warteg", type="primary", use_container_width=True):
                st.session_state.halaman = "ambil"
                st.rerun()

elif st.session_state.halaman == "ambil":
    render_halaman_ambil(MENU_ITEMS)

elif st.session_state.halaman == "antar":
    render_halaman_antar(MENU_ITEMS)

elif st.session_state.halaman == "bayar":
    render_halaman_bayar()

elif st.session_state.halaman == "monitoring":
    render_halaman_monitoring(MENU_ITEMS)