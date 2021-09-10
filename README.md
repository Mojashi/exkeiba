# JRDB parser

1. fetch JRDB docs and data.
2. generate .proto files for each JRDB-doc.
3. convert JRDB data into protobuf format.
4. insert into mysql

## Requirements
- python3
- google-protobuf
- jrdb-account

## Usage
1. setup your db
```sql=
create database jrdb
create user jrdb@localhost
grant all on jrdb.* to jrdb@localhost
```
4. create secret.py
```python=
JRDB_USER_ID = "YOUR JRDB USERID"
JRDB_PASSWORD = "YOUR JRDB PASSWORD"
DB_USER = "jrdb"
DB_HOST = "localhost"
DB_NAME = "jrdb"
DB_PASS = ""
UNIXSOCKET = "/var/run/mysqld/mysqld.sock"
```

4. run
```sh=
make run
```
