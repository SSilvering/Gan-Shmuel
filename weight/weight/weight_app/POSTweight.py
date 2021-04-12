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
        output *= 0.45359237 # convert LBS to KG

    return float(output)

def getTruckWeight(truckid, unit):
    sql = "SELECT weight FROM `trucks` WHERE truckid = %s AND unit = %s"
    values = (f"{truckid}", f"{unit}")

    sql_cur.execute(sql, values)
    res = sql_cur.fetchall()
    if not res:
        abort(404, "no trucks found {}".format(truckid))

    output = np.sum(res)
    
    if unit == "lbs":
        output *= 0.45359237 # convert LBS to KG

    return float(output)

def createSeasion(type, truck, containers, weight, unit, force, produce):
    update = False

    cont_weight = getContainersWeight(containers, unit)
    truck_weight = getTruckWeight(truck, unit)
    lastid = 0
    fixedstring = ""
    neto = 0
    trucktara = 0
    in_bruto = 0
    if type == "in":
        neto = int(float(weight) - truck_weight - cont_weight)
        trucktara = int(float(weight) - float(neto) - float(cont_weight))
        sql = "SELECT id,direction FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        if sql_cur.rowcount == 0:
            res = sql_cur.fetchall()
            for result in res:
                lastid = result[0]
                fixedstring = result[1]
            if fixedstring == "in":
                if force=="1":
                    sql = "UPDATE `trucks` SET weight = %s WHERE truckid = %s"
                    values = (f"{trucktara}", f"{truck}")
                    sql_cur.execute(sql, values)
                    sql_db.commit()
                    update = True
                else:
                    abort(400, "force must be enabled for this action")
    elif type == "out":
        sql = "SELECT id,direction,bruto FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        if sql_cur.rowcount == 0:
            res = sql_cur.fetchall()
            for result in res:
                in_bruto = result[2]
                lastid = result[0]
                fixedstring = result[1]
            trucktara = int(weight) - int(cont_weight)
            neto = int(int(in_bruto) - trucktara)
            if fixedstring == "out":
                sql = "SELECT bruto FROM `sessions` WHERE trucks_id = %s AND direction = 'in' ORDER BY id DESC LIMIT 1"
                sql_cur.execute(sql, (truck, ))
                res = sql_cur.fetchone()
                in_bruto = float(res[0])
                trucktara = float(in_bruto) - float(cont_weight) - float(neto)
                if force=="1":
                    sql = "UPDATE `trucks` SET weight = %s WHERE truckid = %s"
                    values = (f"{trucktara}", f"{truck}")
                    sql_cur.execute(sql, values)
                    sql_db.commit()
                    update = True
                else:
                    abort(400, "force must be enabled for this action")
        else: # if out witout in
            abort(400, "cannot create session without in")
    elif type == "none":
        sql = "SELECT direction FROM `sessions` WHERE trucks_id = %s ORDER BY id DESC LIMIT 1"
        sql_cur.execute(sql, (truck, ))
        res = sql_cur.fetchall()
        fixed_str = np.squeeze(res)[()]
        if fixed_str == "in":
            abort(400, "'in' cannot be after 'none'")
        else:
            neto = int(float(weight) - truck_weight - cont_weight)
            trucktara = int(float(weight) - float(neto))
    currenttime = strftime("%Y%m%d%H%M%S", gmtime())
    if not update:
        sql = "INSERT INTO `sessions` (direction, f, date, bruto, neto, trucks_id, products_id, containers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (f"{type}", f"{force}", f"{currenttime}", f"{weight}", f"{neto}", f"{truck}", f"{produce}", f"{containers}")
        sql_cur.execute(sql, values)
        sql_db.commit()
        if type == "in" or type == "none":
            lastid = sql_cur.lastrowid

    if unit == "lbs":
        weight = float(weight) * 0.45359237 # convert LBS to KG
        in_bruto = float(in_bruto) * 0.45359237 # convert LBS to KG
        neto = float(neto) * 0.45359237 # convert LBS to KG
    if type == "in" or type == "none":
        lastid = sql_cur.lastrowid
        return jsonify({'id': lastid, 'truck': truck, 'bruto': weight})
    elif type == "out":
        return jsonify({'id': lastid, 'truck': truck, 'bruto': in_bruto, 'truckTara': trucktara, 'neto': neto})

def POSTweight(direction, truck, containers, weight, weight_unit, force, produce):
    checkSyntax(direction, weight_unit, containers)

    return createSeasion(direction, truck, containers, weight, weight_unit, force, produce)
