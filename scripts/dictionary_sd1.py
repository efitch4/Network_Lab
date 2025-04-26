router1 = {
    "G0/1": "192.168.0.1",
    "G0/2": "192.168.0.2",
    "G0/3": "192.168.0.3",
    "G0/4": "192.168.0.4",
    "G0/5": "192.168.0.5"
}

print("Available Ports:")
for port in router1:
    print(f"{port}: {router1[port]}")

selected_port = input("Please select a port (e.g., G0/1): ")

if selected_port in router1:
    print(f"The IP address for {selected_port} is {router1[selected_port]}")
else:
    print("Invalid port selected.")
