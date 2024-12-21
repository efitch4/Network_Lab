from netmiko import ConnectHandler

# Router Details
router = {
        "device_type":"cisco_ios",
        "ip":"192.168.1.157",
        "username":"admin",
        "password":"admin",
        "secret":"admin"
}

acl_commands = [
    "ip access-list extended ALLOW_HTTP",
    "permit tcp any any eq 80",
    "permit tcp any any eq 443",
    "deny ip any any",
]

def deploy_acl():
    try:
        print("Connecting to the router....")
        connection = ConnectHandler(**router)

        connection.enable

        print("Entering configuration mode...")
        output = connection.send_config_set(acl_commands)
        print("ACL deployed successfully!")
        print(output)

        print("Verifying ACL...")
        verification = connection.send_command("show ip access-list ALLOW_HTTP")
        print("Verification Output:")
        print(verification)

        connection.disconnect()
        print("Disconnected from the router.")
    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    deploy_acl()