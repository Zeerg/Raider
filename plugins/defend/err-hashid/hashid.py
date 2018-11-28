# Import Hashid class so we don't need to use os or another subshell
from hashid import HashID
from errbot import BotPlugin, arg_botcmd


class HashIDPlugin(BotPlugin):
    '''
    HashID Class
    Usage: !hashid --hash <hash_to_id>
    '''
    @arg_botcmd('--hash', dest='hash_str', type=str)
    def hashid(self, msg, hash_str=None):
        '''
        Adds the ability for slack to use hashid.
        Usage: !hashid --hash <hash_to_id>
        '''
        hid = HashID()
        matches = ""
        self._bot.add_reaction(msg, "hourglass")
        for match in hid.identifyHash(hash_str):
            matches += f"Match: {match.name}; Hashcat Mode: {match.hashcat}\n"
        yield matches
        self._bot.remove_reaction(msg, "hourglass")
