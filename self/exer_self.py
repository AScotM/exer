import os

# Mapping of state codes to human-readable states
TCP_STATES = {
    1: "ESTABLISHED",
    2: "SYN_SENT",
    3: "SYN_RECV",
    4: "FIN_WAIT1",
    5: "FIN_WAIT2",
    6: "TIME_WAIT",
    7: "CLOSE",
    8: "CLOSE_WAIT",
    9: "LAST_ACK",
    10: "LISTEN",
    11: "CLOSING",
    12: "NEW_SYN_RECV",
    13: "FIN_WAIT1",
    14: "FIN_WAIT2",
}

def parse_tcp_socket(line):
    """Parse a single line from /proc/net/tcp"""
    fields = line.split()
    local_address = fields[1]
    rem_address = fields[2]
    state = int(fields[3], 16)  # State is in hex, converting to int
    return local_address, rem_address, state

def get_socket_stats():
    """Get socket stats from /proc/net/tcp and /proc/net/tcp6"""
    sockets = []
    
    # Read TCP connections from /proc/net/tcp
    with open("/proc/net/tcp", "r") as f:
        lines = f.readlines()[1:]  # Skip the header line
        for line in lines:
            local_address, rem_address, state = parse_tcp_socket(line)
            sockets.append({
                "local_address": local_address,
                "rem_address": rem_address,
                "state": TCP_STATES.get(state, f"UNKNOWN({state})")
            })
    
    return sockets

def format_socket_stats(sockets):
    """Format socket stats into a human-readable format."""
    print(f"{'State':<15} {'Local Address':<25} {'Remote Address':<25}")
    print("-" * 65)
    
    for socket in sockets:
        local_ip, local_port = parse_ip_port(socket["local_address"])
        rem_ip, rem_port = parse_ip_port(socket["rem_address"])
        print(f"{socket['state']:<15} {local_ip}:{local_port:<12} {rem_ip}:{rem_port:<12}")

def parse_ip_port(hex_str):
    """Parse hex format IP:Port to human-readable IP:Port"""
    ip_hex, port_hex = hex_str.split(":")
    ip = ".".join(str(int(ip_hex[i:i+2], 16)) for i in range(0, 8, 2))
    port = int(port_hex, 16)
    return ip, port

if __name__ == "__main__":
    sockets = get_socket_stats()
    format_socket_stats(sockets)
