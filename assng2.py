#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
pref = '/24'
## adapters
hAMAC = ''
hBMAC = ''
hCMAC = ''
hDMAC = ''
hEMAC = ''
hFMAC = ''

## interfaces
ir12IP = '10.9.9.1'
ir21IP = '10.9.9.2'
ir23IP = '10.7.7.2'
ir32IP = '10.7.7.1'

## subnets
s1IP = '192.168.1.1/24'
s2IP = '192.168.2.2/24'
s3IP = '192.168.3.3/24'

sn1IP = '192.168.1.0/24'
sn2IP = '192.168.2.0/24'
sn3IP = '192.168.3.0/24'

## PLEASE WORK
class LinuxRouter( Node ):
	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )
	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()
class NetworkTopo( Topo ):
	def build( self, **_opts ):
		s1 = self.addNode( 's1', cls=LinuxRouter, ip=s1IP )
		s2 = self.addNode( 's2', cls=LinuxRouter, ip=s2IP )
		s3 = self.addNode( 's3', cls=LinuxRouter, ip=s3IP )

		ha = self.addHost( 'ada_a', MAC=hAMAC, defaultRoute='via '+s1IP )
		hb = self.addHost( 'ada_b', MAC=hBMAC, defaultRoute='via '+s1IP )
		hc = self.addHost( 'ada_c', MAC=hCMAC, defaultRoute='via '+s2IP )
		hd = self.addHost( 'ada_d', MAC=hDMAC, defaultRoute='via '+s2IP )
		he = self.addHost( 'ada_e', MAC=hEMAC, defaultRoute='via '+s3IP )
		hf = self.addHost( 'ada_f', MAC=hFMAC, defaultRoute='via '+s3IP )

		self.addLink( ha, s1, intfName1='ha-eth0',intfName2='s1-eth0' )
		self.addLink( hb, s1, intfName1='hb-eth0',intfName2='s1-eth1' )
		self.addLink( hc, s2, intfName1='hc-eth0',intfName2='s2-eth0' )
		self.addLink( hd, s2, intfName1='hd-eth0',intfName2='s2-eth1' )
		self.addLink( he, s3, intfName1='he-eth0',intfName2='s3-eth0' )
		self.addLink( hf, s3, intfName1='hf-eth0',intfName2='s3-eth1' )

		self.addLink( s1, s2, intfName1='s1-eth2', params1={'ip' : ir12IP+pref },
			intfName2='s2-eth2', params2={ 'ip' : ir21IP+pref } )
		self.addLink( s2, s3, intfName1='s2-eth3', params={ 'ip': ir23IP+pref },
			intfName2='s3-eth2', params2={ 'ip': ir32IP+pref } )

def run():
	topo = NetworkTopo()
	net = Mininet( topo=topo )
	net.start()
	info( net['s1'].cmd("ifconfig s1-eth2 "+ir12IP+pref) )
	info( net['s2'].cmd("ifconfig s2-eth2 "+ir21IP+pref) )
	info( net['s2'].cmd("ifconfig s2-eth3 "+ir23IP+pref) )
	info( net['s3'].cmd("ifconfig s3-eth2 "+ir32IP+pref) )

	info( net['s1'].cmd( "ip route add to {0} via {1} dev s1-eth2".format(sn2IP, ir21IP) ) )
	info( net['s1'].cmd( "ip route add to {0} via {1} dev s1-eth2".format(sn3IP, ir21IP) ) )
	info( net['s1'].cmd( "ip route add to {0} via {1} dev s1-eth2".format('10.7.7.0/24', ir21IP) ) )
	info( net['s2'].cmd( "ip route add to {0} via {1} dev s2-eth2".format(sn1IP, ir12IP) ) )
	info( net['s2'].cmd( "ip route add to {0} via {1} dev s2-eth3".format(sn3IP, ir32IP) ) )

	info( net['s3'].cmd( "ip route add to {0} via {1} dev s3-eth2".format(sn1IP, ir23IP) ) )
	info( net['s3'].cmd( "ip route add to {0} via {1} dev s3-eth2".format(sn2IP, ir23IP) ) )
	info( net['s3'].cmd( "ip route add to {0} via {1} dev s3-eth2".format('10.9.9.0/24', ir23IP) ) )



	info( '*** Routing Table on Routers:\n' )
	info( 's1:\n')
	info( net[ 's1' ].cmd( 'route' ) )
	info( '\ns2:\n')
	info( net[ 's2' ].cmd( 'route' ) )
	info( '\ns3:\n')
	info( net[ 's3' ].cmd( 'route' ) )
	CLI( net )
	net.stop()
if __name__ == '__main__':
	setLogLevel( 'info' )
	run()
