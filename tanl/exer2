import subprocess

def get_socket_stats():
    """Executes ss -tanl command and returns the output."""
    try:
        result = subprocess.run(['ss', '-tanl'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing ss command: {e}")
        return None

def parse_socket_stats(stats):
    """Parses ss command output into a list of dictionaries."""
    lines = stats.splitlines()
    parsed_stats = []
    
    # Skip the header line and process each entry
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 5:
            socket_info = {
                'state': parts[0],
                'recv_queue': parts[1],
                'send_queue': parts[2],
                'local_address': parts[3],
                'peer_address': parts[4],
            }
            parsed_stats.append(socket_info)
    
    return parsed_stats

def print_parsed_socket_stats():
    """Prints parsed socket statistics in a more readable format."""
    stats = get_socket_stats()
    
    if stats:
        parsed_stats = parse_socket_stats(stats)
        
        print(f"{'State':<10} {'Local Address':<25} {'Peer Address':<25}")
        print("-" * 60)
        
        for entry in parsed_stats:
            print(f"{entry['state']:<10} {entry['local_address']:<25} {entry['peer_address']:<25}")
    else:
        print("Failed to retrieve socket stats.")

if __name__ == "__main__":
    print_parsed_socket_stats()
