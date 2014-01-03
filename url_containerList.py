#!/usr/bin/env python

import pyrax
import pyrax.exceptions as exc
import sys


def pyrax_auth(username, apikey):
	try:
		pyrax.set_credentials(str(username), str(apikey))
		return True
	except exc.AuthenticationFailed:
		print "Authentication was not successful, please enter your username and API key from your Rackspace Control Panel"
		return False

def verify_input():
	if ( len(sys.argv) != 3 ):
		sys.exit('Usage: %s <username> <apikey>' % sys.argv[0])
	else:
		auth_test = pyrax_auth(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	verify_input()
	cdn_uri = raw_input("Enter your CDN URL: ")
	regions = ["ORD", "DFW","IAD"]
	print "Searching containers for " + cdn_uri + "..."
	for region_name in regions:
		cloud_files = pyrax.connect_to_cloudfiles(region=region_name)	
		for container in cloud_files.get_all_containers():
			container = cloud_files.get_container(container.name)
			print container.name
			print container.cdn_uri
			if (
				container.cdn_uri == cdn_uri or
				container.cdn_ssl_uri == cdn_uri or
				container.cdn_streaming_uri == cdn_uri
			):
				print "Container Found: " + container.name
				print "Listing Objects:"
				for object in container.get_objects():
					print " + " + object.name
				sys.exit(0)
	print "No matching container found with the URL: " + cdn_uri
	sys.exit(1)
			
