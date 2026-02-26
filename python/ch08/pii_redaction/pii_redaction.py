import re

def redact_pii(text):
    """
    Simple PII redaction using regular expressions.
    Note: In production, use specialized libraries like Microsoft Presidio.
    """
    
    # Redact Emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, "[EMAIL]", text)
    
    # Redact Phone Numbers (Basic US format)
    phone_pattern = r'\b(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b'
    text = re.sub(phone_pattern, "[PHONE]", text)
    
    # Redact potential Names (Simple heuristic for capitalized words followed by capitalized words)
    # This is a very basic example; name detection is complex.
    name_pattern = r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'
    text = re.sub(name_pattern, "[NAME]", text)

    # Redact simple address patterns (Street numbers and names)
    address_pattern = r'\d+ [A-Z][a-z]+ (St|Ave|Rd|Blvd|Dr)'
    text = re.sub(address_pattern, "[ADDRESS]", text)
    
    return text

def main():
    sample_message = (
        "Hello, my name is John Doe. My email is john.doe@example.com "
        "and my phone number is 555-123-4567. I live at 123 Maple St."
    )
    
    print("[INFO] Original Message:")
    print(sample_message)
    print("[INFO] Redacting PII...")
    
    redacted_message = redact_pii(sample_message)
    
    print("[INFO] Redacted Message:")
    print(redacted_message)

if __name__ == "__main__":
    main()
