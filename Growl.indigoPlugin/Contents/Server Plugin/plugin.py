#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

################################################################################
# Python imports
import socket

# local imports
import Growl.Growl as OldGrowl
import gntp.notifier as NewGrowl

################################################################################
# Globals
################################################################################
# the ID we're using to identify the plugin to the media server
kApplicationName = "Indigo Plugin"
kIconFileName = "application.icns"

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        if "growlVersion" not in self.pluginPrefs:
            self.pluginPrefs["growlVersion"] = "1.3"
        self.debug = False

    ########################################
    # Get the notifications
    ########################################
    def getNotificationList(self, filter="", valuesDict=None, typeId="", targetId=0):
        itemsList = []
        note1 = self.pluginPrefs["notification1"]
        if note1 != "":
            itemsList.append(("notification1", note1))
        note2 = self.pluginPrefs["notification2"]
        if note2 != "":
            itemsList.append(("notification2", note2))
        note3 = self.pluginPrefs["notification3"]
        if note3 != "":
            itemsList.append(("notification3", note3))
        note4 = self.pluginPrefs["notification4"]
        if note4 != "":
            itemsList.append(("notification4", note4))
        note5 = self.pluginPrefs["notification5"]
        if note5 != "":
            itemsList.append(("notification5", note5))
        note6 = self.pluginPrefs["notification6"]
        if note6 != "":
            itemsList.append(("notification6", note6))
        note7 = self.pluginPrefs["notification7"]
        if note7 != "":
            itemsList.append(("notification7", note7))
        note8 = self.pluginPrefs["notification8"]
        if note8 != "":
            itemsList.append(("notification8", note8))
        return itemsList

    ########################################
    # Validate plugin prefs changes:
    ####################
    def validatePrefsConfigUi(self, valuesDict):
        self.debugLog(u"valuesDict: %s" % str(valuesDict))
        errorsDict = indigo.Dict()
        if valuesDict["notification1"] == "":
            errorsDict["notification1"] = "You must specify a value for this notification type"
        if valuesDict["notification2"] == "":
            errorsDict["notification2"] = "You must specify a value for this notification type"
        if valuesDict["notification3"] == "":
            errorsDict["notification3"] = "You must specify a value for this notification type"
        if valuesDict["notification4"] == "":
            errorsDict["notification4"] = "You must specify a value for this notification type"
        if valuesDict["notification5"] == "":
            errorsDict["notification5"] = "You must specify a value for this notification type"
        if valuesDict["notification6"] == "":
            errorsDict["notification6"] = "You must specify a value for this notification type"
        if valuesDict["notification7"] == "":
            errorsDict["notification7"] = "You must specify a value for this notification type"
        if valuesDict["notification8"] == "":
            errorsDict["notification8"] = "You must specify a value for this notification type"
        if len(errorsDict) > 0:
            return (False, valuesDict, errorsDict)
        return (True, valuesDict)

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        # Since they can change the notification list, we need to register those changes
        # with Growl
        self.debugLog(u"pluginPrefs: %s" % str(self.pluginPrefs))
        self.notify(None)

    ########################################
    # UI Validate, Close, and Actions defined in Actions.xml:
    ########################################
    def validateActionConfigUi(self, valuesDict, typeId, devId):
        errorsDict = indigo.Dict()
        validSubstitution = self.substitute(valuesDict['title'], validateOnly=True)
        if not validSubstitution[0]:
            errorsDict['title'] = validSubstitution[1]
        validSubstitution = self.substitute(valuesDict['descString'], validateOnly=True)
        if not validSubstitution[0]:
            errorsDict['descString'] = validSubstitution[1]
        if len(errorsDict) > 0:
            return (False, valuesDict, errorsDict)
        notificationList = self.getNotificationList()
        descString = "Growl Notification: "
        for tup in notificationList:
            if tup[0] == valuesDict['type']:
                descString += tup[1] + " - "
                break
        descString += valuesDict['title']
        valuesDict['description'] = descString
        return (True, valuesDict)

    ########################################
    def notify(self, action):
        self.debugLog(u"notify")
        updateOnly = (action is None)
        notificationList = self.getNotificationList()
        if updateOnly:
            typeString = notificationList[0][1]
            substitutedTitle = "Indigo Plugin Update"
            substitutedDescription = "The list of notifications for the Indigo Plugin was updated."
            growlPriority = 0
            growlSticky = False
        else:
            typeString = self.pluginPrefs[action.props["type"]]
            substitutedTitle = self.substitute(action.props.get("title", ""))
            substitutedDescription = self.substitute(action.props.get("descString", ""))
            try:
                growlPriority = int(action.props.get("priority", 0))
                growlSticky = bool(action.props.get("sticky", False))
            except:
                self.errorLog(u"Action is misconfigured")
                return
        if typeString != "":
            listToGrowl = []
            for key in notificationList:
                if self.pluginPrefs[key[0]] != "":
                    listToGrowl.append(key[1])
            growlVersion = self.pluginPrefs.get("growlVersion", "1.3")
            if growlVersion == "1.2":
                try:
                    theIcon = OldGrowl.Image.imageFromPath(kIconFileName)
                    growl = OldGrowl.GrowlNotifier(applicationName=kApplicationName, notifications=listToGrowl, applicationIcon=theIcon)
                    growl.register()
                    growl.notify(noteType=typeString,
                                 title=substitutedTitle,
                                 description=substitutedDescription,
                                 priority=growlPriority,
                                 sticky=growlSticky)
                except Exception, e:
                    self.errorLog(u"Unable to send Growl v1.2 Notification - make sure you have the correct version selected in the Growl plugin preferences\n%s" % str(e))
            elif growlVersion == "1.3":
                try:
                    growl = NewGrowl.GrowlNotifier(applicationName=kApplicationName, notifications=listToGrowl, applicationIcon="http://static.indigodomo.com/www/images/growlicon_64x64.png")
                    growl.register()
                    growl.notify(noteType=typeString,
                                 title=substitutedTitle,
                                 description=substitutedDescription,
                                 priority=growlPriority,
                                 sticky=growlSticky)
                except socket.error, e:
                    if e.errno == 61:   # Connection refused, very likely they don't have the Growl app running.
                        self.errorLog(u"Unable to send Growl Notification - make sure the Growl application is running.")
                    else:
                        self.errorLog(u"Unable to send Growl Notification - make sure you have the correct version selected in the Growl plugin preferences\n" + str(e))
                except Exception, e:
                    self.errorLog(u"Unable to send Growl Notification - make sure you have the correct version selected in the Growl plugin preferences\n" + str(e))
            else:
                self.errorLog(u"Unknown Growl version")
            return
        else:
            self.errorLog(u"Action is configured with a notification that has been disabled - reconfigure the action")
