import sys
import os
import mammoth
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QListWidget, QFileDialog, QMessageBox, QSplitter, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
from docx import Document  # Đọc nội dung file docx

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF - Prompt - DOCX Processor")
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        font = QFont("Arial", 10)

        # (1) QHBoxLayout1 - Đường dẫn PDF
        self.pdf_label = QLabel("Chưa chọn file PDF")
        self.pdf_label.setFont(font)
        self.pdf_label.setFixedHeight(30)
        self.pdf_label.setStyleSheet("border: 1px solid black; padding: 3px;")
        self.pdf_button = QPushButton("Chọn PDF")
        self.pdf_button.setFixedSize(120, 30)
        self.pdf_button.clicked.connect(self.select_pdf)

        pdf_layout = QHBoxLayout()
        pdf_layout.addWidget(self.pdf_label)
        pdf_layout.addWidget(self.pdf_button)

        # (3) QHBoxLayout2 - Đường dẫn Prompt.txt
        self.prompt_label = QLabel("Chưa chọn file prompt")
        self.prompt_label.setFont(font)
        self.prompt_label.setFixedHeight(30)
        self.prompt_label.setStyleSheet("border: 1px solid black; padding: 3px;")
        self.prompt_button = QPushButton("Chọn Prompt")
        self.prompt_button.setFixedSize(120, 30)
        self.prompt_button.clicked.connect(self.select_prompt)
        self.edit_prompt_button = QPushButton("Sửa Prompt")
        self.edit_prompt_button.setFixedSize(120, 30)
        self.edit_prompt_button.clicked.connect(self.edit_prompt)

        prompt_layout = QHBoxLayout()
        prompt_layout.addWidget(self.prompt_label)
        prompt_layout.addWidget(self.prompt_button)
        prompt_layout.addWidget(self.edit_prompt_button)

        # (6) Button4 - Bắt đầu xử lý
        self.process_button = QPushButton("Bắt đầu xử lý")
        self.process_button.setFont(font)
        self.process_button.setFixedHeight(40)
        self.process_button.clicked.connect(self.process_files)
        self.process_button.setStyleSheet("border: 1px solid black;")
        process_layout = QHBoxLayout()
        process_layout.addWidget(self.process_button)

        # (7) QTextEdit - hiển thị nội dung file docx
        self.docx_viewer = QWebEngineView()
        self.docx_viewer.setFont(font)
        self.docx_viewer.setStyleSheet("border: 1px solid black; padding: 5px;")

        # (8) ListBox1 - danh sách file docx
        self.docx_list = QListWidget()
        self.docx_list.setFont(font)
        self.docx_list.setFixedWidth(220)
        self.docx_list.itemClicked.connect(self.show_selected_docx)

        # Splitter chia (7) và (8)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.docx_viewer)
        splitter.addWidget(self.docx_list)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        # Layout tổng
        main_layout = QVBoxLayout()
        main_layout.addLayout(pdf_layout)
        main_layout.addLayout(prompt_layout)
        main_layout.addLayout(process_layout)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def select_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_label.setText(file_path)

    def select_prompt(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file prompt.txt", "", "Text Files (*.txt)")
        if file_path:
            self.prompt_label.setText(file_path)

    def edit_prompt(self):
        prompt_path = self.prompt_label.text()
        if os.path.isfile(prompt_path):
            os.system(f'notepad "{prompt_path}"')
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn file prompt.txt trước.")

    def process_files(self):
        # Giả lập danh sách file DOCX
        self.docx_list.clear()
        self.generated_files = []
        for fname in self.generated_files:
            # Tạo file giả nếu file chưa tồn tại
            if not os.path.isfile(fname):
                doc = Document()
                doc.add_paragraph(f"Nội dung của {fname}")
                doc.save(fname)
            self.docx_list.addItem(fname)

    def show_selected_docx(self, item):
        file_name = item.text()
        full_path = os.path.abspath(file_name)
        print(f"[DEBUG] Đang mở file: {full_path}")  # Debug

        if not os.path.isfile(full_path):
            self.docx_viewer.setHtml(f"<h3>Lỗi:</h3><p>File không tồn tại: {full_path}</p>")
            return

        try:
            with open(full_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value.strip()
                if html:
                    self.docx_viewer.setHtml(html)
                else:
                    self.docx_viewer.setHtml(f"<p>Không có nội dung trong {file_name}</p>")
        except Exception as e:
            self.docx_viewer.setHtml(f"<h3>Lỗi khi mở {file_name}</h3><p>{str(e)}</p>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
