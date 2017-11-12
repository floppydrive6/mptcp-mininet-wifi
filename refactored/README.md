# MPTCP performance analysis
In this project MPTCP is tested in several topologies and cases in [mininet-wifi](https://github.com/intrig-unicamp/mininet-wifi) emulator.

## Requirements
To run this tests you have to have mininet-wifi installed.<br>Also you have to have (P)OX OpenFlow Controller installed. You can add `-p` option while installing mininet-wifi. Also [mptcp-kernel](https://www.multipath-tcp.org/) and `ifstat` have to be installed. While compiling your own mptcp-kernel from source code do not forget to install also RoundRobin scheduler

## Running tests
1. turn off network-manager: `sudo service network-manager stop`<br>
2. run (P)OX controller with:<br>`cd pox_directory` and then `sudo ./pox.py forwarding.l2_learning openflow.spanning_tree --hold-down --no-flood openflow.discovery host_tracker`<br>
3. go to directory of this repo e.g.: `cd mptcp-mininet-wifi/refactored`, then go to proper test case folder and run `sudo python test-name.py`
