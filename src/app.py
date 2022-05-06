from flask import Flask, redirect,render_template,request,session
from web3 import Web3,HTTPProvider
import json

def connect_Blockchain_register(acc):
    blockchain_address="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address="0xdEa9286A2c200A795FB4d21A5D56292Ce4CDC8cE"
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

def connect_Blockchain(acc):
    blockchain_address="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/tender.json'
    contract_address="0xa794121Da749534db970D129743931fFd1a8F531"
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

app=Flask(__name__)
app.secret_key = 'makeskilled'

@app.route('/bid')
def bidIndexPage():
    return (render_template('bindex.html'))

@app.route('/bregister')
def bidRegisterPage():
    return (render_template('bregister.html'))

@app.route('/blogin')
def bidLoginPage():
    return (render_template('blogin.html'))

@app.route('/')
def indexPage():
    return (render_template('index.html'))

@app.route('/register')
def registerPage():
    return (render_template('register.html'))

@app.route('/login')
def loginPage():
    return (render_template('login.html'))

@app.route('/logout')
def logoutPage():
    session.pop('username',None)
    return render_template('index.html')
    
@app.route('/dashboard')
def dashboardPage():
    contract,web3=connect_Blockchain(session['username'])
    tender_owners,tender_ids,tender_datas,tender_statuses,tender_bidders=contract.functions.viewTenders().call()
    # print(tender_owners)
    # print(tender_ids)
    # print(tender_datas)
    # print(tender_statuses)
    # print(tender_bidders)
    data=[]
    for i in range(len(tender_owners)):
        dummy=[]
        dummy.append(tender_owners[i])
        dummy.append(tender_ids[i])
        dummy.append(tender_datas[i])
        if(tender_statuses[i]==False):
            dummy.append('Open')
        else:
            dummy.append('Closed')
        try:
            dummy.append(tender_bidders[i])
        except:
            dummy.append('Tender Not Closed')
        data.append(dummy)
    print(data)
        
    return(render_template('dashboard.html',len=len(data),dashboard_data=data))
    

@app.route('/tender')
def tenderPage():
    return(render_template('tender.html'))

@app.route('/registerUser',methods=['GET','POST'])
def registerUser():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_Blockchain_register(username)
    tx_hash=contract.functions.registerUser(username,int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(redirect('/login'))

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    username=request.form['username']
    password=int(request.form['password'])
    print(username,password)
    contract,web3=connect_Blockchain_register(username)
    state=contract.functions.loginUser(username,password).call()
    if(state==True):
        session['username']=username
        return (redirect('/dashboard'))
    else:
        return (redirect('/login'))

@app.route('/createTender',methods=['POST','GET'])
def createTender():
    tenderOwner=request.form['tenderOwner']
    tenderId=int(request.form['tenderId'])
    tenderData=request.form['tenderData']
    print(tenderId,tenderData,tenderOwner)
    contract,web3=connect_Blockchain(tenderOwner)
    tx_hash=contract.functions.createTender(tenderOwner,tenderId,tenderData).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return (redirect('/dashboard'))

@app.route('/tenders')
def tendersPage():
    contract,web3=connect_Blockchain(0)
    tender_owners,tender_ids,tender_datas,tender_statuses,tender_bidders=contract.functions.viewTenders().call()
    # print(tender_owners)
    # print(tender_ids)
    # print(tender_datas)
    # print(tender_statuses)
    # print(tender_bidders)
    data=[]
    for i in range(len(tender_owners)):
        dummy=[]
        dummy.append(tender_owners[i])
        dummy.append(tender_ids[i])
        dummy.append(tender_datas[i])
        if(tender_statuses[i]==False):
            dummy.append('Open')
        else:
            dummy.append('Closed')
        try:
            dummy.append(tender_bidders[i])
        except:
            dummy.append('Tender Not Closed')
        data.append(dummy)
    print(data)
        
    return(render_template('tenders.html',len=len(data),dashboard_data=data))

@app.route('/createBid')
def bidPage():
    return render_template('bid.html')
    
if (__name__=='__main__'):
    app.run(debug=True)