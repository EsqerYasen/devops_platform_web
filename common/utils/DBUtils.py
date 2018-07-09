# coding:utf-8

import logging

'''
    公用查询方法
'''

logger = logging.getLogger('devops_appcenter')


def query(sql):
    from django.db import connection
    cursor = connection.cursor()
    row = {}
    try:
        print(sql)
        cursor.execute(sql, None)
        row = dictFetchAll(cursor)
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return row


def dict_query(sql):
    "将查询的结果集以字典数据结构返回"
    from django.db import connection
    cursor = connection.cursor()
    disc = {}
    try:
        cursor.execute(sql, None)
        for row in cursor.fetchall():
            disc[row[0]] = row[1]
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return disc


def dictFetchAll(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


'''
    分页查询
'''


def pageList(page, size, querySql, countSql):
    result = {'page': page, 'size': size}
    from django.db import connection
    cursor = connection.cursor()
    try:
        cursor.execute(countSql)
        countRow = dictFetchAll(cursor)
        count = countRow[0].values()[0]

        querySql = querySql + " limit %s,%s" % (page, size)
        cursor.execute(querySql)
        rows = dictFetchAll(cursor)

        result['total'] = count
        result['rows'] = rows
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return result


'''
    公用保存方法
'''


def save(sql):
    count = 0
    from django.db import connection
    cursor = connection.cursor()
    try:
        count = cursor.execute(sql)
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return count


'''
    公用删除方法
'''


def delete(sql):
    count = 0
    from django.db import connection
    cursor = connection.cursor()
    try:
        count = cursor.execute(sql)
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return count


'''
    公用更新方法
'''


def update(sql):
    count = 0
    from django.db import connection
    cursor = connection.cursor()
    try:
        count = cursor.execute(sql)
    except(Exception) as e:
        logging.error(str(e))
    finally:
        cursor.close()
        connection.close()
    return count
