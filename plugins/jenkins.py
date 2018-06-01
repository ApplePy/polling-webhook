NAME = "jenkins"
TYPE = ["hook"]
API_VERSION = 1


class Hook(object):
    def __init__(self, url, extra_data=None):
        print("{0} hook init successful.".format(NAME))

    def trigger_webhook(self, payload):
        print("{0} hooking payload send success!".format(NAME))
