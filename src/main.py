import sys
from csv import reader
import socket
import ipaddress
import concurrent.futures

import fire

def _run(data):
    """
    
    """
    # NOTE: TCP-> SOCK_STREAM / UDP -> SOCK_DGRAM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return_code = s.connect_ex((data[0], int(data[1])))
        if return_code == 0:
            print(f"TO: {data[0]} Port: {int(data[1])} MSG: open!")
        else:
            print(f"TO: {data[0]} Port: {int(data[1])} MSG: not open!")

# TODO: csvで指定したpathの検査はできていない
def main(target_host='', ports='80,8080', csv=''):
    """
    
    """
    if csv:
        with open('sample.csv', 'r') as csv_file:
            csv_reader = reader(csv_file)
            list_of_rows = list(csv_reader)
            del list_of_rows[0]
            data = list_of_rows
    else:
        ports = [int(x) for x in ports.split(',')]
        if not target_host:
            target_host = input("Input target host name or address: ")
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
        results = excuter.map(_run, data)
    print("==================================================")
    print("Complete!")

def cli():
    """
    
    """
    fire.Fire(main)

if __name__ == "__main__":
    cli()