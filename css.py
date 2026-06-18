import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        div[data-testid="stImage"] img {
            height: 180px !important;
            object-fit: cover !important;
            border-radius: 12px;
        }
        .menu-title {
            min-height: 52px;
            font-size: 1.1rem;
            font-weight: bold;
            color: #1e293b;
            margin-top: 10px;
            margin-bottom: 5px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .price-container {
            display: flex;
            align-items: center;
            height: 40px;
        }
        .price-tag {
            color: #f59e0b;
            font-weight: bold;
            font-size: 1.2rem;
            margin: 0;
        }
        div[data-testid="stPopover"] button {
            padding: 4px !important;
            font-size: 1rem !important;
            min-width: 40px !important; 
        }
        </style>
    """, unsafe_allow_html=True)

def generate_struk_html(data_aktif, total_qty, html_items, ongkir_val, diskon_val, subtotal_val, waktu_val, metode_bayar_val):
    html_ongkir = f"<div>Ongkir <span style='float: right;'>Rp {ongkir_val:,}</span></div>" if ongkir_val > 0 else ""
    html_diskon = f"<div>Diskon Promo <span style='float: right; color: red;'>-Rp {diskon_val:,}</span></div>" if diskon_val > 0 else ""
    
    struk_html = f"""
<div style="font-family: 'Courier New', Courier, monospace; background-color: #fdfdfd; padding: 20px; border: 1px dashed #777; border-radius: 8px; color: #333; max-width: 400px; margin: 0 auto 20px auto; font-size: 14px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
    <div style="text-align: center; margin-bottom: 15px;">
        <h3 style="margin: 0; color: #111;">Warteg Ika Sari</h3>
        <small>Cempaka Putih<br>Jakarta Pusat<br>Telp: 0812-3456-7890</small>
    </div>
    
    <div style="border-bottom: 1px dashed #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        Waktu : {waktu_val}<br>
        Nama  : {data_aktif.get('nama', '-')}<br>
        Telp  : {data_aktif.get('no_telp', '-')}<br>
        Tipe  : {data_aktif.get('jenis_layanan', 'ambil').upper()} ({metode_bayar_val.split()[0]})
    </div>
    
    <div style="border-bottom: 1px dashed #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        {html_items}
    </div>
    
    <div style="border-bottom: 1px dashed #ccc; padding-bottom: 10px; margin-bottom: 10px;">
        <div>Subtotal <span style="float: right;">Rp {subtotal_val:,}</span></div>
        {html_ongkir}
        {html_diskon}
        <div style="margin-top: 8px; font-size: 16px;"><strong>TOTAL AKHIR <span style="float: right;">Rp {data_aktif.get('total_bayar', 0):,}</span></strong></div>
    </div>
    
    <div style="text-align: center; margin-top: 15px;">
        <strong>Total Item: {total_qty} pcs</strong><br>
        <small>Terima Kasih Atas Pembelian Anda!</small>
    </div>
</div>
"""
    return struk_html
