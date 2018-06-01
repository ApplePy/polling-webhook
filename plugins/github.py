NAME = "github"
TYPE = ["poll", "hook"]
API_VERSION = 1


class Poll(object):
    def __init__(self, url, extra_data=None):
        print("{0} poll init successful.".format(NAME))

    def success(self):
        print("{0} polling import success!".format(NAME))


class Hook(object):
    def __init__(self, url, extra_data=None):
        print("{0} hook init successful.".format(NAME))

    def success(self):
        print("{0} hooking import success!".format(NAME))
