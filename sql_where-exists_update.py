#!/usr/bin/python
import psycopg2
import psycopg2.extras
import sys
import time
import config_psql as cp
start = time.clock()
def main():
	conn_string = "host=" + cp.host + " port=" + cp.port + " dbname=" + cp.dbname + " user=" + cp.user + " password="+ cp.password
	try:
		conn = psycopg2.connect(conn_string)
		# print the connection string we will use to connect
		print "Connecting to database\n	->%s" % (conn_string)
		cur = conn.cursor()
		# CLEAR partner_id table account_move (optional)
		update_null="UPDATE account_move SET partner_id=null"
		cur.execute(update_null)
		cur.execute("COMMIT")
		update_query="UPDATE account_move SET partner_id = (SELECT DISTINCT partner_id FROM account_move_line WHERE account_move.id = account_move_line.move_id) WHERE EXISTS (SELECT DISTINCT partner_id FROM account_move_line where account_move.id = account_move_line.move_id)"
		update_set = "UPDATE account_move SET partner_id = "
		update_select = "(SELECT DISTINCT partner_id FROM account_move_line WHERE account_move.id = account_move_line.move_id)"
		#update_select = "(SELECT partner_id FROM account_move_line WHERE account_move.id = account_move_line.move_id)"
		cur.execute(update_set + update_select + " WHERE EXISTS " + update_select)
		cur.execute("COMMIT")
		cur.close()
		conn.close()
	except psycopg2.DatabaseError, e:
			print e.pgcode
			print e.pgerror
			sys.exit()
	

if __name__ == "__main__":
	main()

elapsed = (time.clock() - start)
print "End Update - Time:%s" %(elapsed)
