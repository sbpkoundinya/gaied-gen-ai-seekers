import openai
import hashlib
import os
import pandas as pd
from langchain.chat_models import ChatOpenAI

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "KEY"

INPUT_CSV = "email_data.csv"
OUTPUT_CSV = "openai_responses.csv"
TICKET_CSV = "support_tickets.csv"

# Initialize OpenAI Client
client = openai.Client()
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Store processed email hashes to detect duplicates
detected_hashes = set()

def generate_email_hash(subject, body, attachment_text):
    """Generate a hash of the email content to detect duplicates."""
    email_content = subject + body + (attachment_text or "")
    return hashlib.md5(email_content.encode()).hexdigest()

def process_with_openai(subject, body, attachment_text, image_text):
    """Analyze email content and classify request types with OpenAI."""
    
    # Generate email hash and check for duplicates
    email_hash = generate_email_hash(subject, body, attachment_text)
    if email_hash in detected_hashes:
        print("⚠️ Duplicate email detected, skipping processing.")
        return None
    detected_hashes.add(email_hash)
    
    prompt = f"""
    You are an AI assistant responsible for categorizing emails based on request type and sub-request type. 
    Extract relevant financial details while prioritizing the email body over attachments unless the request type 
    explicitly requires attachment-based extraction.

    Request Types: Adjustment, AU Transfer, Closing Notice (Reallocation Fees, Amendment Fees, Reallocation Principal),
    Commitment Change (Cashless Roll, Decrease, Increase), Fee Payment (Ongoing Fee, Letter of Credit Fee),
    Money Movement - Inbound (Principal, Interest, Principal + Interest, Principal + Interest + Fee),
    Money Movement - Outbound (Timebound, Foreign Currency).

    Priority Extraction Rules:
    - Default to email body; if attachments are present, check for relevance based on request type.
    - Detect multiple requests and categorize them separately.
    - Extract key details such as Deal Name, Amount, Expiration Date.
    - **Ensure correct classification of Money Movement - Inbound vs. Outbound based on payment direction.**
    - **For repayments, ensure classification as Money Movement - Inbound.**
    
    Email Subject: {subject}
    Email Body: {body}
    Attachment Content: {attachment_text or 'None'}
    Image Text: {image_text or 'None'}
    """
    
    response = llm.predict(prompt)
    return response

# Main execution
if __name__ == "__main__":
    df = pd.read_csv(INPUT_CSV)
    results = []
    
    for _, row in df.iterrows():
        response = process_with_openai(row['subject'], row['body'], row.get('attachment_text', ''), row.get('image_text', ''))
        if response:
            results.append(response)
    
    # Save results
    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
    print("✅ Processing completed!")