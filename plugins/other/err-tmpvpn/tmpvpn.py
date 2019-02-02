import paramiko
import requests
import base64
import os

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from time import time
from errbot import BotPlugin, arg_botcmd


class TmpVpn(BotPlugin):
    '''
    Temp VPN helper plugins.
    '''
    global headers
    do_token = "Bearer " + os.getenv("DIGITAL_OCEAN_KEY")
    headers = {
        "Authorization": do_token,
        "Content-Type": "application/json"
    }

    def check_limit(self):

        api_url = 'https://api.digitalocean.com/v2/droplets/?tag_name=vpn'
        running_vpns = requests.get(api_url, headers=headers)
        json_response = running_vpns.json()
        running_count = len(json_response['droplets'])
        return running_count

    def post_key_to_api(self, public_key):
        api_url = 'https://api.digitalocean.com/v2/account/keys'
        key_post_body = {
            "name": "VPN_KEY_" + str(time()),
            "public_key": public_key
        }
        print(key_post_body)
        new_key = requests.post(api_url, json=key_post_body, headers=headers)
        json_response = new_key.json()
        return json_response['ssh_key']['fingerprint']

    def start_vpn(self, region, ssh_key=None):
        api_url = 'https://api.digitalocean.com/v2/droplets'
        user_data_file = open("/app/plugins/err-tmpvpn/user_data")
        user_data = user_data_file.read()

        payload = {
            "name": "vpn-" + str(time()),
            "region": region,
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-18-04-x64",
            "ssh_keys": str(ssh_key),
            "backups": False,
            "ipv6": True,
            "user_data": user_data,
            "private_networking": None,
            "volumes": None,
            "tags": [
                "vpn"
            ]
        }
        api_call = requests.post(api_url, json=payload, headers=headers)
        return api_call.json()['droplet']['id']

    def generate_key(self):
        key_list = []
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption())
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )
        key_list.append(private_key)
        key_list.append(public_key)
        return key_list

    def get_remote_config(self, server_ip, pub_key):

        key = paramiko.PKey.from_private_key(pub_key)
        client = paramiko.SSHClient()
        client.get_host_keys().add(server_ip, 'ssh-rsa', key)
        client.connect(server_ip, username='root')
        stdin, stdout, stderr = client.exec_command('cat /tmp/tmpvpn.ovpn')
        for line in stdout:
            print('... ' + line.strip('\n'))
        client.close()
        return stdout

    def get_droplet_ip(droplet_id):

        api_url = 'https://api.digitalocean.com/v2/droplets/' + str(droplet_id)
        api_call = requests.get(api_url, headers=headers)
        print(api_call.text)
        json_payload = api_call.json()
        return json_payload['droplet']['networks']['v4'][0]['ip_address']

    @arg_botcmd('--region', dest='region', type=str)
    def temp_vpn(self, msg, region="ams3"):
        '''
        Usage: !temp_vpn --region <do_region>
        This command will create a temp vpn and place it in the digital ocean region
        '''
        running_count = self.check_limit()
        if str(running_count) <= os.getenv("DIGITAL_OCEAN_KEY"):
            self.send(msg.frm, "Starting VPN build")
            keys = self.generate_key()
            key_finger = self.post_key_to_api(keys[1].decode("UTF8"))
            post_output = self.start_vpn(region, key_finger)
            self.send(msg.frm, "Droplet ID is: " + post_output)
            self.send(msg.frm, "Waiting on OpenVpn Setup")
            #config = self.get_remote_config(server_ip, keys[1])
            #self.send(msg.frm, config)
        else:
            yield "Sorry we are at max VPNs"

    def destroy_all_vpns(self, msg):
        '''
        Usage: !destroy_all_vpns
        This command will destory the running vpns currently
        '''
        api_url = 'https://api.digitalocean.com/v2/droplets?tag_name=vpn'
        api_call = requests.delete(api_url, headers=headers)
        yield f"Delete all status {api_call.status_code}"
