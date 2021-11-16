# e2e_network_policy_checker
E2Eの通信テストで実施するツール

### 使い方
`e2e-network-policy-checker`コマンドを実行することで対象のIPへPortスキャンを実施できる。

```
# e2e-network-policy-checker

Input target host name or address: 192.168.1.1
==================================================
  target_ip port msg
192.168.1.1   80  OK
192.168.1.1 8080  NG
==================================================
Complete!
```
デフォルトで検査するポートは80/8080  
画面上へ表示のみ

e2e-network-policy-checkerを実行したディレクトリに.tmpディレクトリを作成し、e2e_network_policy_checker_result.csvを生成する

### オプション
#### オプションでIP,Portを指定
`e2e-network-policy-checker -t 192.168.1.1 -p 80,8080,443`

#### CSVファイルを用意して実施
`e2e-network-policy-checker --csv sample.csv`

`sample.csv`
```sample.csv
target_ip,port
192.168.1.1,80
192.168.1.1,8080
192.168.1.1,443
```

## 注意
自分の管理しているサーバ以外へのポートスキャンに利用しないでください。

## インストール
```
pip install git+https://github.com/ksaegusa/e2e_network_policy_checker.git
```