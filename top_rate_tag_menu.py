# -*- coding:utf-8 -*-

from __future__ import print_function
import MySQLdb, sys
"""
데이터 만들기 작업 이후 실시간 반영은 헤당 메뉴만 처리하면 됨!

선작업
    ALTER TABLE `napkin`.`tb_menu` ADD COLUMN `TOPRATE` VARCHAR(45) NULL  AFTER `REGDT` , ADD COLUMN `TOPRATE_RATE` DECIMAL(7,4) NULL  AFTER `TOPRATE` , ADD COLUMN `TOPWITH` VARCHAR(45) NULL  AFTER `TOPRATE_RATE` , ADD COLUMN `TOPWITH_RATE` DECIMAL(7,4) NULL  AFTER `TOPWITH` ;

tb_menu_rate_tag 값 추출 
    1. 1개이면 해당 메뉴에 대입
    2. 2개 이상이면 우열 가려서 최상위값 대입

우열
    1. awesome > good > soso > bad
    2. Napkin 수가 많은 순 
    
"""

def process1(colname):
    
    #TODO DB Connection Module 
    cnx = MySQLdb.connect('localhost', 'root', 'unicad10', 'napkin')
    cursor = cnx.cursor()
    
    query = ("select MENUCD, %sTAG, TAG_RATE from tb_menu_%s_tag where %sTAG<>'0' group by MENUCD having count(*)=1;" % (colname, colname, colname))
    print(query)
    #exit()
    
    try:
        cursor.execute(query)
        result = True
    except:
        print ("Unexpected error: " , sys.exc_info()[0] , sys.exc_info()[1])
        result = False

    print (result)
    #exit()
    
    if (result):
        
        sql = ('top_%s_tag.sql' % colname.lower())

        f = open(sql, 'w')
        cnx.commit()
        
        for row in cursor.fetchall():
            
            MENUCD = row[0]
            TAG = row[1]
            RATE = str(row[2])
            
            upt_query = ("update tb_menu set TOP%s='%s', TOP%s_RATE=%s where MENUCD=%d;\n" % (colname, TAG, colname, RATE, MENUCD) )
            print(upt_query)
            f.write(upt_query)
            
        f.close()
    
    
    cursor.close()
    cnx.close()

"""
@return result list
"""
def process2(colname):
    
    cnx = MySQLdb.connect('localhost', 'root', 'unicad10', 'napkin')
    cursor = cnx.cursor()
    
    query = ("select MENUCD from tb_menu_%s_tag where %sTAG<>'0' group by MENUCD having count(*)>1;" % (colname, colname))
    print(query)
    #exit()
    
    try:
        cursor.execute(query)
        result = True
    except:
        print ("Unexpected error: " , sys.exc_info()[0] , sys.exc_info()[1])
        result = False

    print (result)
    #exit()
    
    if (result):
        
        sql = ('top_%s_tag.sql' % colname.lower())

        f = open(sql, 'w')
        cnx.commit()
        
        return cursor.fetchall()
    
    
    cursor.close()
    cnx.close()
 

def process3(colname, rows):
    
    cnx = MySQLdb.connect('localhost', 'root', 'unicad10', 'napkin')
    cursor = cnx.cursor()
    
    sql = ('top_%s_tag_over2.sql' % colname.lower())
    
    f = open(sql, 'w')
    f.write('')
    f.close()
        
    for row in rows:
        if (colname == 'RATE'):
            query = ("select MENUCD, %sTAG, TAG_RATE from tb_menu_%s_tag where menucd=%d " 
                    " order by  "
                    "     case %stag " 
                    "     when 'awesome' then 1 " 
                    "     when 'awsome' then 1  "
                    "     when 'good' then 2 "
                    "     when 'soso' then 3 "
                    "     when 'So-So' then 3 "
                    "     when 'bad' then 4 "
                    "     else 10 end asc "
                    "     , TAG_CNT DESC "
                    "     , NAPKIN_CNT DESC "
                    "     limit 1;" % ( colname, colname, row[0], colname ))
            
        elif (colname == 'RATE'):
        
            query = ("select MENUCD, %sTAG, TAG_RATE from tb_menu_%s_tag where menucd=%d " 
                    " order by  "
                    "     case %stag " 
                    "     WHEN 'Alone' THEN 1 " 
                    "     WHEN 'Date' THEN 2 " 
                    "     WHEN 'Friends' THEN 3 " 
                    "     WHEN 'Family' THEN 4 " 
                    "     WHEN 'Business' THEN 5 " 
                    "     WHEN 'Party' THEN 6 " 
                    "     else 10 end asc "
                    "     , TAG_CNT DESC " 
                    "     , NAPKIN_CNT DESC "
                    "     limit 1;" % ( colname, colname, row[0], colname ))
        else:
            
            print("Wrong Element(colname)!")
            
            cursor.close()
            cnx.close()
    
            exit()
            
            
        #print(query)
        #exit()

        try:
            cursor.execute(query)
            result = True
        except:
            print ("Unexpected error: " , sys.exc_info()[0] , sys.exc_info()[1])
            result = False
    
        print (result)
        #exit()
        
        if (result):
            
                

    
            f = open(sql, 'a')
            cnx.commit()
            
            for row in cursor.fetchall():
                
                MENUCD = row[0]
                TAG = row[1]
                RATE = str(row[2])
                
                upt_query = ("update tb_menu set TOP%s='%s', TOP%s_RATE=%s where MENUCD=%d;\n" % (colname, TAG, colname, RATE, MENUCD) )
                print(upt_query)
                f.write(upt_query)
                
            f.close()
        

    cursor.close()
    cnx.close()

if __name__ == '__main__':
   
    colname = sys.argv[1]
    
    #1:1
    process1(colname)
    
    #1:Multi
    rows = process2(colname)
    process3(colname, rows)
    
    
    