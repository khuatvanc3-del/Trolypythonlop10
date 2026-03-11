import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from PIL import Image # Thư viện xử lý ảnh

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Trợ lý Tin học 10 (Vision Edition)",
    page_icon="👁️",
    layout="wide"
)

# --- 2. KẾT NỐI AI ---
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Chưa tìm thấy chìa khóa API! Vào Settings > Secrets để cài đặt.")
    st.stop()

genai.configure(api_key=my_api_key)

# --- 3. DỮ LIỆU BÀI HỌC (Sách KNTT) ---
bai_hoc_content = {
    "--- Chọn bài học ôn tập ---": "👋 Chào em! Hãy chọn bài học bên trái hoặc tải ảnh bài tập lên để thầy xem nhé.",
    
    "Bài 16: Ngôn ngữ lập trình bậc cao": """
    - **Khái niệm:** Ngôn ngữ gần với ngôn ngữ tự nhiên (Python, C++).
    - **Đặc điểm Python:** Thông dịch, cú pháp trong sáng, phân biệt hoa/thường.
    """,
    "Bài 17: Biến và lệnh gán": """
    - **Biến:** `ten_bien = gia_tri` (VD: `a = 10`).
    - **Quy tắc:** Không bắt đầu bằng số, không chứa ký tự đặc biệt.
    """,
    "Bài 18: Các lệnh vào ra": """
    - **Nhập:** `input()` (luôn trả về xâu). Muốn nhập số: `int(input())`.
    - **Xuất:** `print("Kết quả:", x)`.
    """,
    "Bài 19: Câu lệnh rẽ nhánh If": """
    - **Thiếu:** `if <đk>: <lệnh>`
    - **Đủ:** `if <đk>: <lệnh1> else: <lệnh2>`
    - *Lưu ý: Thụt đầu dòng thẳng hàng.*
    """,
    "Bài 20: Câu lệnh lặp For": """
    - **Cú pháp:** `for i in range(n):` (Chạy từ 0 đến n-1).
    - **Range:** `range(start, stop, step)`.
    """,
    "Bài 21: Câu lệnh lặp While": """
    - **Cú pháp:** `while <điều kiện>: <lệnh>`.
    - Chạy khi điều kiện còn True. Cẩn thận lặp vô hạn!
    """,
    "Bài 22: Kiểu dữ liệu List": """
    - **List:** Dãy phần tử có thứ tự `A = [1, 2, 3]`.
    - Truy cập: `A[0]`, `A[-1]`.
    """,
    # (Thầy/cô có thể thêm các bài tiếp theo tương tự như hướng dẫn trước)
}

# --- 4. HÀM XỬ LÝ (PDF & ẢNH) ---
def get_pdf_text(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- 5. GIAO DIỆN THANH BÊN ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=80)
    st.title("👁️ Python Vision")
    st.caption("Nghe - Đọc - Nhìn")
    st.markdown("---")
    
    # Menu bài học
    st.subheader("1. 📖 Lý thuyết")
    selected_lesson = st.selectbox("Chọn bài:", list(bai_hoc_content.keys()))
    
    st.markdown("---")
    # Khu vực Upload đa năng
    st.subheader("2. 📸 Tải Đề/Ảnh lỗi")
    uploaded_file = st.file_uploader("Thả file PDF hoặc ẢNH vào đây:", type=['pdf', 'png', 'jpg', 'jpeg'])
    
    # Hiển thị ảnh xem trước nếu người dùng tải ảnh
    if uploaded_file is not None:
        if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            st.image(uploaded_file, caption="Ảnh đã tải lên", use_column_width=True)
            st.success("✅ Đã nhận diện ảnh!")
        elif uploaded_file.type == "application/pdf":
            st.success(f"✅ Đã đọc file PDF: {uploaded_file.name}")

    st.markdown("---")
    if st.button("🗑️ Xóa hội thoại", type="primary"):
        st.session_state.chat_session = None
        st.rerun()

# --- 6. GIAO DIỆN CHÍNH ---
st.title("🎓 Trợ lý ảo Tin học 10 (AI Vision)")

# Hiển thị lý thuyết
if selected_lesson != "--- Chọn bài học ôn tập ---":
    with st.expander(f"📖 Kiến thức: {selected_lesson}", expanded=True):
        st.markdown(bai_hoc_content[selected_lesson])

# Xử lý File (Chuẩn bị dữ liệu cho AI)
context_content = None # Biến chứa nội dung file (Text hoặc Ảnh)
file_type_msg = ""

if uploaded_file:
    # Trường hợp 1: Là file PDF -> Chuyển thành văn bản
    if uploaded_file.type == "application/pdf":
        with st.spinner("Đang đọc tài liệu PDF..."):
            pdf_text = get_pdf_text(uploaded_file)
            context_content = f"\n\n[DỮ LIỆU TỪ PDF]:\n{pdf_text}\n"
            file_type_msg = "(đang xem file PDF)"
            
    # Trường hợp 2: Là file ẢNH -> Dùng thư viện PIL mở ảnh
    else:
        try:
            image_data = Image.open(uploaded_file)
            context_content = image_data # Lưu đối tượng ảnh để gửi cho AI
            file_type_msg = "(đang nhìn ảnh bạn gửi)"
        except:
            st.error("Lỗi không đọc được ảnh.")

# Cấu hình AI
system_instruction = """
Bạn là Trợ lý ảo dạy Tin học 10. Nhiệm vụ:
1. Nếu người dùng gửi ẢNH: Hãy phân tích kỹ ảnh (đó có thể là ảnh chụp đoạn code lỗi, hoặc ảnh chụp đề bài tập).
2. Nếu là ảnh lỗi code: Hãy chỉ ra dòng lỗi, giải thích nguyên nhân và cách sửa.
3. Nếu là ảnh đề bài: Hãy trích xuất nội dung đề và gợi ý hướng giải (KHÔNG giải chi tiết ngay).
4. Luôn thân thiện, sư phạm.
"""
model = genai.GenerativeModel('gemini-flash-latest', system_instruction=system_instruction)

# Khởi tạo chat
if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

# Hiển thị lịch sử chat
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "🧑‍🎓" if role == "user" else "🤖"
    
    # Ẩn nội dung ảnh trong lịch sử chat để tránh lỗi hiển thị, chỉ hiện text
    if len(message.parts) > 0 and hasattr(message.parts[0], 'text'):
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.parts[0].text)

# Xử lý nhập liệu
user_input = st.chat_input(f"Hỏi thầy/cô AI {file_type_msg}...")

if user_input:
    # Hiện câu hỏi của học sinh
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)
    
    # Chuẩn bị gói tin gửi cho AI
    message_parts = [user_input] # Luôn có câu hỏi dạng chữ
    
    # Nếu có file (PDF Text hoặc Ảnh Object), thêm vào gói tin
    if context_content:
        # Nếu là Text (từ PDF) thì cộng chuỗi
        if isinstance(context_content, str):
            message_parts[0] = user_input + context_content 
        # Nếu là Ảnh (từ PIL) thì thêm vào danh sách
        else:
            message_parts.append(context_content) 

    with st.spinner("Thầy đang quan sát và suy nghĩ..."):
        try:
            # Gửi đa phương thức (Text + Ảnh)
            response = st.session_state.chat_session.send_message(message_parts)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")


