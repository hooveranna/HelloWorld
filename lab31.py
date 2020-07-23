#!/usr/bin/python

##oh boy here we go
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
pref = '/24'
r1IP = '10.2.2.1'
r2IP = '10.4.4.1'
r3IP = '10.6.6.1'
ir12IP = '10.9.9.1'
ir21IP = '10.9.9.2'
ir23IP = '10.7.7.2'
ir32IP = '10.7.7.1'
h1IP = '10.2.2.2/24'
h2IP = '10.4.4.4/24'
h3IP = '10.6.6.6/24'
hn1IP = '10.2.2.0/24'
hn2IP = '10.4.4.0/24'
hn3IP = '10.6.6.0/24'

class LinuxRouter( Node ):
	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )
	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()
class NetworkTopo( Topo ):
	def build( self, **_opts ):
		r1 = self.addNode( 'r1', cls=LinuxRouter, ip=r1IP+pref )
		r2 = self.addNode( 'r2', cls=LinuxRouter, ip=r2IP+pref )
		r3 = self.addNode( 'r3', cls=LinuxRouter, ip=r3IP+pref )
		h1 = self.addHost( 'Sam', ip=h1IP, defaultRoute='via '+r1IP )
		h2 = self.addHost( 'Emmy', ip=h2IP, defaultRoute='via '+r2IP )
		h3 = self.addHost( 'Bob', ip=h3IP, defaultRoute='via '+r3IP )
		self.addLink( h1, r1, intfName1='h1-eth0',intfName2='r1-eth0' )
		self.addLink( h2, r2, intfName1='h2-eth0',intfName2='r2-eth0' )
		self.addLink( h3, r3, intfName1='h3-eth0',intfName2='r3-eth0' )
		self.addLink( r1, r2, intfName1='r1-eth1', params1={'ip' : ir12IP+pref },
		intfName2='r2-eth1', params2={ 'ip' : ir21IP+pref } )
		self.addLink( r2, r3, intfName1='r2-eth2', params={ 'ip': ir23IP+pref },
		intfName2='r3-eth1', params2={ 'ip': ir32IP+pref } )
def run():
	topo = NetworkTopo()
	net = Mininet( topo=topo )
	net.start()
	info( net['r1'].cmd("ifconfig r1-eth1 "+ir12IP+pref) )
	info( net['r2'].cmd("ifconfig r2-eth1 "+ir21IP+pref) )
	info( net['r2'].cmd("ifconfig r2-eth2 "+ir23IP+pref) )
	info( net['r3'].cmd("ifconfig r3-eth1 "+ir32IP+pref) )
	info( net['r1'].cmd( "ip route add to {0} via {1} dev r1-eth1".format(hn2IP, ir21IP) ) )
	info( net['r1'].cmd( "ip route add to {0} via {1} dev r1-eth1".format(hn3IP, ir21IP) ) )
	info( net['r1'].cmd( "ip route add to {0} via {1} dev r1-eth1".format('10.7.7.0/24', ir21IP) ) )
	info( net['r2'].cmd( "ip route add to {0} via {1} dev r2-eth1".format(hn1IP, ir12IP) ) )
	info( net['r2'].cmd( "ip route add to {0} via {1} dev r2-eth2".format(hn3IP, ir32IP) ) )

	info( net['r3'].cmd( "ip route add to {0} via {1} dev r3-eth1".format(hn1IP, ir23IP) ) )
	info( net['r3'].cmd( "ip route add to {0} via {1} dev r3-eth1".format(hn2IP, ir23IP) ) )
	info( net['r3'].cmd( "ip route add to {0} via {1} dev r3-eth1".format('10.9.9.0/24', ir23IP) ) )
	info( '*** Routing Table on Routers:\n' )
	info( 'r1:\n')
	info( net[ 'r1' ].cmd( 'route' ) )
	info( '\nr2:\n')
	info( net[ 'r2' ].cmd( 'route' ) )
	info( '\nr3:\n')
	info( net[ 'r3' ].cmd( 'route' ) )
	CLI( net )
	net.stop()
if __name__ == '__main__':
	setLogLevel( 'info' )
	run()
