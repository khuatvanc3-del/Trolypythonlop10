import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Trợ lý Tin học 10",
    page_icon="🎓",
    layout="wide"
)

# --- 2. KẾT NỐI AI (BẢO MẬT) ---
try:
    my_api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Chưa tìm thấy chìa khóa API! Vui lòng cài đặt trong Settings > Secrets.")
    st.stop()

genai.configure(api_key=my_api_key)

# --- 3. KHO DỮ LIỆU BÀI HỌC (Sách Kết nối tri thức) ---
bai_hoc_content = {
    "--- Chọn bài học lý thuyết ---": "👋 Chào mừng em! Hãy chọn một bài học ở menu bên trái để ôn tập kiến thức nhé.",

    "Bài 16: Ngôn ngữ lập trình bậc cao": """
    ### 1. Khái niệm
    - Ngôn ngữ lập trình bậc cao có câu lệnh gần với ngôn ngữ tự nhiên, giúp con người dễ đọc, dễ hiểu (VD: Python, C++, Java).
    ### 2. Python là gì?
    - Là ngôn ngữ thông dịch (Interpreted).
    - Môi trường lập trình: Gõ lệnh trực tiếp (Interactive) hoặc Soạn thảo (Script).
    - Cú pháp đơn giản, bắt buộc thụt đầu dòng.
    """,

    "Bài 17: Biến và lệnh gán": """
    ### 1. Biến (Variable)
    - Tên biến: Bắt đầu bằng chữ/gạch dưới, không bắt đầu bằng số.
    ### 2. Lệnh gán
    - Cú pháp: `<tên biến> = <giá trị>`
    - VD: `a = 5`, `ten = "Nam"`
    """,

    "Bài 18: Các lệnh vào ra đơn giản": """
    ### 1. Xuất (Print): `print("Hello")`
    ### 2. Nhập (Input): 
    - `ten = input("Nhập tên: ")` (Nhập xâu)
    - `n = int(input("Nhập số: "))` (Nhập số nguyên)
    """,

    "Bài 19: Câu lệnh rẽ nhánh If": """
    ### Cấu trúc rẽ nhánh
    **1. Dạng thiếu:** `if <điều kiện>: <câu lệnh>`
    **2. Dạng đủ:**
    ```python
    if <điều kiện>:
        <câu lệnh 1>
    else:
        <câu lệnh 2>
    ```
    """,

    "Bài 20: Câu lệnh lặp For": """
    ### Lặp với số lần biết trước
    - Cú pháp: `for <biến> in range(stop):`
    - Hàm `range(n)`: Tạo dãy từ 0 đến n-1.
    """,

    "Bài 21: Câu lệnh lặp While": """
    ### Lặp với số lần chưa biết trước
    - Cú pháp: `while <điều kiện>: <khối lệnh>`
    - Vòng lặp chạy khi điều kiện còn True.
    """,

    "Bài 22: Kiểu dữ liệu danh sách (List)": """
    ### List
    - Khởi tạo: `A = [1, 3, 5]`
    - Truy cập: `A[0]` (đầu), `A[-1]` (cuối).
    - Độ dài: `len(A)`
    """,

    "Bài 23: Một số lệnh làm việc với List": """
    - `A.append(x)`: Thêm vào cuối.
    - `A.insert(k, x)`: Chèn vào vị trí k.
    - `A.remove(x)`: Xóa phần tử x.
    - `del A[k]`: Xóa tại chỉ số k.
    """,

    "Bài 24: Xâu kí tự (String)": """
    - Xâu đặt trong nháy đơn `' '` hoặc kép `" "`.
    - Truy cập ký tự giống List.
    - Ghép xâu: `S1 + S2`.
    """,

    "Bài 25: Một số lệnh làm việc với Xâu": """
    - `S.find(sub)`: Tìm vị trí.
    - `S.split()`: Tách xâu thành List.
    - `S.replace(old, new)`: Thay thế.
    """,

    "Bài 26: Hàm trong Python": """
    - Cú pháp: `def ten_ham(tham_so):`
    - Giúp chương trình gọn, tránh lặp code.
    """,

    "Bài 27: Tham số của hàm": """
    - Tham số: Biến trong định nghĩa hàm.
    - Đối số: Giá trị truyền vào khi gọi hàm.
    """,

    "Bài 28: Phạm vi của biến": """
    - Biến cục bộ: Chỉ dùng trong hàm.
    - Biến toàn cục: Dùng trong cả chương trình (dùng từ khóa `global` để sửa).
    """,

    "Bài 29: Nhận biết lỗi chương trình": """
    1. Lỗi cú pháp (Syntax): Viết sai quy tắc.
    2. Lỗi ngoại lệ (Runtime): Chạy mới lỗi (chia 0).
    3. Lỗi ngữ nghĩa (Logical): Ra kết quả sai.
    """,
    
    "Bài 30: Kiểm thử và gỡ lỗi": """
    - Dùng `print()` để kiểm tra giá trị trung gian.
    - Dùng công cụ Debugger để chạy từng dòng.
    """
}

