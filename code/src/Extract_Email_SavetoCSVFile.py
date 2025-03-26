import os
import email
import magic
import zipfile
import pandas as pd
import fitz  # PyMuPDF for PDFs
import pytesseract
from PIL import Image
from io import BytesIO
from email import policy
from email.parser import BytesParser
from email.header import decode_header
from bs4 import BeautifulSoup
from docx import Document  # Word document processing
import pandas as pd  # For Excel and CSV files

# Set folders
OUTPUT_CSV = "email_data.csv"
EMAIL_FOLDER = os.getcwd() + "/data"
ATTACHMENT_FOLDER = os.getcwd() + "/data/attachments"
IMAGE_FOLDER = os.getcwd() + "/data/images"

os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Function to extract text from images
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image).strip()

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = ""
    image_paths = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        extracted_text += page.get_text("text") + "\n"

        # Extract images from PDFs
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_filename = f"{IMAGE_FOLDER}/pdf_page_{page_num+1}_img_{img_index+1}.png"
            with open(img_filename, "wb") as img_file:
                img_file.write(base_image["image"])
            image_paths.append(img_filename)

    # Extract OCR from images inside PDF
    for img_path in image_paths:
        extracted_text += extract_text_from_image(img_path) + "\n"

    return extracted_text.strip()

# Function to extract text from Word documents
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs]).strip()

# Function to extract text from Excel or CSV
def extract_text_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
        return df.to_string()
    except:
        df = pd.read_csv(excel_path, encoding="utf-8", errors="ignore")
        return df.to_string()

# Function to extract text from HTML
def extract_text_from_html(html_path):
    with open(html_path, "r", encoding="utf-8", errors="ignore") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()

# Function to extract text from ZIP files
def extract_text_from_zip(zip_path):
    extracted_text = ""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(ATTACHMENT_FOLDER)
        for filename in zip_ref.namelist():
            extracted_text += f"\n[Extracted File: {filename}]\n"
            extracted_text += process_attachment(os.path.join(ATTACHMENT_FOLDER, filename))
    return extracted_text.strip()

# Process attachment based on file type
def process_attachment(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    extracted_text = ""

    if "image" in file_type:
        extracted_text = extract_text_from_image(file_path)
    elif "pdf" in file_type:
        extracted_text = extract_text_from_pdf(file_path)
    elif "msword" in file_type or "wordprocessingml" in file_type:
        extracted_text = extract_text_from_docx(file_path)
    elif "spreadsheet" in file_type or "excel" in file_type or "csv" in file_path:
        extracted_text = extract_text_from_excel(file_path)
    elif "html" in file_type or file_path.endswith(".html"):
        extracted_text = extract_text_from_html(file_path)
    elif "zip" in file_type:
        extracted_text = extract_text_from_zip(file_path)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            extracted_text = f.read()

    return extracted_text.strip()

# Parse .eml file
def parse_email(file_path):
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    sender_email = msg["From"].split("<")[-1].strip(">")
    subject = msg["Subject"]
    body = ""
    image_text = ""

    # Extract body content
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode(part.get_content_charset(), errors="ignore")
            elif content_type == "text/html":
                soup = BeautifulSoup(part.get_payload(decode=True), "html.parser")
                body = soup.get_text()
            elif content_type.startswith("image/"):
                img_filename = f"{IMAGE_FOLDER}/{os.path.basename(file_path)}.png"
                with open(img_filename, "wb") as img_file:
                    img_file.write(part.get_payload(decode=True))
                image_text += extract_text_from_image(img_filename) + "\n"
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="ignore")

    # Extract attachments
    attachment_text = ""
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = decode_header(part.get_filename())[0][0]
            filename = filename.decode("utf-8") if isinstance(filename, bytes) else filename
            file_path = os.path.join(ATTACHMENT_FOLDER, filename)
            
            with open(file_path, "wb") as f:
                f.write(part.get_payload(decode=True))

            # Process the attachment based on file type
            attachment_text += process_attachment(file_path) + "\n"

    return {
        "Sender Email": sender_email,
        "Subject": subject,
        "Body": body.strip(),
        "Attachment Text": attachment_text.strip(),
        "Image Text": image_text.strip()
    }

# Process all emails in the folder
def process_emails():
    email_data = []
    for email_file in sorted(os.listdir(EMAIL_FOLDER)):
        if email_file.endswith(".eml"):
            email_path = os.path.join(EMAIL_FOLDER, email_file)
            print(f"📩 Processing {email_file}...")
            email_data.append(parse_email(email_path))

    if email_data:
        df = pd.DataFrame(email_data)
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"✅ Data saved to {OUTPUT_CSV}")

# Run processing
if __name__ == "__main__":
    process_emails()
