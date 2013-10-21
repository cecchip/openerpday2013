#!/usr/bin/python
import xmlrpclib
import re
import time
import pdb
start = time.clock()
user = 'admin'
pwd = 'password'
dbname = 'acsi7demo'

sock = xmlrpclib.ServerProxy('http://localhost:40069/xmlrpc/common')
uid = sock.login(dbname ,user ,pwd)
try:
	sock = xmlrpclib.ServerProxy('http://localhost:40069/xmlrpc/object')
except:
	print "Connection Error"
#----------------------------------------------------------------------
# Read account_move_line
# SEARCH ID ACCOUNT MOVE LINE
args = [('state', '=', 'valid')]
ids = sock.execute(dbname, uid, pwd, 'account.move.line', 'search', args)
splitids=str(ids).split(',')
print splitids
rowcount=1
for row in splitids:
	if rowcount == len(ids):
		idmove = int(row[1:-1])
	else:
		idmove=int(row[1:])
	print idmove
	fields = ['partner_id','move_id'] #fields to read
	data = sock.execute(dbname, uid, pwd, 'account.move.line', 'read',idmove, fields) 
	splitdata = str(data).split(',')
	if splitdata[0][15:] <> 'False':
		idpartner = int(splitdata[0][16:])
		print data
		idmovew = int(splitdata[3][13::])
		print idpartner
		print idmovew
		fields1 = {'partner_id':idpartner,'membership_state':'invoiced'} #data to update ,'membership_state':'invoiced'
		result = sock.execute(dbname, uid, pwd, 'account.move', 'write', [idmovew], fields1) # Fault error idmovew - no error [idmovew]
		print result
	rowcount = rowcount+1
print rowcount
elapsed = (time.clock() - start)
print "End Update - Time:%s" %(elapsed)

