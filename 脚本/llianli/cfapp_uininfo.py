#!/usr/bin/env python
#-*- coding: utf-8 -*-
# ******************************************************************************
# 程序名称:     cfapp_uininfo.py
# 功能描述:     cfapp mac地址和uin对应关系
# 输入参数:     yyyymmdd    例如：20151208
# 目标表名:     
# 数据源表:     teg_mta_intf::ieg_lol
# 创建人名:     llianli
# 创建日期:     2015-12-08
# 版本说明:     v1.0
# 公司名称:     tencent
# 修改人名:
# 修改日期:
# 修改原因:
# ******************************************************************************


#import system module


# main entry
import datetime
import time


def TDW_PL(tdw, argv=[]):

    tdw.WriteLog("== begin ==")


    tdw.WriteLog("== argv[0] = " + argv[0] + " ==")

    sDate = argv[0]
    
    

    tdw.WriteLog("== sDate = " + sDate + " ==")


    tdw.WriteLog("== connect tdw ==")
    sql = """use ieg_qt_community_app"""
    res = tdw.execute(sql)

    sql = """set hive.inputfiles.splitbylinenum=true"""
    res = tdw.execute(sql)
    sql = """set hive.inputfiles.line_num_per_split=1000000"""
    res = tdw.execute(sql)


     ##创建表写数据
    sql = '''
      CREATE TABLE IF NOT EXISTS tb_cf_app_uininfo
(
fdate int,
id BIGINT,
uin_mac STRING,
uin STRING
)
                      '''
    tdw.WriteLog(sql)   
    res = tdw.execute(sql)


    

    sql = '''  DELETE FROM tb_cf_app_uininfo WHERE  fdate = %s '''%(sDate)
    tdw.WriteLog(sql)
    res = tdw.execute(sql)

 
    
    ##将每日的数据配置写入表中
    sql = ''' 
     INSERT TABLE tb_cf_app_uininfo

SELECT
%s,
id,
uin_mac,
uin
FROM
(
SELECT
id,
concat(ui,mc) AS uin_mac,
get_json_object(kv,'$.uin') AS uin
FROM teg_mta_intf::ieg_lol WHERE sdate =%s AND id in (1100679031,1200679031)
)t
WHERE uin IS NOT NULL           

    '''%(sDate,sDate)
    
    tdw.WriteLog(sql)
    res = tdw.execute(sql)
    

    tdw.WriteLog("== end OK ==")
    
    
    
    