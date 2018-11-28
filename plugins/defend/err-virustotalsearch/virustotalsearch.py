import requests
import json
import os

from errbot import BotPlugin, botcmd


class VtScanner(BotPlugin):
    """
    This plugin scans things on virus total and posts them into slack.
    """

    @botcmd(split_args_with=None)  # flags a command
    def vt_url(self, msg, args):  # a command callable with !tryme
        """
        Scan a URL
        """
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip,  curl/7.0"
        }
        params = {'apikey': os.getenv("VT_API_KEY"), 'resource': args[0]}
        response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
                                 params=params, headers=headers)

        json_response = response.json()
        vt_results = str(json.dumps(json_response['response_code']))
        if vt_results == '1':
            pretty_json = json.dumps(json_response['positives'])
            vt_url = json.dumps(json_response['scans'])
            total_scan = json.dumps(json_response['total'])
            results = "Virus Total Detected: " + pretty_json + "/" + total_scan
            yield results
        else:
            yield "No results in Virus Total. You might want to submit it"

    @botcmd(split_args_with=None)  # flags a command
    def vt_hash(self, msg, args):  # a command callable with !tryme
        """
        Check a file hash.
        """
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip,  curl 7.0"
        }
        params = {'apikey': '', 'resource': args[0]}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/report',
                                 params=params, headers=headers)

        json_response = response.json()
        vt_results = str(json.dumps(json_response['response_code']))
        if vt_results == '1':
            pretty_json = json.dumps(json_response['positives'])
            vt_url = json.dumps(json_response['scans'])
            total_scan = json.dumps(json_response['total'])
            results = "Virus Total Detected: " + pretty_json + "/" + total_scan
            yield results
        else:
            yield "No results in Virus Total. You might want to submit it"
