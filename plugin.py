###
# Copyright (c) 2011, James Petrosky
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

import twitter

api=twitter.Api(consumer_key='',
		consumer_secret='',
		access_token_key='',
		access_token_secret='')

def strip_accents(string):
  import unicodedata
  return unicodedata.normalize('NFKD', unicode(string)).encode('ASCII', 'ignore')

class SupySpam(callbacks.Plugin):
    """Supybot Twitter plugin.  Hopefully."""
    pass

    
    def lastfrom(self, irc, msg, args, text):
	"""<user>

	Returns the last tweet from <user>
	"""
	status=api.GetUserTimeline(text)
        irc.reply(strip_accents('<'+status[0].user.screen_name+'> '+status[0].text))
    lastfrom=wrap(lastfrom,['text'])

    def friends(self, irc, msg, args):
	"""no arguments

	Lists all usernames being followed.
	"""
	friends=api.GetFriends()
	result=""
	for a in friends:
	    result=result+a.screen_name+', '
	irc.reply(strip_accents(result[:-2]))
    friends=wrap(friends)





    def update(self, irc, msg, args, text):
	"""<update text>

	Update the bot's status
	"""
	status=api.PostUpdate(text)
	irc.replySuccess()
    update=wrap(update,['text'])

    def recent(self, irc, msg, args):
	"""no arguments

	Lists recent updates by users the bot is following.
	"""
	result=api.GetFriendsTimeline(count=30, retweets=True)
	printable=""
	for x in result:
	    printable=printable + "<" + x.user.screen_name + "> " + x.text + " "
        irc.reply(strip_accents(printable))
    recent=wrap(recent)



    def trending(self, irc, msg, args):
	"""no arrguments

	Lists currently trending topics.
	"""
	trends=api.GetTrendsCurrent()
	result=""
	for s in trends:
            result=result+s.name+", "
	irc.reply(strip_accents(result[:-2]))
    trending=wrap(trending)
Class = SupySpam


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
