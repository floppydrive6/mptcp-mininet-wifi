#!/usr/bin/python

"""
MPTCP performance test
created by:
Grzegorz Przybylo
University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
"""

import os
from time import sleep

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import RemoteController, OVSKernelSwitch


def topology(pathmanager, scheduler):
    #  distances at start:
    #  ap2 - ap3: 10.30m
    #  sta1 - ap2: 6.71m
    #  sta1 - ap3: 6.08m
    #  distances at the end:
    #  sta1 - ap2: 36.40m
    #  sta1 - ap3: 44.28m
    FOLDER_NAME = "n-n-ch1-ch6"
    "Create a network."
    net = Mininet(controller=RemoteController,
                  link=TCLink, switch=OVSKernelSwitch)
    net.start()
    print "*** Creating nodes"
    sta1 = net.addStation(
        'sta1', wlans=2, ip='10.0.0.10/8', position='30,10,0')
    ap2 = net.addAccessPoint('ap2', mac='00:00:00:00:00:02', equipmentModel='TLWR740N',
                             protocols='OpenFlow10', ssid='ssid_ap2', mode='n', channel='1', position='55,20,0')
    ap3 = net.addAccessPoint('ap3', mac='00:00:00:00:00:03', equipmentModel='TLWR740N',
                             protocols='OpenFlow10', ssid='ssid_ap3', mode='n', channel='6', position='50,11,0')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.254/8')
    h5 = net.addHost('h5', mac='00:00:00:00:00:05', ip='192.168.0.254/24')
    s6 = net.addSwitch('s6', mac='00:00:00:00:00:06', protocols='OpenFlow10')
    s7 = net.addSwitch('s7', mac='00:00:00:00:00:07', protocols='OpenFlow10')
    s8 = net.addSwitch('s8', mac='00:00:00:00:00:08', protocols='OpenFlow10')
    s9 = net.addSwitch('s9', mac='00:00:00:00:00:09', protocols='OpenFlow10')
    h10 = net.addHost('h10', mac='00:00:00:00:00:10', ip='192.168.1.254/24')
    c11 = net.addController('c11', controller=RemoteController, ip='127.0.0.1')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Associating and Creating links"
    net.addLink(ap2, sta1)
    net.addLink(ap3, sta1)
    net.addLink(ap2, h4, bw=100)
    net.addLink(ap3, h5, bw=100)  #
    net.addLink(s6, h4, bw=1000)
    net.addLink(s6, h5, bw=1000)  #
    net.addLink(s6, s7, bw=1000)  #
    net.addLink(s6, s8, bw=1000)
    net.addLink(s7, s9, bw=1000)  #
    net.addLink(s8, s9, bw=1000)
    net.addLink(s9, h10, bw=1000)

    h4.cmd('ifconfig h4-eth1 192.168.1.1/24')
    h5.cmd('ifconfig h5-eth1 192.168.1.2/24')

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10/8')
    sta1.cmd('ifconfig sta1-wlan1 192.168.0.10/24')

    sta1.cmd('ip route add default 10.0.0.254/8 via sta1-wlan0')
    sta1.cmd('ip route add default 192.168.0.254/24 via sta1-wlan1')

    sta1.cmd('ip rule add from 10.0.0.10 table 1')
    sta1.cmd('ip rule add from 192.168.0.10 table 2')

    sta1.cmd('ip route add 10.0.0.0 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 192.168.0.0 dev sta1-wlan1 scope link table 2')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-wlan1 table 2')

    sta1.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta1-wlan0')

    print"*** Plot graph ***"
    net.plotGraph(max_x=100, max_y=100)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=20, position='30.0,10.0,0.0')
    net.mobility(sta1, 'stop', time=120, position='90.0,30.0,0.0')
    net.stopMobility(time=120)

    print "*** Starting network"
    net.build()
    c11.start()
    s6.start([c11])
    s7.start([c11])
    s8.start([c11])
    s9.start([c11])
    ap2.start([c11])
    ap3.start([c11])

    h10.cmd('ip route add 10.0.0.0/8 via 192.168.1.1')
    h10.cmd('ip route add 192.168.0.0/24 via 192.168.1.2')

    h4.cmd('sysctl -w net.ipv4.ip_forward=1')
    h5.cmd('sysctl -w net.ipv4.ip_forward=1')

    # waiting till flows be registrated in POX controller
    sleep(10)

    name_postfix = pathmanager + '_' + scheduler
    # set path manager
    os.system('sysctl -w net.mptcp.mptcp_path_manager=' + pathmanager)
    # set scheduler
    os.system('sysctl -w net.mptcp.mptcp_scheduler=' + scheduler)
    #  wait for setting mptcp options
    sleep(2)

    print "starting simulation for path_manager: ", pathmanager, " and scheduler: ", scheduler

    # print"*** Plot graph ***"
    # net.plotGraph(max_x=100, max_y=100)

    # net.startMobility(time=0)
    # net.mobility(sta1, 'start', time=20, position='30.0,10.0,0.0')
    # net.mobility(sta1, 'stop', time=120, position='90.0,30.0,0.0')
    # net.stopMobility(time=120)

    print "*** Running CLI"
    CLI(net)

    # print "*** Running CLI"
    # CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology("fullmesh", "default")
