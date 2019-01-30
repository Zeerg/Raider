import paramiko
import requests
import base64
import json
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
    def check_limit(self):

        pass

    def start_vpn(self, region, ssh_key=None):
        api_url = 'https://api.digitalocean.com/v2/droplets'
        user_data_file = open("/app/plugins/err-tmpvpn/user_data")
        user_data = user_data_file.read()
        do_token = "Bearer " + os.getenv("DIGITAL_OCEAN_KEY")
        headers = {
            "Authorization": do_token,
            "Content-Type": "application/json"
        }
        payload = {
            "name": "vpn-" + str(time()),
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-18-04-x64",
            "ssh_keys": None,
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
        return api_call

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

        key = paramiko.RSAKey(pub_key)
        client = paramiko.SSHClient()
        client.get_host_keys().add(server_ip, 'ssh-rsa', key)
        client.connect(server_ip, username='root')
        stdin, stdout, stderr = client.exec_command('cat /tmp/tmpvpn.ovpn')
        for line in stdout:
            print('... ' + line.strip('\n'))
        client.close()
        return stdout

    @arg_botcmd('--region', dest='region', type=str)
    def temp_vpn(self, msg, region="nyc1"):
        '''
        Usage: !temp_vpn --region <do_region>
        This command will create a temp vpn and place it in the digital ocean region
        '''
        server_ip = "123.123.123.123"
        self.check_limit()
        self.send(msg.frm, "Starting VPN build")
        keys = self.generate_key()
        post_output = self.start_vpn("ams3")
        self.send(msg.frm, post_output.text)
        self.send(msg.frm, post_output.json())
        #config = self.get_remote_config(server_ip, keys[1])
        #self.send(msg.frm, config)

    def destroy_vpns(self, msg):
        '''
        Usage: !destroy_vpns
        This command will destory the running vpns currently
        '''
        pass
