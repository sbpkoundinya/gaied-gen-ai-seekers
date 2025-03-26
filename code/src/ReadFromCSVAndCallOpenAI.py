import openai
import os
import pandas as pd
import json  # Import json module
from langchain.chat_models import ChatOpenAI  # Correct LangChain import

# 🔹 Set OpenAI API Key securely
os.environ["OPENAI_API_KEY"] = "KEY"  # Don't hardcode; use an environment variable

INPUT_CSV = "email_data.csv"
OUTPUT_CSV = "openai_responses.csv"
TICKET_CSV = "support_tickets.csv"

# 🔹 Initialize OpenAI Client
client = openai.Client()

# 🔹 Initialize OpenAI model using LangChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def process_with_openai(subject, body, attachment_text, image_text):
    """Send extracted email content to OpenAI API with a structured prompt."""

    # 🔹 Structured Prompt
    prompt = f"""
    You are an AI email classification assistant responsible for analyzing emails (which may include attachments) and categorizing them based on Request Type and Sub Request Type. Additionally, you must extract key financial details such as Deal Name, Amount, and Expiration Date while following priority-based extraction rules to ensure accuracy and consistency.

Priority-Based Extraction Rules:
1️. Primary Request Type (Highest Priority)
Identify the main intent of the email.

Focus on the most critical financial action mentioned.

Examples: Money Movement - Inbound, Money Movement - Outbound, Closing Notice, Adjustment.

2️. Secondary Request Type(s) (If Applicable)
Extract additional relevant categories that provide context to the primary request.

Examples: Reallocation Fees, Commitment Change, Decrease/Increase.

3️. Key Financial Details Extraction
Deal Name: Identify the financial agreement associated with the request.

Amount: Extract the key transaction amount.

Expiration Date: Identify relevant dates (e.g., payment date, repricing date).

4️. Justification (Reasoning)
Clearly explain why the email fits into the selected categories.

Keep the explanation concise and structured.

Classification Categories:
1️. Adjustment
2️. AU Transfer
3. Closing Notice
	Reallocation Fees
	Amendment Fees
	Reallocation Principal
4️. Commitment Change
	Cashless Roll
	Decrease
	Increase
5️. Fee Payment
	Ongoing Fee
	Letter of Credit Fee
6️. Money Movement - Inbound
	Principal
	Interest
	Principal + Interest
	Principal + Interest + Fee
7️. Money Movement - Outbound
	Timebound
	Foreign Currency	

**Email Content:**
    - **Subject:** {subject}
    - **Body:** {body}
    - **Attachment Text:** {attachment_text}
    - **Image Text (OCR Extracted):** {image_text}

**Response Format (JSON):**
    {{
        "Category": [
            {{
                "Request Type": "[Primary Request Type]",
                "Sub Request Type": "[Primary Sub Request Type]"
            }},
            {{
                "Request Type": "[Secondary Request Type (if applicable)]",
                "Sub Request Type": "[Secondary Sub Request Type]"
            }}
        ],
        "Deal Name": "[Extracted Deal Name]",
        "Amount": "[Extracted Amount]",
        "Expiration Date": "[Extracted Expiration Date]",
        "Reasoning": "[Provide a concise explanation of why the email fits into the selected category based on priority]"
    }}
    """

    try:
        response = client.chat.completions.create(  # ✅ Corrected OpenAI API call
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:  # ✅ Corrected error handling
        return f"Error: {e}"

# 🔹 Read CSV file
df = pd.read_csv(INPUT_CSV)

# 🔹 Apply OpenAI processing
df["OpenAI Response"] = df.apply(
    lambda row: process_with_openai(row["Subject"], row["Body"], row["Attachment Text"], row["Image Text"]), axis=1
)

# 🔹 Define ROLE_MAPPING
ROLE_MAPPING = {
    "Adjustment": "Adjustment Support",
    "AU Transfer": "Transfer Support",
    "Closing Notice": "Closing Support",
    "Commitment Change": "Commitment Support",
    "Fee Payment": "Fee Support",
    "Money Movement - Inbound": "Inbound Support",
    "Money Movement - Outbound": "Outbound Support",
    "General Support": "General Support"
}

def create_support_ticket(response_json, subject, body):
    """Create a support ticket based on OpenAI response."""
    try:
        response_data = json.loads(response_json)

        primary_request = response_data["Category"][0]["Request Type"]
        sub_request = response_data["Category"][0]["Sub Request Type"]
        deal_name = response_data.get("Deal Name", "")
        amount = response_data.get("Amount", "")
        expiration_date = response_data.get("Expiration Date", "")
        reasoning = response_data.get("Reasoning", "")

        # Determine support team role
        assigned_role = ROLE_MAPPING.get(primary_request, "General Support")

        ticket_details = {
            "Subject": subject,
            "Request Type": primary_request,
            "Sub Request Type": sub_request,
            "Deal Name": deal_name,
            "Amount": amount,
            "Expiration Date": expiration_date,
            "Assigned Role": assigned_role,
            "Reasoning": reasoning
        }

        # 🔹 Save to CSV (if using file-based tracking)
        ticket_df = pd.DataFrame([ticket_details])
        ticket_df.to_csv(TICKET_CSV, mode="a", header=not os.path.exists(TICKET_CSV), index=False)

    except json.JSONDecodeError:
        print("❌ Failed to parse OpenAI response JSON")

# 🔹 Read CSV file
df = pd.read_csv(INPUT_CSV)

# 🔹 Apply OpenAI processing and create tickets
df["OpenAI Response"] = df.apply(
    lambda row: process_with_openai(row["Subject"], row["Body"], row["Attachment Text"], row["Image Text"]), axis=1
)

# 🔹 Generate Support Tickets
df.apply(lambda row: create_support_ticket(row["OpenAI Response"], row["Subject"], row["Body"]), axis=1)

# 🔹 Save results
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ OpenAI responses saved to {OUTPUT_CSV}")
print(f"✅ Support tickets saved to {TICKET_CSV}")
