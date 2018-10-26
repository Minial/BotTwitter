import logging
import random
import json

logger = logging.getLogger(__name__)

class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, txt, attachments=None):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {} with attachments: {}'.format(txt, channel_id, attachments))
        channel = self.clients.rtm.server.channels.find(channel_id)
        if attachments:
            self.clients.web.chat.post_message(channel_id, txt, attachments=attachments, as_user='true')
            print(json.dumps(attachments))
        else:
            channel.send_message("{}".format(txt))

    #### SPECIFIC USE-CASE METHODS #####

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        docs_url = "https://github.com/thundergolfer/arXie-Bot#how-to-basics"
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm a Slack bot written to keep you update to date with ML.  I *_respond_* to a number of commands:",
            "> `hi <@{}>` - I'll respond with a randomized greeting mentioning your user. :wave:".format(bot_uid),
            "> `<@{}> [COMMAND] - I respond to a number of natural language commands. See docs here: {}`".format(bot_uid, docs_url)
            "> `<@{}> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:".format(bot_uid))
        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
