# Sublime BetterSettings Dependency

Better settings management for Sublime Plugins.

This module allows a plugin to easily implement OS, Host and
OS/Host-level settings aside the normal user-level settings.

This allows to keep the settings file in the User package, so they can
be synced between machines using different OSes or with specific
configuration for each host without interfering between them.

To implement, you should load the settings in the `plugin_loaded` method
of your package:

```python
import better_settings
settings = None

def plugin_loaded():
    global settings
    settings = better_settings.load_for(__package__, "MyPackage")
```

Where `__package__` should be the one of the main file of your package, as it's going to be used to get the path of the default settings when using the oepn settings command, and `MyPackage` is the name of the settings file you want to use (typically, it's the name of your package).

The format of the file names is as follows:

- For user settings: `MyPackage.sublime-settings`
- For OS-level settings: `MyPackage (Windows).sublime-settings`
- For Host-level settings: `MyPackage (hostname).sublime-settings`
- For Host/OS-level settings: `MyPackage (hostname on Windows).sublime-settings`

Once loaded, you can use the `get` method to get the most specific value
for a setting.

Precedency is as follows:

  1. Host/OS Settings
  2. Host
  3. OS
  4. User settings

## Example

If you have the following files in your User package folder:

```javascript
// MyPackage.sublime-settings
{
  "source": "User"
}
```

```javascript
// MyPackage (Windows).sublime-settings
{
  "source": "OS"
}
```

```javascript
// MyPackage (host1).sublime-settings
{
  "source": "Host"
}
```

```javascript
// MyPackage (host1 on Windows).sublime-settings
{
  "source": "OS/Host"
}
```

And you use:

    settings.get('source')

The value to get, given you use the machine with the hostname and OS
specified in the following table are:

| Hostname | OS      | Value   |
|----------|---------|---------|
| host1    | Windows | OS/Host |
| host1    | Linux   | Host    |
| host2    | Windows | OS      |
| host2    | Linux   | User    |

## Command to open the settings file

You can implement a command to open the settings files:

```python
class MyPackageOpenSettings(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    def run(self):
        # global settings  # Not required as we are not replacing the instance
        settings.open_settings(self.window)
```

And then use it on your `MyPackage.sublime-commands` file as follows:

```json
[
  {
        "caption": "Preferences: MyPackage Settings",
        "command": "my_package_open_settings"
  }
]
```

## Packages using this dependency

* [ToolRunner](https://github.com/KuttKatrea/sublime-toolrunner)
