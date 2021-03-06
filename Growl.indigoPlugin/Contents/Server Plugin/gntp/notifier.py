"""
The gntp.notifier module is provided as a simple way to send notifications
using GNTP

.. note::
	This class is intended to mostly mirror the older Python bindings such
	that you should be able to replace instances of the old bindings with
	this class.
	`Original Python bindings <http://code.google.com/p/growl/source/browse/Bindings/python/Growl.py>`_

"""
import gntp
import socket
import logging

logger = logging.getLogger(__name__)

def mini(description, applicationName='PythonMini', noteType="Message",
			title="Mini Message", applicationIcon=None, hostname='localhost',
			password=None, port=23053, sticky=False, priority=None):
	"""Single notification function

	Simple notification function in one line. Has only one required parameter
	and attempts to use reasonable defaults for everything else
	:param string description: Notification message
	"""
	growl = GrowlNotifier(
		applicationName=applicationName,
		notifications=[noteType],
		defaultNotifications=[noteType],
		hostname=hostname,
		password=password,
		port=port,
	)
	result = growl.register()
	if result is not True:
		return result

	return growl.notify(
		noteType=noteType,
		title=title,
		description=description,
		icon=applicationIcon,
		sticky=sticky,
		priority=priority,
	)

class GrowlNotifier(object):
	"""Helper class to simplfy sending Growl messages

	:param string applicationName: Sending application name
	:param list notification: List of valid notifications
	:param list defaultNotifications: List of notifications that should be enabled
		by default
	:param string applicationIcon: Icon URL
	:param string hostname: Remote host
	:param integer port: Remote port
	"""

	passwordHash = 'MD5'

	def __init__(self, applicationName='Python GNTP', notifications=[],
			defaultNotifications=None, applicationIcon=None, hostname='localhost',
			password=None, port=23053):

		self.applicationName = applicationName
		self.notifications = list(notifications)
		if defaultNotifications:
			self.defaultNotifications = list(defaultNotifications)
		else:
			self.defaultNotifications = self.notifications
		self.applicationIcon = applicationIcon

		self.password = password
		self.hostname = hostname
		self.port = int(port)

	def _checkIcon(self, data):
		'''
		Check the icon to see if it's valid
		@param data:
		@todo Consider checking for a valid URL
		'''
		return data

	def register(self):
		"""Send GNTP Registration

		.. warning::
			Before sending notifications to Growl, you need to have
			sent a registration message at least once
		"""
		logger.info('Sending registration to %s:%s', self.hostname, self.port)
		register = gntp.GNTPRegister()
		register.add_header('Application-Name', self.applicationName)
		for notification in self.notifications:
			enabled = notification in self.defaultNotifications
			register.add_notification(notification, enabled)
		if self.applicationIcon:
			register.add_header('Application-Icon', self.applicationIcon)
		if self.password:
			register.set_password(self.password, self.passwordHash)
		return self._send('register', register.encode())


	def notify(self, noteType, title, description, icon=None, sticky=False, priority=None):
		"""Send a GNTP notifications

		.. warning::
			Must have registered with growl beforehand or messages will be ignored

		:param string noteType: One of the notification names registered earlier
		:param string title: Notification title (usually displayed on the notification)
		:param string description: The main content of the notification
		:param string icon: Icon URL path
		:param boolean sticky: Sticky notification
		:param integer priority: Message priority level from -2 to 2
		"""
		logger.info('Sending notification [%s] to %s:%s', noteType, self.hostname, self.port)
		assert noteType in self.notifications
		notice = gntp.GNTPNotice()
		notice.add_header('Application-Name', self.applicationName)
		notice.add_header('Notification-Name', noteType)
		notice.add_header('Notification-Title', title)
		if self.password:
			notice.set_password(self.password, self.passwordHash)
		if sticky:
			notice.add_header('Notification-Sticky', sticky)
		if priority:
			notice.add_header('Notification-Priority', priority)
		if icon:
			notice.add_header('Notification-Icon', self._checkIcon(icon))
		if description:
			notice.add_header('Notification-Text', description)
		return self._send('notify', notice.encode())

	def subscribe(self, id, name, port):
		"""Send a Subscribe request to a remote machine"""
		sub = gntp.GNTPSubscribe()
		sub.add_header('Subscriber-ID', id)
		sub.add_header('Subscriber-Name', name)
		sub.add_header('Subscriber-Port', port)
		if self.password:
			sub.set_password(self.password, self.passwordHash)
		return self._send('subscribe', sub.encode())

	def _send(self, type, data):
		"""Send the GNTP Packet"""
		logger.debug('To : %s:%s <%s>\n%s', self.hostname, self.port, type, data)

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.hostname, self.port))
		s.send(data.encode('utf8', 'replace'))
		response = gntp.parse_gntp(s.recv(1024))
		s.close()

		logger.debug('From : %s:%s <%s>\n%s', self.hostname, self.port, response.__class__, response)

		if response.info['messagetype'] == '-OK':
			return True
		logger.error('Invalid response: %s', response.error())
		return response.error()

if __name__ == '__main__':
	mini('Testing mini notification')

