# AI-Powered Email Classification & OCR Solution

## 📌 Project Overview
This project is a Gen AI-powered email classification and OCR solution that processes `.eml` files, extracts relevant details, classifies email requests, and routes them accordingly. The solution supports:
- Request categorization
- Duplicate detection
- Priority-based extraction
- Multi-request handling

The system is designed to integrate seamlessly with financial service workflows, ensuring automated processing and routing of service requests.

---

## 🚀 Features
✅ **Email Classification**: Categorizes emails into predefined request types and sub-request types.
✅ **Duplicate Detection**: Prevents reprocessing of duplicate emails.
✅ **Multi-Request Handling**: Detects and processes multiple requests in a single email.
✅ **Attachment Processing**: Extracts information from PDFs, images (JPG/PNG/GIF), TXT, DOC, and XLSX files.
✅ **Priority-Based Extraction**: Prefers email body over attachments unless the request type requires attachment-based extraction.
✅ **Context-Based Data Extraction**: Retrieves key financial details such as deal name, amount, and expiration date.

---

## 📂 Request Types & Sub-Request Types
### Supported Request Types:
1️⃣ **Adjustment**
2️⃣ **AU Transfer**
3️⃣ **Closing Notice**  
   - Reallocation Fees
   - Amendment Fees
   - Reallocation Principal
4️⃣ **Commitment Change**  
   - Cashless Roll
   - Decrease
   - Increase
5️⃣ **Fee Payment**  
   - Ongoing Fee
   - Letter of Credit Fee
6️⃣ **Money Movement - Inbound**  
   - Principal
   - Interest
   - Principal + Interest
   - Principal + Interest + Fee
7️⃣ **Money Movement - Outbound**  
   - Timebound
   - Foreign Currency

---

## 🛠️ Technology Stack
- **Python** (Backend Processing)
- **FastAPI** (Optional API Integration)
- **OpenAI API** (Classification)
- **Tesseract OCR** (Image Text Extraction)
- **Pandas** (Data Handling)
- **LangChain** (AI Model Interaction)
- **Unittest** (Test Automation)

---

## 🔧 Installation & Setup
### Prerequisites:
- Python 3.8+
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```

### Running the Application:
1️⃣ **Extract email details and save to CSV:**
   ```sh
   python code/src/Extract_Email_SavetoCSVFile.py
   ```
2️⃣ **Process saved emails with OpenAI classification:**
   ```sh
   python code/src/ReadFromCSVAndCallOpenAI.py
   ```
3️⃣ **Run test cases:**
   ```sh
   python -m unittest discover code/test
   ```

---

## 📖 Usage Guide
- **To classify a new email**, drop the `.eml` file into `code/src/data/`
- The system will process the email and generate:
  - `openai_responses.csv` (AI-classified results)
  - `support_tickets.csv` (Generated ticket details)

---

## 🧪 Testing & Validation
- The test suite covers:
  ✅ Classification for all request and sub-request types.
  ✅ Emails with & without attachments.
  ✅ Various attachment types (PDF, images, TXT, DOC, XLSX, etc.).
  ✅ Edge cases such as duplicate emails and multi-request handling.

To execute all tests:
```sh
python -m unittest discover code/test
```

---

## 📁 Project Structure
```
├── code
│   ├── src
│   │   ├── Extract_Email_SavetoCSVFile.py
│   │   ├── ReadFromCSVAndCallOpenAI.py
│   │   ├── update_email_classification.py
│   │   ├── data
│   │   │   ├── sample.eml
│   │   │   ├── attachments
│   │   │   │   ├── sample.pdf
│   │   │   │   ├── image.jpg
│   ├── test
│   │   ├── test_email_classification.py
├── requirements.txt
├── README.md
```

---

## 🚀 Deployment Guide
To package the project, run:
```sh
zip -r email_classification_solution.zip code README.md requirements.txt
```
For production deployment:
- **Option 1:** Deploy via FastAPI & expose an API.
- **Option 2:** Integrate with an existing service pipeline.

---

## 🔮 Future Enhancements
🚀 **API Integration:** Expose an API endpoint for real-time email classification.  
🚀 **Logging & Monitoring:** Enhance debugging with better logging.  
🚀 **Improved OCR:** Enhance text extraction accuracy from complex documents.  

---

## 📩 Contact Information
For support, reach out at: [your-email@example.com]
