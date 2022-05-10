import random
from flask import Flask, redirect,render_template,request,session
from web3 import Web3,HTTPProvider
import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtpObj=smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.login('tenderblockchain@gmail.com','m@keskilled')
otp_created=0

def connect_Blockchain_register(acc):
    blockchain_address="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address="0x483b82150bE2B7Ef3072DBC4683D40b5B1AdE25E"
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
    contract_address="0x095493D146c6F82e72F4854D598956cb7804DBA3"
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

@app.route('/bregisterUser',methods=['GET','POST'])
def bregisterUser():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_Blockchain_register(username)
    tx_hash=contract.functions.registerUser(username,int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(redirect('/blogin'))

@app.route('/bloginUser',methods=['GET','POST'])
def bloginUser():
    username=request.form['username']
    password=int(request.form['password'])
    print(username,password)
    contract,web3=connect_Blockchain_register(username)
    state=contract.functions.loginUser(username,password).call()
    if(state==True):
        session['username']=username
        return (redirect('/bdashboard'))
    else:
        return (redirect('/blogin'))

@app.route('/bdashboard')
def bdashboardPage():
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
            dummy.append('Tender Not Closed')
        else:
            dummy.append('Closed')
            dummy.append(tender_bidders[i])
        
        data.append(dummy)
    print(data)
    return render_template('bdashboard.html',len=len(data),dashboard_data=data)

@app.route('/blogout')
def blogoutPage():
    session.pop('username',None)
    return render_template('bindex.html')

@app.route('/bemail')
def bemail():
    return render_template('bemail.html')

@app.route('/createbid')
def bidPage():
    return render_template('bid.html')

@app.route('/sendOtp',methods=['GET','POST'])
def sendOTP():
    global otp_created
    otp_created=random.randint(1800,9999)
    email=request.form['email']
    print(email)
    msg = MIMEMultipart()
    msg['From'] = 'tenderblockchain@gmail.com'
    msg['To'] = email
    msg['Subject']= 'Your OTP as bidder registration'
    msg.attach(MIMEText("OTP to register: "+str(otp_created), 'plain'))
    text = msg.as_string()
    smtpObj.sendmail('tenderblockchain@gmail.com',msg['To'],text)
    session['bidderemail']=email
    return render_template('otp.html')

@app.route('/bidTender',methods=['GET','POST'])
def bidTenderPage():
    bidOwner=request.form['bidOwner']
    tenderId=request.form['tenderId']
    bidAmount=request.form['bidAmount']
    bidEmail=request.form['bidEmail']
    print(bidOwner,tenderId,bidAmount,bidEmail)
    contract,web3=connect_Blockchain(bidOwner)
    tx_hash=contract.functions.bidTender(int(tenderId),int(bidAmount),bidEmail).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return (redirect('/verifybid'))

@app.route('/verifybid')
def verifyBidPage():
    contract,web3=connect_Blockchain(session['username'])
    tender_owners,tender_ids,tender_datas,tender_statuses,tender_bidders=contract.functions.viewTenders().call()
    # print(tender_owners)
    # print(tender_ids)
    # print(tender_datas)
    # print(tender_statuses)
    # print(tender_bidders)
    bid_tender_ids,bid_emails,bidders,bidamounts=contract.functions.viewBids().call()
    # print(bid_tender_ids)
    # print(bid_emails)
    # print(bidders)
    # print(bidamounts)
    # print(session['username'])
    data=[]
    datai=[]
    for i in range(len(bid_tender_ids)):
        if session['username']==bidders[i]:
            datai.append(i)
    print(datai)
    for j in datai:
        dummy=[]
        dummy.append(bid_tender_ids[j])
        k=tender_ids.index(bid_tender_ids[j])
        dummy.append(tender_datas[k])
        dummy.append(bid_emails[j])
        dummy.append(bidders[j])
        dummy.append(bidamounts[j])
        if(tender_statuses[k]==False):
            dummy.append('In Progress')
        elif(tender_statuses[k]==True and tender_bidders[k]==session['username']):
            dummy.append('You Won')
        elif(tender_statuses[k]==True and tender_bidders[k]!=session['username']):
            dummy.append('You Lost')
        data.append(dummy)
    print(data)
    return (render_template('verifybid.html',len=len(data),dashboard_data=data))

@app.route('/')
def indexPage():
    return (render_template('index.html'))

@app.route('/register')
def registerPage():
    return (render_template('register.html'))

@app.route('/login')
def loginPage():
    return (render_template('login.html'))

@app.route('/finalbid')
def finalBidPage():
    return render_template('finalbid.html')

@app.route('/logout')
def logoutPage():
    session.pop('username',None)
    return render_template('index.html')

@app.route('/bids')
def bidsPage():
    contract,web3=connect_Blockchain(session['username'])
    tender_owners,tender_ids,tender_datas,tender_statuses,tender_bidders=contract.functions.viewTenders().call()
    # print(tender_owners)
    # print(tender_ids)
    # print(tender_datas)
    # print(tender_statuses)
    # print(tender_bidders)
    bid_tender_ids,bid_emails,bidders,bidamounts=contract.functions.viewBids().call()
    # print(bid_tender_ids)
    # print(bid_emails)
    # print(bidders)
    # print(bidamounts)
    # print(session['username'])
    data=[]
    datai=[]
    for i in range(len(tender_ids)):
        if session['username']==tender_owners[i]:
            datai.append(i)
    print(datai)
    for j in range(len(bid_tender_ids)):
        dummy=[]
        dummy.append(bid_tender_ids[j])
        k=tender_ids.index(bid_tender_ids[j])
        dummy.append(tender_datas[k])
        dummy.append(bid_emails[j])
        dummy.append(bidders[j])
        dummy.append(bidamounts[j])
        if(tender_statuses[k]==False):
            dummy.append('In Progress')
        elif(tender_statuses[k]==True):
            dummy.append('Tender Closed')
        
        data.append(dummy)
    print(data)
    return render_template('bids.html',len=len(data),dashboard_data=data)

@app.route('/allocate',methods=['GET','POST'])
def allocateBidtoTender():
    contract,web3=connect_Blockchain(session['username'])
    bid_tender_ids,bid_emails,bidders,bidamounts=contract.functions.viewBids().call()
    tenderId=request.form['tenderId']
    print(tenderId)
    print(bid_tender_ids)
    kIndexes=[]
    kBidAmounts=[]
    kBidEmails=[]
    kBidders=[]
    for i in range(len(bid_tender_ids)):
        if int(tenderId)==bid_tender_ids[i]:
            kBidAmounts.append(bidamounts[i])
            kBidEmails.append(bid_emails[i])
            kBidders.append(bidders[i])
    
    kMinBidAmount=min(kBidAmounts)
    kMinBidIndex=kBidAmounts.index(kMinBidAmount)
    bidderAddress=kBidders[kMinBidIndex]
    # print(kBidders)
    # print(kBidAmounts)
    # print(kBidEmails)
    # print(bidderAddress)

    # bidderAddress=request.form['bidderAddress']
    # print(tenderId,bidderAddress)
    # bidderIndex=bidders.index(bidderAddress)
    output=bidderAddress
    msg = MIMEMultipart()
    msg['From'] = 'tenderblockchain@gmail.com'
    msg['To'] = kBidEmails[kMinBidIndex]
    msg['Subject']= 'Your Bid for tender id ' +tenderId+' was finalised'
    msg.attach(MIMEText("Please arrange a prior meeting for the MoU as your bid was selected", 'plain'))
    text = msg.as_string()
    smtpObj.sendmail('tenderblockchain@gmail.com',msg['To'],text)
    contract,web3=connect_Blockchain(session['username'])
    tx_hash=contract.functions.allocateTender(int(tenderId),bidderAddress).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/dashboard')

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
            dummy.append('Tender Not Closed')
        else:
            dummy.append('Closed')
            dummy.append(tender_bidders[i])
        
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

    
if (__name__=='__main__'):
    app.run(debug=True)