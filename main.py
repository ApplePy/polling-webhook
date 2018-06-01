#! /usr/bin/env python3
import plugins.api


def main():
    test = plugins.api.get_poll_plugin("github", "stuff")
    test.success()
    test2 = plugins.api.get_hook_plugin("github", "stuff")
    test2.success()


if __name__ == "__main__":
    main()
