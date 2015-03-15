#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys
import yaml


log = logging.getLogger('gen')


class InstallGen(object):

	commands = ['error', 'user', 'repositories', 'packages', 'pythonpip', 'shell']

	def __init__(self, env, cyml):
		self.env = env
		with open(cyml) as f:
			self.ys = list(yaml.load_all(f))
		log.error(self.ys)

	def out(self, s=''):
		print s

	def script_header(self):
		out('#!/bin/bash')
		#out('set -eux')

	def matchenv(self, e):
		for k in self.env.keys():
			if k in e:
				if isinstance(e[k], list):
					if self.env[k] not in e[k]:
						return False
				elif self.env[k] != e[k]:
					return False
		return True

	def parse(self):
		for y in self.ys:
			self.parsedoc(y)
			self.out()

	def parsedoc(self, y):
		assert len(y) == 1
		for x in y.values()[0]:
			if not self.matchenv(x):
				log.debug('No match: %s', x)
				continue

			log.debug('Match: %s', x)
			invalid = set(x.keys()).difference(
				self.env.keys() + self.commands)
			if invalid:
				raise Exception('Invalid command(s): %s' % invalid)
			for cmd in self.commands:
				if cmd in x:
					self.process(cmd, x[cmd])

	def process(self, cmd, params):
		log.debug('Processing: %s', cmd)
		getattr(self, cmd)(params)

	def repositories(self, params):
		for p in params:
			m = re.match('[a-z]+://.+/([^/]+\.repo)$', p, re.I)
			if m:
				self.out('curl -o /etc/yum.repos.d/%s %s' % (m.group(1), p))
				continue

			m = re.match('.*([^/]+\.rpm)$', p, re.I)
			if m:
				self.out('yum -y install %s' % p)
				continue

			self.out('yum -y install %s' % p)

	def packages(self, params):
		if self.env['os'] in ('centos6', 'centos7'):
			self.out('yum -y install ' + ' '.join(params)) 

		if self.env['os'] in ('ubuntu1404', ):
			self.out('apt-get update')
			self.out('apt-get -y install %s' % ' '.join(params))

	def pythonpip(self, params):
		for p in params:
			self.out('pip install %s' % p)

	def shell(self, params):
		for p in params:
			self.out('%s' % p)

	def user(self, params):
		p = params
		self.out('if [ $(id -un) != %s ]; then echo '
			'"Must be run as user %s"; exit 1' % (p, p))

	def error(self, params):
		raise Exception('ERROR: %s' % params)


def main(env):
	defaultenv = {
		'os': 'centos6',
		'webserver': 'nginx',
		'omero': 5.0,
		#'webserver': 'apache-2.4',
	}
	defaultenv.update(env)
	igen = InstallGen(defaultenv, 'commands.yml')
	igen.parse()


if __name__ == '__main__':
	logging.basicConfig()
	#log.setLevel(logging.DEBUG)
	env = {}
	for arg in sys.argv[1:]:
		k, v = arg.split('=', 1)
		env[k] = v
	main(env)

