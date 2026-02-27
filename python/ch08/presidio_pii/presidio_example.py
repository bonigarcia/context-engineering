from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

def main():
    # 1. Initialize the analyzer and anonymizer engines
    # The analyzer uses NLP models and regex to find PII
    analyzer = AnalyzerEngine()
    # The anonymizer applies redaction or masking logic
    anonymizer = AnonymizerEngine()

    # 2. Define the sample text containing sensitive information
    text = (
        "Hello, my name is David Miller. You can reach me at "
        "david.miller@example.com or by phone at 212-555-0123. "
        "I live at 123 Main St, New York."
    )

    # 3. Analyze the text
    # We scan the text for common entities like names, emails, and phone numbers
    print("Analyzing text for PII...")
    results = analyzer.analyze(text=text, language='en')

    # 4. Define the anonymization strategy
    # We replace any found PII with a generic <REDACTED> placeholder
    operators = {
        "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"}),
    }

    # 5. Execute anonymization
    print("Anonymizing sensitive entities...")
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )

    # 6. Display results
    print("-" * 20)
    print(f"Original Text: {text}")
    print("-" * 20)
    print(f"Anonymized Text: {anonymized_result.text}")

if __name__ == "__main__":
    main()
