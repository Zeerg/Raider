import requests
import json

from errbot import BotPlugin, botcmd
from time import sleep


class Cymon(BotPlugin):
    @botcmd  # flags a command
    def cymon_domain(self, msg, args):  # a command callable with !tryme
        cymon_url = 'https://api.cymon.io/v2/ioc/search/domain/'
        target_domain = args
        get_url = cymon_url + target_domain
        request = requests.get(get_url)
        results = json.loads(request.text)
        if results['total'] == 0:
            yield "Nothing Returned from Cymon...Prob safe"
        else:
            yield "Gathering Details Now. I'll respond when I have something"
            sleep(5)
            for items in results['hits']:
                yield "Title: " + items['title']
                yield "Cymon Tags: " + str(items['tags'])
                try:
                    yield "Reported URL: " + items['ioc']['url']
                    yield " "
                except KeyError:
                    yield "No URL Found in Cymon DataSet"
                    yield " "

    @botcmd  # flags a command
    def cymon_ip(self, msg, args):  # a command callable with !tryme
        return 'It *works* !'  # This string format is markdown.

    @botcmd  # flags a command
    def cymon_search(self, msg, args):  # a command callable with !tryme
        return 'It *works* !'  # This string format is markdown.

    @botcmd  # flags a command
    def cymon_iptodomains(self, msg, args):  # a command callable with !tryme
        return 'It *works* !'  # This string format is markdown.

    @botcmd  # flags a command
    def cymon_hashlookup(self, msg, args):  # a command callable with !tryme
        return 'It *works* !'  # This string format is markdown.
