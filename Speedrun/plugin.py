###
# Copyright (c) 2020, Elvira Khabirova
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.log as log
import json
import requests
import datetime
import re
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Speedrun')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Speedrun(callbacks.Plugin):
    """Fetch speedrun.com info"""

    threaded = True

    def speedrun(self, irc, msg, args, user, game):
        """<user> <game>

        Fetches info from speedrun.com
        """
        url = None
        response = None
        result = None

        regex = re.compile('[^a-zA-Z0-9_-]')
        user_f = regex.sub('', user)
        game_f = regex.sub('', game)

        url = \
            "https://www.speedrun.com/api/v1/users/{}/personal-bests?".format(user_f) + \
            utils.web.urlencode({ "embed": "category,game", "game": game_f })
        try:
            request = utils.web.getUrl(url).decode()
            response = json.loads(request)
            if not response.get("Error"):
                if "status" in response:
                    irc.reply(response["message"], action=True)
                else:
                    result = ""
                    for run in response["data"]:
                        if (result != ""):
                            result += "; "
                        result += run["category"]["data"]["name"] + " - #" + \
                            str(run["place"]) + " - " + str(datetime.timedelta(seconds=run["run"]["times"]["primary_t"]))
                    if (result != ""):
                        irc.reply("[" + response["data"][0]["game"]["data"]["names"]["international"]
                                + "] " + result, action=True)
                    else:
                        irc.reply("No results", action=True)
            elif response.get("Error"):
                log.debug("Speedrun API: %s" % response["Error"])
                irc.error("Couldn't fetch results")
        except:
            irc.reply("No results", action=True)

    speedrun = wrap(speedrun, ["somethingWithoutSpaces", "somethingWithoutSpaces"])


Class = Speedrun


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
