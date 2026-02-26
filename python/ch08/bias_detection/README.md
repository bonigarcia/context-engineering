# Bias detection: assessing fairness in AI recommendations

This example demonstrates how to use the [Fairlearn](https://fairlearn.org/) library to detect demographic parity issues in a model's recommendations.

## Requirements

This project requires [Python](https://www.python.org/) 3.x and the libraries listed in `requirements.txt`.

## Steps for running this example
 
1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the script:
```bash
python bias_detection.py
```

## Output

The script will analyze a mock dataset of credit approval recommendations and calculate the selection rate across different age groups to identify potential bias.

```text
[INFO] Analyzing bias in credit approval recommendations...
[INFO] Demographic Parity Metrics:
Selection rate for Group A (Young): 0.25
Selection rate for Group B (Senior): 0.75
[WARNING] Disparity detected! Demographic Parity Ratio: 0.33
[INFO] A ratio below 0.80 suggests potential bias against Group A.
```