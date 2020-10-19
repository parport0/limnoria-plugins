An assortion of plugins for [Limnoria](https://github.com/ProgVal/Limnoria).

To add a plugin:
* place the plugin directory in your plugins/
* in your config file, add its name to `supybot.plugins`
* in your config file, add `supybot.plugins.<YourPluginName>: True` and `supybot.plugins.<YourPluginName>.public: True`
* all changes to the config file must be done when the bot *is not running* or else the changes might get erased
