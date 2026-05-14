import ipaddress

def calculate_vlsm(base_network, hosts_list):
    """
    VLSM calculation engine
    returns list of subnet results
    """

    # ترتيب تنازلي (مهم في VLSM)
    hosts_list = sorted(hosts_list, reverse=True)

    try:
        network = ipaddress.ip_network(base_network, strict=False)
    except ValueError:
        raise ValueError("Invalid base network format")

    current_ip = network.network_address
    results = []

    for i, hosts in enumerate(hosts_list):

        # حساب عدد البتات المطلوبة
        required_bits = 0
        while (2 ** required_bits - 2) < hosts:
            required_bits += 1

        subnet = ipaddress.ip_network(
            (current_ip, 32 - required_bits),
            strict=False
        )

        usable_hosts = list(subnet.hosts())

        results.append({
            "Network": f"Network {i+1}",
            "Required Hosts": hosts,
            "Subnet Mask": subnet.netmask,
            "Network Address": subnet.network_address,
            "Broadcast Address": subnet.broadcast_address,
            "First Host": usable_hosts[0] if usable_hosts else None,
            "Last Host": usable_hosts[-1] if usable_hosts else None,
            "Total Usable": len(usable_hosts)
        })

        # الانتقال للشبكة التالية
        current_ip = subnet.broadcast_address + 1

    return results