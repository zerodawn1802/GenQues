import json
import re

# Biểu thức chính quy để khớp chuỗi "\nLời giải:\n<4 ký tự 0 hoặc 1>\n####"
pattern = r'\nLời giải:\n[01]{4}\n####'

# Đọc file JSON
input_file = r"C:\Users\Admin\Desktop\Maru\GenQues\result.json"  # Thay bằng tên file JSON của bạn
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Phân loại câu hỏi
dungsai = []
tracnghiem = []

for item in data:
    try:
        # Kiểm tra trường "Nội dung câu hỏi"
        if "Nội dung câu hỏi" in item and re.search(pattern, item["Nội dung câu hỏi"]):
            dungsai.append(item)
        else:
            tracnghiem.append(item)
    except Exception as e:
        print(f"Lỗi khi xử lý phần tử: {e}")

# Ghi vào file dungsai.json
with open("dungsai.json", "w", encoding="utf-8") as f:
    json.dump(dungsai, f, ensure_ascii=False, indent=4)

# Ghi vào file tracnghiem.json
with open("tracnghiem.json", "w", encoding="utf-8") as f:
    json.dump(tracnghiem, f, ensure_ascii=False, indent=4)

print("Đã phân loại và lưu vào dungsai.json và tracnghiem.json")