# --- 4. HÀM XỬ LÝ PDF ---
def get_pdf_text(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- 5. GIAO DIỆN THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=90)
    st.title("📚 Góc học tập")
    st.markdown("---")
    
    # Menu chọn bài học
    st.subheader("1. 📖 Ôn tập Lý thuyết")
    selected_lesson = st.selectbox("Chọn bài học:", list(bai_hoc_content.keys()))
    
    # Nút tải file
    st.markdown("---")
    st.subheader("2. 📂 Tải đề bài (PDF)")
    uploaded_file = st.file_uploader("Tải file bài tập để AI hỗ trợ:", type=['pdf'])
    
    st.markdown("---")
    if st.button("🗑️ Xóa hội thoại", type="primary"):
        st.session_state.chat_session = None
        st.rerun()

# --- 6. GIAO DIỆN CHÍNH ---
st.title("🎓 Trợ lý ảo Tin học 10")

# Hiển thị lý thuyết
if selected_lesson != "--- Chọn bài học lý thuyết ---":
    with st.expander(f"📖 Kiến thức trọng tâm: {selected_lesson}", expanded=True):
        st.markdown(bai_hoc_content[selected_lesson])

# Xử lý PDF
context_pdf = ""
if uploaded_file:
    with st.spinner("Đang đọc tài liệu..."):
        pdf_text = get_pdf_text(uploaded_file)
        context_pdf = f"\n\n[DỮ LIỆU TỪ FILE PDF]:\n{pdf_text}\n"
    st.success(f"✅ Đã đọc file: {uploaded_file.name}. Em hãy đặt câu hỏi nhé!")

# Cấu hình "Não bộ" AI
system_instruction = """
Bạn là Trợ lý ảo dạy Tin học 10 (Sách Kết nối tri thức).
Nhiệm vụ:
1. Giải thích kiến thức Python dễ hiểu, thân thiện.
2. Nếu có [DỮ LIỆU TỪ FILE PDF], hãy dùng nó để trả lời.
3. QUAN TRỌNG: KHÔNG giải bài tập hộ (chỉ gợi ý thuật toán, input/output).
"""
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# Khởi tạo chat
if "chat_session" not in st.session_state or st.session_state.chat_session is None:
    st.session_state.chat_session = model.start_chat(history=[])

# Hiển thị lịch sử
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    avatar = "🧑‍🎓" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.parts[0].text)

# Xử lý câu hỏi
user_input = st.chat_input("Nhập câu hỏi hoặc dán code vào đây...")
if user_input:
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)
    
    full_prompt = user_input + context_pdf # Ghép nội dung PDF vào câu hỏi
    
    with st.spinner("Thầy đang suy nghĩ..."):
        try:
            response = st.session_state.chat_session.send_message(full_prompt)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Lỗi: {e}")
