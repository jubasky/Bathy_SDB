__author__ = 'm'
# -*- coding: utf-8 -*-

# Classe para criar objecto para aceder à base de dados
# Toda a comunicação com a base de dados é feita por este
# objecto:
#
# - execução de scripts para construção da estrutura
#   da base de dados (tabelas, relações, partições, triggers, constraints)
#
# - queries, com leitura de informação para listas, arrays, etc.
#
# - operações de manutenção de tabelas
# - operações de manutenção das partições
#   Marcos Rosa 08/Nov/2015
# --------- Classe para ligar a base de dados

import psycopg2

class DB_Admin():

    # propriedade para guardar string de ligação à bd
    # para já, tem valor por defeito de:
    Db_str_conn="dbname='lidar' user='postgres' host='localhost' password='juba'"
    # propriedade para guardar objecto cursor (psycopg2)
    Db_cursor = None

    def set_connection(self, strcon):
        # permitir mudar a Db_conn
        if len(strcon)>0:
            self.Db_conn=strcon

    def ligar(self):
        print "Ligar-----------------" +  self.Db_str_conn

        self.Db_conn = psycopg2.connect(self.Db_str_conn)
        self.Db_cursor = self.Db_conn.cursor()
        print "Ligado!"

    def execute_sql(self, strsql):
        if len(strsql)>0:
            self.Db_cursor.execute(strsql)


    def ler_sql(self, strsql):
         if len(strsql)>0:
            self.Db_cursor.execute(strsql)
            resultado = self.Db_cursor.fetchall()
            return resultado

    def desligar(self):
        if self.Db_conn:
            self.Db_conn = None
