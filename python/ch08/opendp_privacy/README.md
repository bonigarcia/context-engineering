# Differential privacy with OpenDP

This example demonstrates how to implement differential privacy using the [OpenDP])(https://docs.opendp.org/) library. The script calculates a private mean of a numerical dataset while protecting individual data points. To achieve this the system builds a transformation pipeline that bounds the data and ensures a fixed dataset size. It then applies the Laplace mechanism to add calibrated noise based on a privacy budget.

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
python opendp_example.py
```

## Output

The script will compute both the actual mean and the differentially private mean of a sample dataset.

```text
Actual Mean: 40.00
Differentially Private Mean: 38.74
```