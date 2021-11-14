from e2e_network_policy_checker.cli import cli, send_socket
import sys 
import os

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/"))

# TODO: csvのインポートのところとかテスト必要かな
# def test_cli():
#   assert cli(target_host='192.168.0.1', ports='80', csv='') == ['192.168.0.1,80, not open!']

def test_send_socket():
  assert send_socket(['192.168.0.1','80']) == '192.168.0.1,80,NG'
  assert send_socket(['192.168.0.1000','80']) == '192.168.0.1000,80,Input error target_ip=192.168.0.1000'
  assert send_socket(['192.168.0.1000.0','80']) == '192.168.0.1000.0,80,Input error target_ip=192.168.0.1000.0'
  assert send_socket(['192.168.0.1','80000']) == '192.168.0.1,80000,Input error port=80000'
  assert send_socket(['192.168.0.1','0.1']) == '192.168.0.1,0.1,Input error port=0.1'
