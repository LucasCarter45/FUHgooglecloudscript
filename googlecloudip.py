from google.cloud import compute_v1

def update_firewall_rule(project_id, firewall_rule_name, source_ip, action):
    firewall_client = compute_v1.FirewallsClient()

    firewall_rule = firewall_client.get(project=project_id, firewall=firewall_rule_name)

    if source_ip in firewall_rule.source_ranges:
        if action == 'allow':
            print(f"IP {source_ip} is already allowed in the firewall rule.")
            return
        elif action == 'deny':
            firewall_rule.source_ranges.remove(source_ip)
            print(f"IP {source_ip} will be removed from the allowed list.")
    else:
        if action == 'allow':
            firewall_rule.source_ranges.append(source_ip)
            print(f"IP {source_ip} will be allowed in the firewall rule.")
        elif action == 'deny':
            print(f"IP {source_ip} is not currently allowed, no changes will be made.")
            return

    
    operation = firewall_client.update(project=project_id, firewall=firewall_rule_name, firewall_resource=firewall_rule)

    print(f"Updating firewall rule {firewall_rule_name}...")
    wait_for_operation(project_id, operation)

def wait_for_operation(project_id, operation):
    """Wait for the operation to complete."""
    compute_client = compute_v1.GlobalOperationsClient()
    while True:
        result = compute_client.get(project=project_id, operation=operation.name)
        if result.status == compute_v1.Operation.Status.DONE:
            print("Update completed.")
            break
        else:
            print("Waiting for the operation to finish...")

if __name__ == "__main__":
    project_id = "carbon-storm-435915-e4"
    firewall_rule_name = "test-vpc-firewall"
    source_ip = "35.235.240.0/20"
    action = "allow"

    update_firewall_rule(project_id, firewall_rule_name, source_ip, action)
