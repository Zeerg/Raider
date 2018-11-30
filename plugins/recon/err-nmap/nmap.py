import ipaddress
import subprocess
from errbot import BotPlugin, arg_botcmd


class Nmap(BotPlugin):
    '''
    Nmap bot plugin class.
    Usage: !nmap --scan-type <scan_type> --use-tor <Bool> --ip <ip of target>
    '''
    @arg_botcmd('--scan-type', dest='scan_type', type=str)
    @arg_botcmd('--use-tor', dest='use_tor', type=bool, default=True)
    @arg_botcmd('--ip', dest='ip', type=str)
    def nmap(self, msg, scan_type=None, use_tor=True, ip=None):
        '''
        Single nmap bot command that works with multiple scan types.
        Usage: !nmap --scan-type <scan_type> --use-tor <Bool> --ip <ip of target>
        '''
        # Validate IP address because unvalidated user input is aids.
        if not ipaddress.ip_address(ip):
            yield "Usage: --ip <ip of target>...ie 192.168.1.1"
        elif not scan_type:
            yield "Usage: --scan-type <top100 or top1000>"
        else:
            if scan_type == "top1000":
                bash_command = "proxychains nmap --top-ports 1000 -PN -n -sV " + ip
            elif scan_type == "top100":
                bash_command = "proxychains nmap --top-ports 100 -PN -n -sV " + ip
            elif scan_type == "udp":
                bash_command = "proxychains nmap -F -sU " + ip
            self._bot.add_reaction(msg, "hourglass")
            self._bot.add_reaction(msg, "thumbsup_all")
            process = subprocess.Popen(bash_command.split(),
                                       stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode('UTF-8')
            yield output
