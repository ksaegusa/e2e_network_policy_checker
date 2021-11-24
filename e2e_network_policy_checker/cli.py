import os
import sys
import socket
import ipaddress
import concurrent.futures

import click
import pandas as pd

from logging import basicConfig, getLogger, INFO
from configparser import ConfigParser
from csv import reader, writer

config = ConfigParser()
# TODO: 上書きでファイル指定できるようにする
config.read(os.path.dirname(os.path.abspath(__file__))+'/config.ini')

# TODO: ログの出力レベルをツール起動時に変更できるようにする
basicConfig(level=INFO)
logger = getLogger(__name__)

def send_socket(data):
    """
    
    """
    # NOTE: inputのチェック
    try:
      ipaddress.ip_address(data[0])
    except ValueError:
        logger.error(f"Input error target_ip={data[0]}")
        return [f"{data[0]}",f"{int(data[1])}",f"Input error target_ip={data[0]}"]

    try:
        int(data[1])
        if int(data[1]) > 65535:
            raise ValueError
    except ValueError:
        logger.error(f"Input error port={data[1]}")
        return [f"{data[0]}",f"{data[1]}",f"Input error port={data[1]}"]

    # NOTE: TCP-> SOCK_STREAM / UDP -> SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        logger.debug(f"START: {data[0]} {int(data[1])}")
        logger.debug(f"OPTION: timeout: {int(config['DEFAULT']['socket_timeout'])}")
        s.settimeout(int(config['DEFAULT']['socket_timeout']))
        return_code = s.connect_ex((data[0], int(data[1])))
        if return_code == 0:
            return [f"{data[0]}",f"{int(data[1])}","OK"]
        else:
            return [f"{data[0]}",f"{int(data[1])}","NG"]

def csv_export(df):
    _dir = config['DEFAULT']['save_result_dir']
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    filename = _dir + config['DEFAULT']['result_filename']
    df.to_csv(filename, sep=",",index=False)
    return print(f"Create -> {filename}")

def open_csv(csv):
    # TODO: csvのフォーマットのバリデーションチェックをする
    with open(csv, 'r') as csv_file:
        csv_reader = reader(csv_file)
        list_of_rows = list(csv_reader)
        del list_of_rows[0]
        data = list_of_rows
        return data

def input_user(target_host, ports):
    data = list()
    if not target_host:
        target_host = input("Input target address: ")
    try:
        ipaddress.ip_address(target_host)
    except ValueError:
        logger.error(f"Input error: {target_host}")
        sys.exit()

    if ',' in ports:
        ports = [int(x) for x in ports.split(',')]
        for i in ports:
            data.append([target_host,int(i)])
    else:
        data.append([target_host, int(ports)])
    return data

@click.command()
@click.option("-t","--target_host", type=str)
@click.option("-p","--ports", type=str, default='80,8080')
@click.option("-c","--csv", type=click.Path(exists=True, dir_okay=False))
@click.option("-l","--log", type=str, default='INFO')
def cli(target_host, ports, csv, log):
    """
    
    """
    logger.debug(f"SCRIPT START")
    if csv:
        data = open_csv(csv)

    else:
        data = input_user(target_host, ports)

    print("==================================================")
    logger.debug(f"SCRIPT START")
    with concurrent.futures.ProcessPoolExecutor(max_workers=int(config['DEFAULT']['process_workers'])) as excuter:
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