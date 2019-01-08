import socket

from errbot import BotPlugin, arg_botcmd


class Upnp(BotPlugin):
    '''
    usage: !upnp --ip <ip_to_test>
    '''

    @arg_botcmd('--ip', dest='ip', type=str)
    def upnp(self, msg, ip=None):
        upnp_message = [
                    'M-SEARCH * HTTP/1.1',
                    'Host:239.255.255.250:1900',
                    'ST:upnp:rootdevice',
                    'Man:"ssdp:discover"',
                    'MX:1',
                    '']

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(10)
        yield f"Sending UPnP Probes To {ip}"
        s.sendto('\r\n'.join(upnp_message).encode(), (ip, 1900))

        try:
            data, addr = s.recvfrom(32 * 1024)
            yield f"[+] {addr} Responded Likely Exploitable\n"
        except socket.timeout:
            yield(f"Socket Timeout for {ip} Likely Closed or Filtered")
