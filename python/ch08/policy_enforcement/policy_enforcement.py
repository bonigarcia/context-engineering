def evaluate_policy(user, tool_name, arguments):
    """
    A simple policy engine inspired by Open Policy Agent (OPA).
    In a real system, this would evaluate Rego files.
    """
    # Policy Rules
    roles = {
        "admin_user": ["read", "write", "delete"],
        "marketing_intern": ["read"]
    }
    
    tool_permissions = {
        "list_files": "read",
        "generate_text": "read",
        "delete_database": "delete",
        "update_credentials": "write"
    }
    
    user_role = user.get("role", "guest")
    user_perms = roles.get(user_role, [])
    required_perm = tool_permissions.get(tool_name, "none")
    
    if required_perm in user_perms:
        return True, "ALLOW"
    else:
        return False, f"DENY. Reason: User with role '{user_role}' lacks '{required_perm}' permission for tool '{tool_name}'."

def main():
    user_a = {"id": "u1", "role": "marketing_intern"}
    
    # Test 1: Safe action
    print(f"[INFO] User {user_a['id']} ({user_a['role']}) calling 'list_files'...")
    allowed, msg = evaluate_policy(user_a, "list_files", {})
    print(f"[RESULT] {msg}")
    
    # Test 2: Restricted action
    print(f"[INFO] User {user_a['id']} ({user_a['role']}) calling 'delete_database'...")
    allowed, msg = evaluate_policy(user_a, "delete_database", {"db": "prod_users"})
    print(f"[RESULT] {msg}")

if __name__ == "__main__":
    main()
