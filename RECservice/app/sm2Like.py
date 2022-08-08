from dbconnector import dbconnector as db
import os
import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta

def sm2like(quality,repetitions,previous_interval,previous_ef):

    if quality>=3:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 3
        else:
            interval = int(round(previous_interval * previous_ef))
        
        repetitions+=1
        easeFactor = previous_ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    else:
        repetitions = 0
        interval = 1
        easeFactor = previous_ef

    if (easeFactor < 1.3):
        easeFactor = 1.3
        
    return (interval,repetitions,easeFactor)


def calculate_sm2like(keyidList):
    dbobj = db()
    cursordb = dbobj.get_cursor()
    columns =['keyid','repetitions','quality','nxt_interval','previous_interval',
    'curr_ef','previous_ef','scheduled_date','displaying_date','curr_status','needs_update_flag','deleted_tag'
    ]
    in_params = ','.join(['%s'] * len(keyidList))
    Qr = '''SELECT %s FROM '''% ','.join(columns) + os.environ['MYSQL_TABLENAME']+ ''' WHERE keyid IN (%s)''' % in_params
    cursordb.execute(Qr,tuple(keyidList))
    df = DataFrame(cursordb.fetchall())
    

    if df.empty:
        print("empty df")
        return True

    df.columns = columns
    # print(df)
    base_Qr = '''UPDATE '''+os.environ['MYSQL_TABLENAME']
    for i in range(len(df)):
        # print(df.loc[i, "quality"],df.loc[i, "repetitions"],df.loc[i, "previous_interval"],df.loc[i, "previous_ef"])
        if int(df.loc[i, "quality"])>4:
            df.loc[i, "curr_status"]='inactive'
            df.loc[i, "repetitions"]=0
            df.loc[i, "previous_ef"]=2.5
            
        else:
            intrvl,repetn,easefctr = sm2like(float(df.loc[i, "quality"]),float(df.loc[i, "repetitions"]),
            float(df.loc[i, "previous_interval"]),float(df.loc[i, "previous_ef"]))
            df.loc[i, "previous_interval"],df.loc[i, "repetitions"],df.loc[i, "previous_ef"]=intrvl,repetn,round(easefctr,4)
            df.loc[i,'scheduled_date'] = datetime.date(datetime.today())+ timedelta(days=int(df.loc[i, "previous_interval"]))
            df.loc[i,'curr_status']='scheduled'
            df.loc[i, "quality"]=4

            if datetime.date(datetime.today())>=df.loc[i,'scheduled_date']:
                df.loc[i,'displaying_date']=datetime.date(datetime.today())
                df.loc[i, "curr_status"]='active'

        Qr=base_Qr+''' SET '''+ (' = %s ,').join(columns[1:]) + ' = %s '+'''WHERE keyid =%s '''%("'"+df.loc[i, "keyid"]+"'")
        # print(tuple(df.values[i][1:]))
        cursordb.execute(Qr,tuple(df.values[i][1:]))

    # print("new df\n ",df)
    dbobj.close_cnx()
    return True

def updateStatus():
    dbobj = db()
    cursordb = dbobj.get_cursor()
    columns =['keyid','repetitions','quality','nxt_interval','previous_interval',
    'curr_ef','previous_ef','scheduled_date','displaying_date','curr_status','needs_update_flag','deleted_tag'
    ]
    Qr = '''SELECT %s FROM '''% ','.join(columns) + os.environ['MYSQL_TABLENAME']+ ''' WHERE curr_status is NOT NULL AND curr_status NOT in ('inactive')'''
    cursordb.execute(Qr)
    df = DataFrame(cursordb.fetchall())
    

    if df.empty:
        print("df empty in updateStatus")
        return True

    df.columns = columns
    # print(df)
    base_Qr = '''UPDATE '''+os.environ['MYSQL_TABLENAME']
    update_required_list=[]
    for i in range(len(df)):
        if df.loc[i,'curr_status']=='scheduled' and datetime.date(datetime.today())>=df.loc[i,'scheduled_date']:
            df.loc[i, "curr_status"]='active'
            df.loc[i,'displaying_date']=datetime.date(datetime.today())
            update_required_list.append(df.loc[i,'keyid'])

        if df.loc[i,'curr_status']=='active' and df.loc[i,'scheduled_date']>datetime.date(datetime.today())>df.loc[i,'displaying_date']: 
            df.loc[i, "curr_status"]='scheduled'

        if df.loc[i,'curr_status']=='active' and df.loc[i,'scheduled_date']<=datetime.date(datetime.today()):
            df.loc[i,'displaying_date']=datetime.date(datetime.today())
            update_required_list.append(df.loc[i,'keyid'])

        Qr=base_Qr+''' SET '''+ (' = %s ,').join(columns[1:]) + ' = %s '+'''WHERE keyid =%s '''%("'"+df.loc[i, "keyid"]+"'")
        cursordb.execute(Qr,tuple(df.values[i][1:]))

    dbobj.close_cnx()
    if update_required_list:
        calculate_sm2like(update_required_list)
    
    return True


# if __name__=="__main__":
#     # print(sm2like(5,2,4,1.8))
#     # getUpdatedData(['2202-05791v2','2203-08777v3'])
#     updateStatus()


    