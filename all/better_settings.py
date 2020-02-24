"""
Better settings management for Sublime Plugins.

This module allows a plugin to easily implement OS, Host and
OS/Host-level settings aside the normal user-level settings.

This allows to keep the settings file in the User package, so they can
be synced between machines using different OSes or with specific
configuration for each host without interfering between them.
"""
import platform

import sublime

SCOPE_HOST_OS = "Host/OS"
SCOPE_HOST = "Host"
SCOPE_USER = "User"
SCOPE_OS = "OS"
SCOPE_DEFAULT = "Default"


ASK_SCOPE_ITEMS = [
    [SCOPE_DEFAULT, "Default settings"],
    [SCOPE_USER, "Normal user settings"],
    [SCOPE_OS, "Settings specific to this machine OS"],
    [SCOPE_HOST, "Settings specific to this machine"],
    [SCOPE_HOST_OS, "Settings specific to this machine on this OS"],
]


class BetterSettings(object):
    def __init__(self, basepackage, package_name):
        self.basepackage = basepackage
        self.package_name = package_name
        self.hostplatform_settings = None
        self.host_settings = None
        self.platform_settings = None
        self.user_settings = None

    def get(self, setting_name, default=None):
        return self.hostplatform_settings.get(
            setting_name,
            self.host_settings.get(
                setting_name,
                self.platform_settings.get(
                    setting_name, self.user_settings.get(setting_name, default)
                ),
            ),
        )

    def set(self, scope, setting_name, setting_value):
        if scope == SCOPE_HOST_OS:
            self.hostplatform_settings.set(setting_name, setting_value)
        elif scope == SCOPE_HOST:
            self.host_settings.set(setting_name, setting_value)
        elif scope == SCOPE_USER:
            self.user_settings.set(setting_name, setting_value)
        elif scope == SCOPE_OS:
            self.platform_settings.set(setting_name, setting_value)
        elif scope == SCOPE_DEFAULT:
            raise Exception("You should not save the default settings")
        else:
            raise Exception("Invalid scope specified: %s" % (scope))

    def load(self):
        self.hostplatform_settings = sublime.load_settings(
            self.get_hostplatform_settings_filename()
        )

        self.host_settings = sublime.load_settings(self.get_host_settings_filename())

        self.platform_settings = sublime.load_settings(
            self.get_platform_settings_filename()
        )

        self.user_settings = sublime.load_settings(self.get_settings_filename())

        self.loaded_ = True

    def save(self):
        sublime.save_settings(self, self.get_hostplatform_settings_filename())
        sublime.save_settings(self, self.get_host_settings_filename())
        sublime.save_settings(self, self.get_settings_filename())
        sublime.save_settings(self, self.get_platform_settings_filename())

    def add_on_change(self, event_name, callback):
        self.hostplatform_settings.add_on_change(event_name, callback)
        self.user_settings.add_on_change(event_name, callback)
        self.platform_settings.add_on_change(event_name, callback)
        self.host_settings.add_on_change(event_name, callback)

    def clear_on_change(self, event_name):
        if self.hostplatform_settings is not None:
            self.hostplatform_settings.clear_on_change(event_name)

        if self.host_settings is not None:
            self.host_settings.clear_on_change(event_name)

        if self.platform_settings is not None:
            self.platform_settings.clear_on_change(event_name)

        if self.user_settings is not None:
            self.user_settings.clear_on_change(event_name)

    def get_hostplatform_settings_filename(self):
        return self.get_settings_filename(
            platform.uname()[1].lower() + " on " + sublime.platform().capitalize()
        )

    def get_host_settings_filename(self):
        return self.get_settings_filename(platform.uname()[1].lower())

    def get_platform_settings_filename(self):
        return self.get_settings_filename(sublime.platform().capitalize())

    def get_settings_filename(self, special=None):
        special = " (" + special + ")" if special else ""
        return "".join((self.package_name, special, ".sublime-settings"))

    def get_hostplatform_setting(self, setting_name, default=None):
        return self.hostplatform_settings.get(setting_name, default)

    def get_host_setting(self, setting_name, default=None):
        return self.host_settings.get(setting_name, default)

    def get_platform_setting(self, setting_name, default=None):
        return self.platform_settings.get(setting_name, default)

    def get_user_setting(self, setting_name, default=None):
        return self.user_settings.get(setting_name, default)

    def get_settings_file_path(self, scope):
        return "${packages}/%0s/%1s" % self.get_settings_pieces(scope)

    def get_settings_pieces(self, scope):
        if scope == SCOPE_HOST_OS:
            return ("User/", self.get_hostplatform_settings_filename())
        if scope == SCOPE_HOST:
            return ("User/", self.get_host_settings_filename())
        elif scope == SCOPE_USER:
            return ("User/", self.get_settings_filename())
        elif scope == SCOPE_OS:
            return ("User/", self.get_platform_settings_filename())
        elif scope == SCOPE_DEFAULT:
            return (self.basepackage, self.get_settings_filename())
        else:
            raise Exception("Invalid scope specified: %s" % (scope))

    def open_settings(self, window, scope=None):
        def do_open_settings(selected_scope):
            window.run_command(
                "open_file", {"file": self.get_settings_file_path(selected_scope)}
            )

        def on_ask_scope_done(selected_index):
            if selected_index < 0:
                return

            selected_scope = ASK_SCOPE_ITEMS[selected_index][0]
            do_open_settings(selected_scope)

        def ask_scope_and_open_settings():
            window.show_quick_panel(ASK_SCOPE_ITEMS, on_ask_scope_done, 0, 0, None)

        if scope is None:
            ask_scope_and_open_settings()
        else:
            do_open_settings(scope)
