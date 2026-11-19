from pyflow.utils import analyze_email_domains

if __name__ =="__main__":
    print("__Question 5: Email domain analysis test----")

    # for the test take some dummy emails list

    sample_emails =[
        "student1@gmail.com",
        "student2@yahoo.com",
        "data_guy@gmail.com",
        "boss@outlook.com",
        "test.user@YAHOO.COM",
        "invalid_email_without_at_sign"
    ]
    try:
        result = analyze_email_domains(sample_emails)
        print("\n[Success] Domain Analysis Result:")
        for domain, count in result.items():
            print(f"-> {domain}:,{count} emails")

    except Exception as e:
        print(f"[Error] Test fail ho gaya: {e}")