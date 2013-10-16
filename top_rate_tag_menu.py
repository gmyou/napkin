# -*- coding:utf-8 -*-

from __future__ import print_function
import MySQLdb, sys
"""
데이터 만들기 작업 이후 실시간 반영은 헤단 메뉴만 처리하면 됨!

선작업
    ALTER TABLE `napkin`.`tb_menu` ADD COLUMN `TOPRATE` VARCHAR(45) NULL  AFTER `REGDT` , ADD COLUMN `TOPRATE_RATE` DECIMAL(7,4) NULL  AFTER `TOPRATE` , ADD COLUMN `TOPWITH` VARCHAR(45) NULL  AFTER `TOPRATE_RATE` , ADD COLUMN `TOPWITH_RATE` DECIMAL(7,4) NULL  AFTER `TOPWITH` ;

tb_menu_rate_tag 값 추출 
    1. 1개이면 해당 메뉴에 대입
    2. 2개 이상이면 우열 가려서 최상위값 대입

우열
    1. awesome > good > soso > bad
    2. Napkin 수가 많은 순 
    
"""

#tablename = "tb_menu_rate_tag"
#colname = "RATE"
tablename = "tb_menu_with_tag"
colname = "WITH"

cnx = MySQLdb.connect('localhost', 'root', 'unicad10', 'napkin')
cursor = cnx.cursor()

def dbClose():
    cursor.close()
    cnx.close()

def process1():
    
    global cnx
    global cursor
    
    global tablename
    global colname
    
    query = ("select MENUCD, %sTAG, TAG_RATE from %s where %sTAG<>'0' group by MENUCD, %sTAG having count(*)=1" % (colname, tablename, colname, colname))
    print(query)
    
    #exit()
    try:
        cursor.execute(query)
        result = True
    except:
        print ("Unexpected error: " , sys.exc_info()[0] , sys.exc_info()[1])
        result = False

    #print (result)
    
    
    if (result):
        
        sql = ('top_%s_tag.sql' % colname.lower())
        f = open(sql, 'w')
        cnx.commit()
        
        for row in cursor.fetchall():
            
            MENUCD = row[0]
            TAG = row[1]
            RATE = str(row[2])
            
            """
            #upt_query = "update tb_menu set TOPRATE='"+str(row[1])+"', TOPRATE_RATE="+str(row[2])+" where MENUCD="+str(row[0])+';\n'
            """
            upt_query = ("update tb_menu set TOP%s='%s', TOP%s_RATE=%s where MENUCD=%d;\n" % (colname, TAG, colname, RATE, MENUCD) )
            print(upt_query)
            f.write(upt_query)
            
        f.close()
    
    
    dbClose()


if __name__ == '__main__':
   
    process1()