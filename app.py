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

    "Bài 16: Ngôn ngữ lập trình bậc cao và Python": """
    - **Ngôn ngữ lập trình bậc cao:** Gần với ngôn ngữ tự nhiên, độc lập với phần cứng, giúp lập trình viên dễ đọc, dễ hiểu và dễ bảo trì.
    - **Môi trường Python:** Phần mềm thân thiện, hỗ trợ soạn thảo và gỡ lỗi chương trình. 
    - **Hai chế độ làm việc:** + *Chế độ gõ lệnh trực tiếp (>>>):* Dùng để tính toán nhanh, thử nghiệm từng dòng lệnh.
      + *Chế độ soạn thảo:* Mở cửa sổ mới (File -> New File) để viết, lưu và chạy một chương trình hoàn chỉnh.
    - **Đặc điểm:** Python tự động nhận biết kiểu dữ liệu và phân biệt chữ hoa/chữ thường (ví dụ: `A` khác `a`).
    """,

    "Bài 17: Biến và lệnh gán": """
    - **Lệnh gán:** `tên_biến = giá_trị`. Cú pháp này vừa tạo ra biến, vừa gán giá trị cho nó.
    - **Quy tắc đặt tên biến:** + Chỉ gồm chữ cái tiếng Anh, chữ số và dấu gạch dưới `_`.
      + KHÔNG bắt đầu bằng chữ số. KHÔNG chứa khoảng trắng.
      + KHÔNG trùng với các từ khóa của Python (như `if`, `for`, `while`...).
    - **Các kiểu dữ liệu cơ bản:** Số nguyên (`int`), Số thực (`float`), Xâu kí tự (`str`), Lôgic (`bool`).
    """,

    "Bài 18: Các lệnh vào ra đơn giản": """
    - **Lệnh xuất dữ liệu:** `print(giá_trị_1, giá_trị_2, ...)` in các giá trị ra màn hình, mặc định cách nhau bằng một khoảng trắng.
    - **Lệnh nhập dữ liệu:** `input("Câu thông báo:")` tạm dừng chương trình để người dùng nhập dữ liệu từ bàn phím. 
    - **Ép kiểu dữ liệu:** Vì hàm `input()` luôn trả về dữ liệu ở dạng xâu (`str`), nên để nhập số, ta phải ép kiểu:
      + Nhập số nguyên: `n = int(input())`
      + Nhập số thực: `x = float(input())`
    """,

    "Bài 19: Câu lệnh rẽ nhánh If": """
    - **Biểu thức lôgic:** Trả về giá trị `True` (Đúng) hoặc `False` (Sai). Thường dùng phép toán so sánh (`<, >, ==, !=, <=, >=`) và phép toán lôgic (`and, or, not`).
    - **Cú pháp dạng thiếu:** `if <điều kiện>:`
      `    <khối lệnh>`
    - **Cú pháp dạng đủ:**
      `if <điều kiện>:`
      `    <khối lệnh 1>`
      `else:`
      `    <khối lệnh 2>`
    - *Lưu ý cực kỳ quan trọng:* Các lệnh trong cùng một khối phải được **thụt lề (indentation)** thẳng hàng với nhau.
    """,

    "Bài 20: Câu lệnh lặp For": """
    - **Mục đích:** Sử dụng vòng lặp `for` khi ta đã biết trước số lần lặp.
    - **Hàm range():** `range(start, stop, step)` tạo dãy số nguyên từ `start` đến `stop - 1`, với khoảng cách bước nhảy là `step`. (Mặc định start=0, step=1).
    - **Cú pháp lặp với vùng giá trị:** `for i in range(n):` (Vòng lặp sẽ chạy n lần, biến i đi từ 0 đến n-1).
    - **Cú pháp duyệt phần tử (danh sách/xâu):** `for char in "Python":` (Duyệt qua từng kí tự trong xâu).
    """,

    "Bài 21: Câu lệnh lặp While": """
    - **Mục đích:** Sử dụng khi chưa biết trước số lần lặp, vòng lặp phụ thuộc vào một điều kiện.
    - **Cú pháp:**
      `while <điều kiện>:`
      `    <khối lệnh>`
    - **Hoạt động:** Kiểm tra điều kiện, nếu `True` thì thực hiện khối lệnh, rồi quay lại kiểm tra. Nếu `False` thì thoát vòng lặp ngay lập tức.
    - *Lưu ý:* Bên trong khối lệnh bắt buộc phải có câu lệnh làm thay đổi giá trị của điều kiện để tránh gây ra **vòng lặp vô hạn**.
    """,

    "Bài 22: Kiểu dữ liệu danh sách (List)": """
    - **Khái niệm:** Là tập hợp các phần tử có thứ tự, được đặt trong cặp ngoặc vuông `[]`, ngăn cách nhau bởi dấu phẩy. VD: `A = [1, 2, "Python"]`.
    - **Chỉ số (Index):** Bắt đầu từ `0` (nếu đếm từ trái qua phải) hoặc `-1` (nếu đếm ngược từ phải qua trái).
    - **Truy cập:** Lấy phần tử thông qua chỉ số, ví dụ `A[0]`.
    - **Sửa phần tử:** Có thể thay đổi giá trị trực tiếp bằng lệnh gán `A[i] = giá_trị_mới`.
    - **Duyệt danh sách:** Lệnh `for x in A:` (lấy từng giá trị) hoặc `for i in range(len(A)):` (lấy theo vị trí chỉ số).
    """,

    "Bài 23: Một số lệnh làm việc với dữ liệu danh sách": """
    - **Thêm phần tử:** + `A.append(x)`: Thêm phần tử x vào cuối danh sách.
      + `A.insert(i, x)`: Chèn phần tử x vào vị trí chỉ số i.
    - **Xóa phần tử:**
      + `A.pop(i)`: Xóa và trả về phần tử nằm ở vị trí i.
      + `A.remove(x)`: Xóa phần tử đầu tiên có giá trị bằng x.
      + `A.clear()`: Xóa toàn bộ phần tử (biến thành danh sách rỗng).
    - **Phép toán:** Dùng `in` hoặc `not in` để kiểm tra phần tử có nằm trong danh sách không. Ghép hai danh sách bằng dấu `+`.
    """,

    "Bài 24: Xâu kí tự (String)": """
    - **Khái niệm:** Là dãy các kí tự nằm trong cặp nháy đơn `' '` hoặc nháy kép `" "`. 
    - **Tính bất biến:** KHÔNG thể thay đổi từng kí tự bên trong xâu (VD: `S[0] = "a"` sẽ báo lỗi). Chỉ có thể tạo ra xâu mới.
    - **Cắt xâu (Slicing):** `S[start:stop]` lấy xâu con từ chỉ số `start` đến `stop-1`.
    - **Phép toán trên xâu:**
      + `S1 + S2`: Nối hai xâu lại với nhau.
      + `S * n`: Lặp lại xâu S n lần.
    """,

    "Bài 25: Một số lệnh làm việc với xâu kí tự": """
    - **Tìm kiếm:** `S.find(sub)` trả về vị trí xuất hiện đầu tiên của xâu con `sub` trong S. Nếu không tìm thấy, hệ thống trả về `-1`.
    - **Thay thế:** `S.replace(s1, s2)` thay thế tất cả các xâu `s1` thành `s2` trong S.
    - **Tách xâu:** `S.split(kí_tự_phân_cách)` cắt xâu gốc thành một **danh sách** các từ (mặc định phân cách bằng khoảng trắng).
    - **Nối xâu:** `kí_tự_nối.join(danh_sách)` dùng để nối các phần tử của một danh sách thành một xâu duy nhất.
    """,

    "Bài 26: Hàm trong Python": """
    - **Khái niệm:** Là đoạn chương trình thực hiện một công việc cụ thể, có thể tái sử dụng nhiều lần để giúp code gọn gàng, dễ gỡ lỗi.
    - **Cú pháp định nghĩa:**
      `def tên_hàm(tham_số):`
      `    <khối lệnh>`
      `    return <giá_trị>`
    - **Gọi hàm:** `tên_hàm(đối_số_truyền_vào)`. Lệnh `return` kết thúc quá trình chạy hàm và trả kết quả về nơi vừa gọi nó.
    """,

    "Bài 27: Tham số của hàm": """
    - **Tham số (Parameter):** Là các biến được khai báo bên trong ngoặc tròn `()` khi định nghĩa hàm.
    - **Đối số (Argument):** Là giá trị thực tế truyền vào cho hàm khi tiến hành gọi hàm trong chương trình chính.
    - Hàm có thể **không có tham số**, có **1 tham số** hoặc **nhiều tham số** (phân cách bằng dấu phẩy).
    - Khi gọi hàm, các đối số được truyền lần lượt cho các tham số theo đúng thứ tự tương ứng.
    """,

    "Bài 28: Phạm vi của biến": """
    - **Biến cục bộ (Local):** Biến được khai báo bên trong một hàm. Chỉ có tác dụng và tồn tại bên trong hàm đó. Khi hàm kết thúc, biến bị xóa khỏi bộ nhớ.
    - **Biến toàn cục (Global):** Biến được khai báo bên ngoài mọi hàm. Có tác dụng ở mọi nơi trong chương trình.
    - **Từ khóa global:** Sử dụng bên trong hàm khi ta muốn cấp quyền cho hàm đó được phép thay đổi trực tiếp giá trị của một biến toàn cục.
    """,

    "Bài 29: Nhận biết lỗi chương trình": """
    - **Lỗi cú pháp (Syntax Error):** Viết sai cấu trúc ngữ pháp của Python (VD: thiếu dấu `:`, sai thụt lề, viết sai tên lệnh). Phần mềm sẽ báo lỗi ngay lập tức, chương trình không thể chạy.
    - **Lỗi ngoại lệ (Exception / Runtime Error):** Cú pháp đúng nhưng khi chạy gặp tình huống không hợp lệ (VD: chia cho 0 `ZeroDivisionError`, truy cập chỉ số vượt quá mảng `IndexError`, sai kiểu dữ liệu `TypeError`).
    - **Lỗi ngữ nghĩa (Logic Error):** Chương trình chạy bình thường, không báo thông báo lỗi, nhưng kết quả tính toán cuối cùng bị sai so với yêu cầu bài toán.
    """,

    "Bài 30: Kiểm thử và gỡ lỗi chương trình": """
    - **Kiểm thử (Testing):** Kỹ thuật chạy thử chương trình với nhiều bộ dữ liệu (Test case) khác nhau để đối chiếu kết quả thực tế với kết quả dự kiến. Cần đặc biệt chú ý test các trường hợp biên, trường hợp ngoại lệ.
    - **Gỡ lỗi (Debugging):** Quá trình tìm và sửa lỗi. 
      + *Thủ công:* Thêm các lệnh `print()` trung gian để xem giá trị biến đang thay đổi như thế nào.
      + *Dùng công cụ:* Sử dụng chức năng Debug của các phần mềm (như Thonny, VS Code) để chạy chậm từng dòng lệnh (Step into/Step over).
    """,

    "Bài 31: Thực hành viết chương trình đơn giản": """
    - **Quy trình giải quyết bài toán:** 1. Phân tích bài toán (Xác định Input đầu vào / Output đầu ra).
      2. Thiết kế thuật toán (Xây dựng từng bước xử lý logic).
      3. Viết mã chương trình Python.
      4. Kiểm thử và gỡ lỗi.
    - **Trọng tâm:** Kết hợp linh hoạt các cấu trúc điều khiển (if, for, while), kiểu dữ liệu (list, string) và hàm (def) để giải quyết bài toán.
    """,

    "Bài 32: Ôn tập lập trình Python": """
    - **Trọng tâm ôn tập học kỳ:** Hệ thống hóa lại toàn bộ kiến thức lập trình Python lớp 10:
      + Kiểu dữ liệu: int, float, str, bool, list.
      + Cấu trúc điều khiển: Lệnh rẽ nhánh (if - else), Vòng lặp (for, while).
      + Chương trình con: Cách viết hàm, tham số và giá trị trả về.
      + Kỹ năng sửa lỗi: Phát hiện lỗi cú pháp và lỗi logic để chuẩn bị tốt cho các bài kiểm tra thực hành cuối kỳ.
    """
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
st.title("🐍 Trợ lý ảo Tin học 10")

