import json
from docx import Document
from docx.shared import Inches
from PIL import Image
from io import BytesIO
import requests
import validators
from google import genai
from google.genai import types
from text2Image import generate_image_from_text

# Function to create DOCX file
def create_docx_from_json(json_data, output_file):
    # Initialize a new Document
    doc = Document()
    
    # Parse JSON data
    data = json.loads(json_data)
    
    # Iterate through each question in the JSON data
    for idx, item in enumerate(data, 1):
        # Add question number
        doc.add_paragraph(f"Câu {idx}.")
        
        # Handle image based on "Mô tả ảnh"
        mo_ta_anh = item.get("Mô tả ảnh", "Không có")
        if mo_ta_anh != "Không có":
            try:
                # Check if mo_ta_anh is a valid URL
                if validators.url(mo_ta_anh):
                    # Download image from URL
                    response = requests.get(mo_ta_anh)
                    response.raise_for_status()  # Raise exception for bad status codes
                    image = Image.open(BytesIO(response.content))
                else:
                    # Generate image from text description
                    image = generate_image_from_text(mo_ta_anh)
                
                # Save image temporarily to BytesIO
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                # Add image to document
                doc.add_picture(img_byte_arr, width=Inches(4.0))
            except Exception as e:
                # If image generation or download fails, add placeholder text
                doc.add_paragraph(f"[Không thể tạo hoặc tải ảnh: {str(e)}]")
        
        # Add question content
        noi_dung_cau_hoi = item.get("Nội dung câu hỏi", "")
        doc.add_paragraph(noi_dung_cau_hoi)
        
        # Add a blank line for spacing
        doc.add_paragraph()
    
    # Save the document
    doc.save(output_file)

# JSON data provided by the user
with open(r'C:\Users\Admin\Desktop\Maru\GenQues\result.json', 'r', encoding='utf-8') as f:
    json_data = f.read()

# Call the function to create the DOCX file
create_docx_from_json(json_data, "questions.docx")