import mysql.connector
from flask import Flask, jsonify
from flask import abort
from time import gmtime, strftime
import numpy as np

try:
    sql_db = mysql.connector.connect(
        host="db",
        user="root",
        password="123",
        database="weight_testing_db"
    )
except mysql.connector.Error as err:
    print(f"{err}")

sql_cur = sql_db.cursor()

directions_to_use = {
    "in",
    "out",
    "none"
}

weight_unit_to_use = {
    "kg",
    "lbs"
}

def checkSyntax(direction, weight_unit, containers):
    if direction not in directions_to_use:
        abort(404, "direction {} doesn't exist".format(direction))

    if weight_unit not in weight_unit_to_use:
        abort(404, "weight unit {} doesn't exist".format(weight_unit))

    if not containers:
        abort(400, "must insert container")

# ---------------------------[MYSQL DATABASE AS OUTPUT]---------------------------------------
def getContainersWeight(containers, unit): # returns the total weight of all containers
    query = []
    query_value = []
    total = containers.count(',')
    if total:
        count = containers.split(',')
        for i in count:
            query.append("""SELECT weight FROM `containers` WHERE id = %s AND unit = %s""")
            query_value.append(i)
            query_value.append(unit)
    else:
        query.append("""SELECT weight FROM `containers` WHERE id = %s AND unit = %s""")
        query_value.append(containers)
        query_value.append(unit)

    res2 = sql_cur.execute(";".join(query), query_value, multi=True)
    output = 0
    for result in res2:
        if result.with_rows:
            for j in result:
                b = np.sum(j)
                output = output + b
    
    if not output:
        abort(404, "no containers found {}".format(containers))

    if unit == "lbs":
        output * 0.45359237 # convert LBS to KG

    return output

def getTruckWeight(truckid, unit):
    sql = "SELECT weight FROM `trucks` WHERE truckid = %s AND unit = %s"
    values = (f"{truckid}", f"{unit}")

    sql_cur.execute(sql, values)
    res = sql_cur.fetchall()
    if not res:
        return abort(404, "no trucks found {}".format(truckid))

    output = np.sum(res)
    
    if unit == "lbs":
        output * 0.45359237 # convert LBS to KG

    return output

def createSeasion(type, truck, containers, weight, unit, force, produce):
    if type == "in":
        sql = "SELECT direction FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        res = sql_cur.fetchall()
        fixed_str = np.squeeze(res)[()]
        lastid = 0
        if fixed_str == "in":
            if force:
                sql = "UPDATE `trucks` SET weight = %s WHERE truckid = %s"
                values = (f"{weight}", f"{truck}")
                sql_cur.execute(sql, values)
                sql_db.commit()
                print("update")
            else:
                abort(400, "force must be enabled for this action")
    elif type == "out":
        #sql = "SELECT * FROM `sessions` WHERE `trucks_id` = %s"
        #values = (f"{truckid}", )
        #sql_cur.execute(sql, values)
        #res = sql_cur.fetchall()
        #if not res:
        #    return print("err")

        sql = "SELECT direction FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        res = sql_cur.fetchall()
        fixed_str = np.squeeze(res)[()]
        lastid = sql_cur.lastrowid
        if res == "out":
            if force:
                sql = "UPDATE `trucks` SET weight = %s WHERE truckid = %s"
                values = (f"{weight}", f"{truck}")
                sql_cur.execute(sql, values)
                sql_db.commit()
                #print("update")
            else:
                abort(400, "force must be enabled for this action")
        else:
            abort(404, "'in' session not found")
    elif type == "none":
        sql = "SELECT direction FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        res = sql_cur.fetchall()
        fixed_str = np.squeeze(res)[()]
        if res == "in":
            abort(400, "none after in cannot be executed")

    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    truck_weight = getTruckWeight(truck, unit)
    cont_weight = getContainersWeight(containers, unit)
    neto = round(weight - truck_weight - cont_weight)
    sql = "INSERT INTO `sessions` (direction, f, date, bruto, neto, trucks_id, products_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (f"{type}", f"{force}", f"{currenttime}", f"{weight}", f"{neto}", f"{truck}", f"{produce}")
    #print(values)
    sql_cur.execute(sql, values)
    sql_db.commit()
    if type == "in" or type == "none":
        lastid = sql_cur.lastrowid
        return jsonify({'id': lastid, 'truck': truck, 'bruto': weight})
    elif type == "out":
        return jsonify({'id': lastid, 'truck': truck, 'bruto': weight, 'truckTara': bruto - neto, 'neto': neto})

def POSTweight(direction, truck, containers, weight, weight_unit, force, produce):
    checkSyntax(direction, weight_unit, containers)

    return createSeasion(direction, truck, containers, weight, weight_unit, force, produce)
    
# ---------------------------[CSV FILE AS OUTPUT]---------------------------------------
#def getContainer(containers, unit): # returns the total weight of all containers
#    total = containers.count(',')
#    if total:
#        count = containers.split(',')
#        for i in count:
#            choosenCont.append(i)
#    else:
#        choosenCont.append(containers)
#
#    if unit == "kg":
#        file_path = "weight_app/samples/containers1.csv"
#        row = "kg"
#    else:
#        file_path = "weight_app/samples/containers2.csv"
#        row = "lbs"
#
#    try: 
#        with open (file_path) as csvfile:
#            reader = csv.DictReader(csvfile)
#            for rows in reader:
#                cont_names.append(rows['id'])
#                cont_weight.append(int(rows[row]))
#    except:
#        abort(404, "no containers output for choosen unit")
#
#    output = 0
#    i = len(cont_names)
#    for ids in range(i):
#        if cont_names[ids] not in choosenCont:
#            continue
#        
#        output += cont_weight[ids]
#    
#    if not output:
#        abort(404, "no containers found {}".format(containers))
#    
#    return output