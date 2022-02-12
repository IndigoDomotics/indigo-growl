# Growl Plugin
**Note**: Growl no longer works on macOS, this plugin is end-of-lifed.

The Growl Plugin for Indigo allows you to send growl messages via a plugin action in the Actions UI tab. Before you try to use this plugin you need to install [Growl](http://www.growl.info/). 

**Note**: In versions prior to Indigo 7.5, it was included in the installer. In December of 2020, the [macOS Growl project was retired](https://growl.github.io/growl/), so we decided to remove it from the installer and place it in our open source repo. We will no longer maintain it, but it's now open source so anyone with changes are welcome to submit pull requests on the GitHub repo for it.

**Note**: Version 1.0.5 and later of this plugin supports both Growl 1.2 and 1.3. However, you must select the correct version in the plugin preferences because the Growl API is specific to the version being used. 

## Notification Types


The Growl Plugin creates 8 "notifications", which show up in the Growl preference pane. You can customize each of these notification types as desired in Growl. You can also change the names (and remove them entirely if desired) via the plugin's preferences:

![growl_preferences](https://github.com/IndigoDomotics/indigo-growl/raw/main/growl_preferences.png)

By leaving any of the notifications blank, you can remove that notification type. It won't show up in the action config dialog or in Growl as a notification type. 

## Notification Action

When you're ready to send a notification, you just add a "Notification" action and adjust it's options via the action config dialog:

![growl_action_config](https://github.com/IndigoDomotics/indigo-growl/raw/main/growl_action_config.png)

There are 5 fields for each notify action described below

  - Type - this specifies the notification type (see above to configure those)
  - Title† - this is the title of the notification - typically shown at the top of the notification window
  - Description† - this is the description of the notification, typically shown in the main content area of the notification
  - Priority - that's the Growl-defined priority (not used by most Growl themes)
  - Sticky - that indicates whether the notification will require the user to manually close it or if Growl will close it automatically after some period of time

† - the title and description fields may contain substitution markup. So, as you can see from the example above, we're substituting the value of variable ID 867446802 in the title and variable ID 264884531 in the description. See [[variable_substitution|Substitutions]] for more information.

## Scripting Support

As with all plugins, actions defined by this plugin may be executed by [Python scripts](https://www.indigodomo.com/docs/plugin_scripting_tutorial#scripting_indigo_plugins). Here's the information you need to script the actions in this plugin.

**Plugin ID**: com.perceptiveautomation.indigoplugin.Airfoil

### Action specific properties

#### Notify

**Action id**: notify

Properties for scripting:

| Property   | Description                                                  |
| ---------- | ------------------------------------------------------------ |
| type       | the string key of the notification type, must be one of: 'notification1', 'notification2', 'notification3', 'notification4', 'notification5', 'notification6', 'notification7', 'notification7' and must be enabled in the preferences (see preferences above) |
| title      | the title of the growl notification                          |
| descString | the full text of the notification                            |
| priority   | the optional number priority for the notification: -2 (very low) through 2 (emergency) - defaults to 0 (normal priority) |
| sticky     | optional boolean that will cause the notification to stick (not automatically disappear) - defaults to False |

Example:

```python
growlPlugin = indigo.server.getPlugin("com.perceptiveautomation.indigoplugin.growl")
if growlPlugin.isEnabled():
	props = {
		'type':"notification1", 
		'title':"Growl Title", 
		'descString':"Description of Growl Notification", 
		'priority':0, 
		'sticky':False
	}
	growlPlugin.executeAction("notify", props=props)
```
