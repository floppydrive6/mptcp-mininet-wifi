#!/usr/bin/python

"""
MPTCP performance test
created by:
Grzegorz Przybylo
AGH University of Science and Technology in Cracow
Faculty of Computer Science, Electronics and Telecomunications
ICT
"""

import os
from time import sleep

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import RemoteController, OVSKernelSwitch


def topology(pathmanager, scheduler):
    #  distances:
    #  sta1 - ap2: 6.71m
    FOLDER_NAME = "refactored-iter5"
    "Create a network."
    net = Mininet(controller=RemoteController,
                  link=TCLink, switch=OVSKernelSwitch)
    net.start()
    print "*** Creating nodes"
    sta1 = net.addStation(
        'sta1', wlans=1, ip='10.0.0.10/8', position='49,17,0')
    ap2 = net.addAccessPoint('ap2', mac='00:00:00:00:00:02', equipmentModel='TLWR740N',
                             protocols='OpenFlow10', ssid='ssid_ap2', mode='n', channel='1', position='55,20,0')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04', ip='10.0.0.254/8')
    h5 = net.addHost('h5', mac='00:00:00:00:00:05', ip='192.168.0.254/24')
    h6 = net.addHost('h6', mac='00:00:00:00:00:11', ip='192.168.2.254/24')
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
    net.addLink(sta1, h5, bw=100)  # ethernet technology
    net.addLink(sta1, h6, bw=30, delay='10ms', loss=0.01)  # virtual link to set params on delay in one way, so RTT should be around 20ms
    net.addLink(ap2, h4, bw=100)  # delay='10ms')
    net.addLink(s6, h4, bw=1000)
    net.addLink(s6, h5, bw=1000)  #
    net.addLink(s6, h6, bw=1000)
    net.addLink(s6, s7, bw=1000)  #
    net.addLink(s6, s8, bw=1000)
    net.addLink(s7, s9, bw=1000)  #
    net.addLink(s8, s9, bw=1000)
    net.addLink(s9, h10, bw=1000)

    h4.cmd('ifconfig h4-eth1 192.168.1.1/24')
    h5.cmd('ifconfig h5-eth1 192.168.1.2/24')

    h6.cmd('ifconfig h6-eth1 192.168.1.3/24')

    # iw dev sta1-wlan0 disconnect
    # iw dev sta1-wlan1 connect ssid_ap2

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10/8')
    sta1.cmd('ifconfig sta1-eth1 192.168.0.10/24')
    sta1.cmd('ifconfig sta1-eth2 192.168.2.10/24')

    sta1.cmd('ip route add default 10.0.0.254/8 via sta1-wlan0')
    sta1.cmd('ip route add default 192.168.0.254/24 via sta1-eth1')
    sta1.cmd('ip route add default 192.168.2.254/24 via sta1-eth2')

    sta1.cmd('ip rule add from 10.0.0.10 table 1')
    sta1.cmd('ip rule add from 192.168.0.10 table 2')
    sta1.cmd('ip rule add from 192.168.2.10 table 3')

    sta1.cmd('ip route add 10.0.0.0 dev sta1-wlan0 scope link table 1')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('ip route add 192.168.0.0 dev sta1-eth1 scope link table 2')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-eth1 table 2')  # need to be added after putting up/down interface

    sta1.cmd('ip route add 192.168.2.0 dev sta1-eth2 scope link table 3')
    sta1.cmd('ip route add default via 192.168.2.254 dev sta1-eth2 table 3')  # need to be added after putting up/down interface

    # sta1.cmd('ip route add default scope global nexthop via 10.0.0.254 dev sta1-wlan0')

    sta1.cmd('ip route add default scope global nexthop via 192.168.2.254 dev sta1-eth2')
    #sta1.cmd('iw dev sta1-wlan0 disconnect')
    #sta1.cmd('ifconfig sta1-eth1 down')

    print "*** Starting network"
    net.build()
    c11.start()
    s6.start([c11])
    s7.start([c11])
    s8.start([c11])
    s9.start([c11])
    ap2.start([c11])

    h10.cmd('ip route add 10.0.0.0/8 via 192.168.1.1')
    h10.cmd('ip route add 192.168.0.0/24 via 192.168.1.2')
    h10.cmd('ip route add 192.168.2.0/24 via 192.168.1.3')

    h4.cmd('sysctl -w net.ipv4.ip_forward=1')
    h5.cmd('sysctl -w net.ipv4.ip_forward=1')
    h6.cmd('sysctl -w net.ipv4.ip_forward=1')

    # waiting till flows be registrated in POX controller
    sleep(10)

    name_postfix = pathmanager + '_' + scheduler
    # rm file, we are now appending to the end
    os.system('rm testtechnologies/' + FOLDER_NAME +
              '/client/iperf/client_' + name_postfix + '.log')
    os.system('rm testtechnologies/' + FOLDER_NAME +
              '/client/ifstat/ifstat_' + name_postfix + '.log')
    os.system('rm testtechnologies/' + FOLDER_NAME +
              '/client/proc/proc_' + name_postfix + '.log')
    os.system('rm testtechnologies/' + FOLDER_NAME +
              '/server/server_' + name_postfix + '.log')
    # set path manager
    os.system('sysctl -w net.mptcp.mptcp_path_manager=' + pathmanager)
    # set scheduler
    os.system('sysctl -w net.mptcp.mptcp_scheduler=' + scheduler)
    #  wait for setting mptcp options
    sleep(2)

    print "starting simulation for path_manager: ", pathmanager, " and scheduler: ", scheduler

    h10.cmd('iperf -s -i 1 >> testtechnologies/' + FOLDER_NAME +
            '/server/server_' + name_postfix + '.log &')
    sta1.cmd('iperf -c 192.168.1.254 -t 60 -i 1 >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log 2>&1 &')
    sta1.cmd('ifstat -b >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log 2>&1 &')

    # lets wait a moment
    sleep(3)

    # (older mptcp versions might have '/proc/net/mptcp')
    proc_path = '/proc/net/mptcp_net/mptcp'

    # and write some information about the current connection
    sta1.cmd('cat ' + proc_path + ' >> testtechnologies/' + FOLDER_NAME + '/client/proc/proc_' +
             name_postfix + '.log')

    sleep(11)

    sta1.cmd('ifconfig sta1-eth1 down')

    sta1.cmd('echo \"*** ethernet down ***\" >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log ')
    sta1.cmd('echo \"*** ethernet down ***\" >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log ')
    print "*** ethernet is down ***"

    sleep(7)

    sta1.cmd('ifconfig sta1-wlan0 0.0.0.0')

    sta1.cmd('echo \"*** wifi down ***\" >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log ')
    sta1.cmd('echo \"*** wifi down ***\" >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log ')
    print "*** wifi is down ***"

    sleep(7)

    sta1.cmd('ifconfig sta1-wlan0 10.0.0.10')
    sta1.cmd('ip route add default via 10.0.0.254 dev sta1-wlan0 table 1')

    sta1.cmd('echo \"*** wifi up ***\" >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log ')
    sta1.cmd('echo \"*** wifi up ***\" >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log ')
    print "*** wifi is up ***"

    sleep(7)

    sta1.cmd('ifconfig sta1-eth1 up')
    sta1.cmd('ip route add default via 192.168.0.254 dev sta1-eth1 table 2')

    sta1.cmd('echo \"*** ethernet up ***\" >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log ')
    sta1.cmd('echo \"*** ethernet up ***\" >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log ')
    print "*** ethernet is up ***"

    sleep(26)

    sta1.cmd('echo \"*** end of the test ***\" >> testtechnologies/' + FOLDER_NAME + '/client/iperf/client_' +
             name_postfix + '.log ')
    sta1.cmd('echo \"*** end of the test ***\" >> testtechnologies/' + FOLDER_NAME + '/client/ifstat/ifstat_' +
             name_postfix + '.log ')

    print "*** Stopping network"
    net.stop()
    sleep(1)


def mptcpTest():
    # enable MPTCP
    os.system('sysctl -w net.mptcp.mptcp_enabled=1')
    # enable debug output, execute "dmesg" to read output
    os.system('sysctl -w net.mptcp.mptcp_debug=0')

    scheduler = ["default", "roundrobin"]
    pathmanager = ["fullmesh"]
    # scheduler = ["default"]
    # pathmanager = ["fullmesh"]
    for pm in pathmanager:
        for sched in scheduler:
            topology(pm, sched)


if __name__ == '__main__':
    setLogLevel('warning')
    mptcpTest()
