import subprocess
from errbot import BotPlugin, arg_botcmd


class Nmap(BotPlugin):
    '''
    Nikto is an Open Source (GPL) web server scanner which performs comprehensive
    tests against web servers for multiple items.
    '''
    @arg_botcmd('--target', dest='target', type=str)
    def nikto_basic(self, msg, target=None):
        '''
        This bot command performs a basic nikto scan against a target
        Usage: !nikto --host <target>
        '''
        yield "Starting Nikto Scan via Tor. Results will arrive via PM"
        self._bot.add_reaction(msg, "hourglass")
        self._bot.add_reaction(msg, "thumbsup_all")
        bash_command = "proxychains nikto -h " + target
        process = subprocess.Popen(bash_command.split(),
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('UTF-8')
