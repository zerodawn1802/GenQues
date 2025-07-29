from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

def generate_image_from_text(prompt):
    client = genai.Client(api_key="AIzaSyCHEhmMG3Olcb-nw0K6hIn8MF9eFagspQQ")

    contents = (prompt)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            return image