from napalm import get_network_driver
import difflib

driver = get_network_driver('nxos_ssh')
device = driver('192.168.184.145', 'admin', 'Hoss1234')
device.open()

device.load_replace_candidate(filename='32_nexus_backup')

device._create_sot_file()
sot_content = device._send_command("show file sot_file", raw_text=True)
candidate_content = device._send_command("show file candidate_config.txt", raw_text=True)

diff = "\n".join(difflib.unified_diff(
    sot_content.splitlines(),
    candidate_content.splitlines(),
    fromfile="running-config",
    tofile="candidate",
    lineterm="",
))
print(diff)

if len(diff.strip()) > 0:
    choice = input("\nWould you like to replace the config? [y/N]: ").strip().lower()
    if choice == 'y':
        print('commit...')
        device.commit_config()

        rb = input("\nWould you like to rollback to the previous config? [y/N]: ").strip().lower()
        if rb == 'y':
            print('rolling back...')
            device.rollback()
    else:
        print('Discarding')
        device.discard_config()
else:
    print('NO DIFFERENCE')

device.close()
print('Done.')
