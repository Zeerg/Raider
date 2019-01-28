variable "do_token" {}
variable "region" {}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = "${var.do_token}"
}

# Create a new SSH key
data "digitalocean_ssh_key" "commodore" {
  name = "Commodore"
}

resource "digitalocean_droplet" "vpn" {
  image  = "ubuntu-18-04-x64"
  name   = "vpn-${sha256(timestamp())}"
  region = "${var.region}"
  size   = "s-1vcpu-1gb"
  ssh_keys = ["${data.digitalocean_ssh_key.commodore.fingerprint}"]
  user_data = <<EOF
#!/bin/bash
apt-get update
apt-get upgrade -y
apt-get install docker docker.io -y
docker volume create --name ovpn-data-dir
export IP_ADDRESS=$(ifconfig eth0 | grep "inet " | awk '{print $2}')
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_genconfig -u udp://$${IP_ADDRESS}
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn /bin/bash -c "easyrsa init-pki"
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn /bin/bash -c "easyrsa --batch --req-cn=$${IP_ADDRESS} build-ca nopass"
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn /bin/bash -c "easyrsa gen-dh"
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn /bin/bash -c "openvpn --genkey --secret /etc/openvpn/pki/ta.key"
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm kylemanna/openvpn /bin/bash -c "easyrsa build-server-full $${IP_ADDRESS} nopass"
docker run -v ovpn-data-dir:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
docker run -v ovpn-data-dir:/etc/openvpn --log-driver=none --rm -it kylemanna/openvpn easyrsa build-client-full tmpvpn nopass
docker run -v $OVPN_DATA:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_getclient tmpvpn > /tmp/tmpvpn.ovpn
EOF
}


output "droplet_ip" {
  value = "${digitalocean_droplet.vpn.ipv4_address}"
}