# 6. Khu vực hiển thị tin nhắn chào mừng (chat session)
# Sử dụng st.chat_message("assistant") để hiện tin nhắn chào mừng
with st.chat_message("assistant"):
    st.write("Chào bạn! Mình là thầy/cô AI chuyên về Python 10. Hãy gửi ảnh, file PDF hoặc code để mình giúp nhé! 👋")
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
# Cấu hình AI
system_instruction = """
Bạn là Trợ lý ảo dạy Tin học 10. Nhiệm vụ:
1. Nếu người dùng gửi ẢNH: Hãy phân tích kỹ ảnh (đó có thể là ảnh chụp đoạn code lỗi, hoặc ảnh chụp đề bài tập).
2. Nếu là ảnh lỗi code: Hãy chỉ ra dòng lỗi, giải thích nguyên nhân và cách sửa.
3. Nếu là bài tập tự luận: Hãy trích xuất nội dung đề và gợi ý hướng giải (KHÔNG giải chi tiết ngay).
4. Nếu là câu hỏi TRẮC NGHIỆM: Hãy đưa ra đáp án chính xác nhất, sau đó giải thích chi tiết lý do tại sao lại chọn đáp án đó (và giải thích ngắn gọn tại sao các phương án khác sai nếu cần).
5. Luôn thân thiện, sư phạm.
"""
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)

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








