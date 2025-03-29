# RFC20232023

import loglin


fromClient = ['HELO','PASS','BALA','WDRA','BYE']
toClient = ['500 AUTH REQUIRE','525 OK!','401 ERROR!','AMNT','BYE']

def checkProtocol(data):
    dowhat = ''
    raw_data = data.strip()
    pName = raw_data.split(' ')[0]
    if pName in fromClient:
        print("Incoming type",pName)
        return data
    else:
        dowhat = 'Invalid Incoming'
        return dowhat


def handle(sentence,online: loglin.logDataBase):
    a = checkProtocol(sentence)
    parts = a.split()
    if len(parts)==2:   # 带有信息的请求
        id = parts[0]
        value = parts[1]
        print(value)
        print(a)
        if id == 'HELO':
            print('Hello')
            online.setID(value)
            return '500 AUTH REQUIRE'
        if id == 'PASS':
            online.setPass(value)
            return online.login()    
        if id == 'WDRA':
            if online.withdraw(value):
                return '525 OK!'
            if not online.withdraw(value):
                return '401 ERROR!'
        
        else:
            return 'Invalid'
    else:                   # 不带参数的请求 
        id = parts[0]
        if id == 'BALA':
            return 'AMNT'+' '+str(online.getAmount())
        if id == 'BYE':
            online.byeDatabase()
            return 'BYE'
        else:               # 无法识别的请求
            return 'Invalid'





