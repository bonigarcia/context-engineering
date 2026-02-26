import yaml
import os

def load_instructions(file_path):
    """Loads system instructions from a YAML file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instruction file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def validate_governance(instructions_data):
    """Simple governance check for forbidden patterns or terms."""
    # Example: Check for forbidden keywords (e.g., internal server names)
    forbidden_terms = ["internal-db-01", "root_password", "confidential_project_x"]
    
    # Convert instructions to a single string for easy scanning
    content = str(instructions_data)
    
    for term in forbidden_terms:
        if term in content:
            return False, f"Governance violation: Found forbidden term '{term}'"
    
    return True, "Governance check passed. No forbidden terms found."

def format_system_prompt(data):
    """Formats the structured YAML data into a flat system prompt string."""
    parts = []
    instr = data.get("instructions", {})
    
    if "persona" in instr:
        parts.append(instr["persona"])
    
    if "goal" in instr:
        parts.append(f"Your goal is to {instr['goal']}")
    
    if "rules" in instr:
        parts.append("Follow these rules:")
        for rule in instr["rules"]:
            parts.append(f"- {rule}")
            
    if "constraints" in instr:
        parts.append("Constraints:")
        for constraint in instr["constraints"]:
            parts.append(f"- {constraint}")
            
    return "".join(parts)

def main():
    file_path = "system_instructions.yaml"
    
    print(f"[INFO] Loading system instructions...")
    try:
        data = load_instructions(file_path)
        print(f"[INFO] Loaded version {data.get('version', 'unknown')}")
    except Exception as e:
        print(f"[ERROR] Failed to load instructions: {e}")
        return

    print("[INFO] Running governance validation...")
    is_valid, message = validate_governance(data)
    
    if is_valid:
        print(f"[SUCCESS] {message}")
        system_prompt = format_system_prompt(data)
        print("[INFO] Final System Prompt:")
        print("-" * 30)
        print(system_prompt)
        print("-" * 30)
    else:
        print(f"[FAILURE] {message}")

if __name__ == "__main__":
    main()
