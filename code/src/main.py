from Extract_Email_SavetoCSVFile import process_emails
import subprocess

def main():
    # Step 1: Extract email details and save to CSV
    print("📂 Starting email extraction...")
    output_csv = "email_data.csv"  # Path to save the extracted email data
    process_emails()
    print(f"✅ Email details saved to {output_csv}")

    # Step 2: Process the saved CSV with OpenAI
    print("🤖 Starting OpenAI processing...")
    try:
        # Run the ReadFromCSVAndCallOpenAI.py script
        subprocess.run(["python", "ReadFromCSVAndCallOpenAI.py"], check=True)
        print("✅ OpenAI processing completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while running OpenAI processing: {e}")

if __name__ == "__main__":
    main()