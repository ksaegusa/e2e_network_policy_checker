import os
import sys
from csv import reader, writer
import socket
import ipaddress
import concurrent.futures

import click
import pandas as pd

def send_socket(data):
    """
    
    """
    # NOTE: inputのチェック
    try:
      ipaddress.ip_address(data[0])
    except ValueError:
        return [f"{data[0]}",f"{int(data[1])}",f"Input error target_ip={data[0]}"]

    try:
        int(data[1])
        if int(data[1]) > 65535:
            raise ValueError
    except ValueError:
        return [f"{data[0]}",f"{data[1]}",f"Input error port={data[1]}"]

    # NOTE: TCP-> SOCK_STREAM / UDP -> SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return_code = s.connect_ex((data[0], int(data[1])))
        if return_code == 0:
            return [f"{data[0]}",f"{int(data[1])}","OK"]
        else:
            return [f"{data[0]}",f"{int(data[1])}","NG"]

def csv_export(df):
    _dir = ".tmp"
    if not os.path.exists(_dir):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(_dir)
    filename = _dir + "/e2e_network_policy_checker_result.csv"
    df.to_csv(filename, sep=",",index=False)
    return print(f"Create -> {filename}")

@click.command()
@click.option("-t","--target_host", type=str)
@click.option("-p","--ports", type=str, default='80,8080')
@click.option("-c","--csv", type=click.Path(exists=True, dir_okay=False))
def cli(target_host, ports, csv):
    """
    
    """
    if csv:
        with open(csv, 'r') as csv_file:
            csv_reader = reader(csv_file)
            list_of_rows = list(csv_reader)
            del list_of_rows[0]
            data = list_of_rows
    else:
        if ',' in ports:
            ports = [int(x) for x in ports.split(',')]
        else:
            ports = int(ports)
        if not target_host:
            target_host = input("Input target address: ")
        try:
            ipaddress.ip_address(target_host)
        except ValueError:
            print(f"Input error: {target_host}")
            sys.exit()
        data = list()
        for i in ports:
            data.append([target_host,int(i)])
    print("==================================================")
    with concurrent.futures.ProcessPoolExecutor(max_workers=100) as excuter:
        results = excuter.map(send_socket, data)
        _ip,_port,_msg = list(), list(), list()
        for res in list(results):
            _ip.append(res[0])
            _port.append(res[1])
            _msg.append(res[2])

        data = dict(
            target_ip=_ip,
            port=_port,
            msg=_msg
        )

        df = pd.DataFrame(data=data)
        print(df.to_string(index=False))
    print("==================================================")

    csv_export(df)

if __name__ == "__main__":
    cli()