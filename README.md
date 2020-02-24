# Sublime BetterSettings Dependency

Better settings management for Sublime Plugins.

This module allows a plugin to easily implement OS, Host and
OS/Host-level settings aside the normal user-level settings.

This allows to keep the settings file in the User package, so they can
be synced between machines using different OSes or with specific
configuration for each host without interfering between them.

To implement, you can create an instance of the
`better_settings.BetterSettings` class.

    settings = BetterSettings(__package__, "My Package")

the, use the `load` method to load the different settings files for each specifity.

The format of the file names is as follows:

- For user settings: `My Package.sublime-settings`
- For OS-level settings: `My Package (Windows).sublime-settings`
- For Host-level settings: `My Package (hostname).sublime-settings`
- For Host/OS-level settings: `My Package (hostname on Windows).sublime-settings`

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
// My Package.sublime-settings
{
  "source": "User"
}
```

```javascript
// My Package (Windows).sublime-settings
{
  "source": "OS"
}
```

```javascript
// My Package (host1).sublime-settings
{
  "source": "Host"
}
```

```javascript
// My Package (host1 on Windows).sublime-settings
{
  "source": "OS/Host"
}
```

And you use:

    settings.get('source')

The value to get, given you use the machine with the hostname and OS
specified in the following table are:

| Hostname | OS      | Value   |
+----------+---------+---------+
| host1    | Windows | OS/Host |
| host1    | Linux   | Host    |
| host2    | Windows | OS      |
| host2    | Linux   | User    |
