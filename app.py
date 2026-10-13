import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình hiển thị trang web rộng rãi
st.set_page_config(page_title="Quản Lý Điểm Sinh Viên", layout="wide")

# YÊU CẦU 1 & 4: Hiển thị tiêu đề chuẩn xác theo đề bài
st.title("QUẢN LÝ ĐIỂM SINH VIÊN-")

# ==========================================
# 1. Khởi tạo DataFrame chứa thông tin 10 sinh viên
# ==========================================
data = {
    'Họ tên': [
        'Nguyễn Văn A', 'Trần Thị B', 'Lê Hoàng C', 'Phạm Minh D', 'Vũ Thị E',
        'Hoàng Văn F', 'Đỗ Thúy G', 'Bùi Xuân H', 'Ngô Quốc I', 'Phan Văn K'
    ],
    'Chuyên cần': [9.0, 8.5, 7.0, 10.0, 6.5, 8.0, 9.5, 5.0, 7.5, 8.8],
    'Giữa kỳ': [8.0, 7.5, 6.0, 9.0, 5.5, 7.0, 8.5, 4.0, 6.5, 8.0],
    'Cuối kỳ': [8.5, 8.0, 6.5, 9.5, 6.0, 7.5, 9.0, 4.5, 7.0, 8.5]
}
df = pd.DataFrame(data)

# ==========================================
# 2. Tính điểm tổng kết (20% CC + 30% GK + 50% CK)
# ==========================================
df['Tổng kết'] = (df['Chuyên cần'] * 0.2) + (df['Giữa kỳ'] * 0.3) + (df['Cuối kỳ'] * 0.5)
df['Tổng kết'] = df['Tổng kết'].round(2)

# ==========================================
# 3. Xếp loại sinh viên theo quy định
# ==========================================
def phan_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(phan_loai)

# ==========================================
# 4. Hiển thị bảng điểm của 10 sinh viên
# ==========================================
st.subheader("📋 Bảng điểm của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# ==========================================
# 5. Các thông tin thống kê theo yêu cầu đề bài
# ==========================================
st.subheader("📊 Thống kê kết quả học tập")

# Tính toán các giá trị thống kê
diem_tb_lop = df['Tổng kết'].mean()
sv_cao_nhat = df.loc[df['Tổng kết'].idxmax()]
sv_thap_nhat = df.loc[df['Tổng kết'].idxmin()]
so_sv_dat = len(df[df['Tổng kết'] >= 5.0])

# Hiển thị ra giao diện bằng cấu trúc cột đẹp mắt
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Điểm trung bình của lớp:", f"{diem_tb_lop:.2f}")
    st.metric("Số sinh viên đạt (Điểm TK ≥ 5):", f"{so_sv_dat} sinh viên")

with col2:
    st.info(f"🏆 **Sinh viên có điểm tổng kết cao nhất:**\n\n* **Họ tên:** {sv_cao_nhat['Họ tên']}\n* **Điểm:** {sv_cao_nhat['Tổng kết']} ({sv_cao_nhat['Xếp loại']})")

with col3:
    st.warning(f"📉 **Sinh viên có điểm tổng kết thấp nhất:**\n\n* **Họ tên:** {sv_thap_nhat['Họ tên']}\n* **Điểm:** {sv_thap_nhat['Tổng kết']} ({sv_thap_nhat['Xếp loại']})")

# ==========================================
# 6. Tạo danh sách xổ xuống (Selectbox) tra cứu
# ==========================================
st.subheader("🔍 Tra cứu thông tin chi tiết sinh viên")
sv_selected = st.selectbox("Chọn một sinh viên từ danh sách:", df['Họ tên'])

# Khi chọn sinh viên, hiển thị đầy đủ các cột điểm theo yêu cầu
if sv_selected:
    sv_info = df[df['Họ tên'] == sv_selected].iloc[0]
    
    # Tạo 5 ô hiển thị thông tin nằm ngang tương ứng 5 loại điểm/xếp loại
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Chuyên cần", f"{sv_info['Chuyên cần']:.1f}")
    c2.metric("Giữa kỳ", f"{sv_info['Giữa kỳ']:.1f}")
    c3.metric("Cuối kỳ", f"{sv_info['Cuối kỳ']:.1f}")
    c4.metric("Điểm tổng kết", f"{sv_info['Tổng kết']:.2f}")
    c5.metric("Xếp loại học lực", sv_info['Xếp loại'])

# ==========================================
# 7. Trực quan hóa dữ liệu (Biểu đồ cột)
# ==========================================
st.subheader("📈 Biểu đồ cột điểm tổng kết của 10 sinh viên")

fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(df['Họ tên'], df['Tổng kết'], color='#3498db', edgecolor='black')

# Thiết lập tiêu đề và các trục điểm đúng mô tả đề bài
ax.set_title("Biểu đồ điểm tổng kết của 10 sinh viên trong lớp", fontsize=12, fontweight='bold')
ax.set_xlabel("Tên sinh viên", fontsize=10)
ax.set_ylabel("Thang điểm tổng kết", fontsize=10)
ax.set_ylim(0, 11)
plt.xticks(rotation=30, ha='right')

# Hiển thị số điểm chính xác lên đầu mỗi cột điểm cho trực quan
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, f"{yval:.2f}", ha='center', va='bottom', fontsize=8)

# Đẩy biểu đồ lên giao diện trang Web
st.pyplot(fig)

# ==========================================
# 8. Hiển thị họ tên & MSSV cuối trang (Chữ nhỏ)
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: gray; font-style: italic;'>"
    "Ứng dụng được tạo bởi: <b>[Điền Họ Tên Bạn Vào Đây]</b> - MSSV: <b>[Điền MSSV Bạn Vào Đây]</b>"
    "</p>", 
    unsafe_allow_html=True
)
