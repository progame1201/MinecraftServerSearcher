from nbtlib import Compound, List, String, load

def find_ip(ip, file):
    for server in file['servers']:
        if ip == str(server['ip']):
            return True
    return False

def last_server_id(file_path):
    with load(file_path) as servers:
        return len(servers['servers'])

def add_server_to_minecraft(server_name, file_path, server_ip):
    with load(file_path) as servers:
        new_server = Compound({
            'ip': String(server_ip),
            'name': String(f"{last_server_id(file_path)} - {server_name}"),
        })
        if find_ip(server_ip, servers) == False:
         servers['servers'].append(new_server)
         return True