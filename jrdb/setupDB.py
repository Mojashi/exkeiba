#!python
# create table
# add primary index
# make generated column
from db.config import TableConfig, TableConfigs
from typing import List
import mysql.connector
from mysql.connector.cursor import CursorBase
import glob
import logging
from env import ProtoBuildDir
from secret import DB_USER, DB_HOST, DB_NAME, DB_PASS


def getConn():
    return mysql.connector.connect(
        user=DB_USER,
        host=DB_HOST,
        database=DB_NAME,
        password=DB_PASS)


def makeTable(cur: CursorBase):
    statements: List[str] = []
    for sqlFile in glob.glob(ProtoBuildDir + "/*.sql"):
        with open(sqlFile, "r") as f:
            statements.append(f.read())

    for stat in statements:
        cur.execute(stat)


def setup(cur: CursorBase, conf: TableConfig):
    for stat in conf.generatedColumns:
        logging.info("generatedColumn " + stat)
        cur.execute(f"ALTER TABLE {conf.name} ADD {stat}")
    stat = ",".join(conf.primaryKey)
    cur.execute(f"ALTER TABLE {conf.name} ADD PRIMARY KEY ({stat})")
    for idxName, cols in conf.indexes:
        stat = ",".join(cols)
        logging.info("addIndex " + idxName)
        cur.execute(f"ALTER TABLE {conf.name} ADD INDEX {idxName}({stat})")


def removeTables(cur: CursorBase):
    cur.execute("SHOW TABLES")
    tables = []
    for table in cur:
        tables.append(table)
    for (table,) in tables:
        logging.info("remove " + table)
        cur.execute("DROP TABLE %s" % table)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    conn = getConn()
    cur = conn.cursor()
    removeTables(cur)
    makeTable(cur)
    for conf in TableConfigs.values():
        setup(cur, conf)
