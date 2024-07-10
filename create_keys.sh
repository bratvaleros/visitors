cd /code
mkdir -p {ca_root,ca1}/{pub,priv,newcerts}
echo 1000 > ca_root/serial
echo 1000 > ca1/serial
touch  {ca_root,ca1}/{index.txt,openssl.conf}
mkdir ca1/{csr,psk12}

cd /code/ca_root
openssl genrsa -aes256 -out priv/ca.key 4096

cd /code/ca_root
openssl req -config openssl.conf -key priv/ca.key -new -x509 -days 7300 -sha256 -extensions v3_ca -out pub/ca.crt

export SAN=
cd /code/ca1
openssl genrsa -aes256 -out priv/ca1.key 4096

cd /code/ca1
openssl req -config openssl.conf -new -sha256 -key priv/ca1.key -out csr/ca1.csr

openssl ca -config /code/ca_root/openssl.conf -extensions v3_intermediate_ca -days 3650 -notext -md sha256 -in /code/ca1/csr/ca1.csr -out /code/ca1/pub/ca1.crt

cd /code/ca1
openssl genrsa -out priv/visitors.local.key 2048

openssl req -config openssl.conf -key priv/visitors.local.key -new -sha256 -out csr/visitors.local.csr

export SAN=DNS:visitors.local,IP:192.168.200.10
openssl ca -config openssl.conf -extensions server_cert -days 375 -notext -md sha256 -in csr/visitors.local.csr -out pub/visitors.local.crt

cat /code/ca1/pub/ca1.crt /code/ca_root/pub/ca.crt > /code/ca1/pub/ca1_chain.crt

cat /code/ca1/pub/visitors.local.crt /code/ca1/pub/ca1_chain.crt > /code/ca1/pub/visitors.local_chain.crt

