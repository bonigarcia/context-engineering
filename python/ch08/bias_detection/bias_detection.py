import pandas as pd
from fairlearn.metrics import MetricFrame, selection_rate

def run_bias_audit():
    """
    Simulates a bias audit for an AI system recommending credit approvals.
    """
    # Mock data: 'recommendation' is the binary output (1=approved, 0=denied)
    # 'age_group' is the sensitive attribute
    data = {
        "user_id": range(100),
        "age_group": ["Young"] * 50 + ["Senior"] * 50,
        "recommendation": [1] * 10 + [0] * 40 + [1] * 30 + [0] * 20
    }
    
    df = pd.DataFrame(data)
    
    print("[INFO] Analyzing bias in credit approval recommendations...")
    
    # Calculate selection rate per group
    metrics = MetricFrame(
        metrics=selection_rate,
        y_true=df["recommendation"], # In an audit, we treat the recommendation as the outcome
        y_pred=df["recommendation"],
        sensitive_features=df["age_group"]
    )
    
    young_rate = metrics.by_group["Young"]
    senior_rate = metrics.by_group["Senior"]
    
    print(f"[INFO] Selection rate for Young group: {young_rate:.2f}")
    print(f"[INFO] Selection rate for Senior group: {senior_rate:.2f}")
    
    # Calculate Demographic Parity Ratio
    ratio = young_rate / senior_rate if senior_rate > 0 else 1.0
    print(f"[INFO] Demographic Parity Ratio: {ratio:.2f}")
    
    if ratio < 0.80:
        print("[WARNING] Significant disparity detected against the Young group.")
        print("[INFO] This result suggests the context or model logic may be biased.")
    else:
        print("[SUCCESS] No significant demographic disparity detected.")

if __name__ == "__main__":
    run_bias_audit()
