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
	except:
		print "Connection error to database\n	->%s" % (conn_string)
		sys.exit()
		
	# psycopg2 creates a server-side cursor
	c_line = conn.cursor("c_account_move_line", cursor_factory=psycopg2.extras.DictCursor)
	c_move = conn.cursor()
	# CLEAR partner_id table account_move (optional)
	update_null="UPDATE account_move SET partner_id=null"
	c_move.execute(update_null)
	
	#c_line.execute("SELECT move_id, partner_id, credit, debit FROM account_move_line WHERE (partner_id > 0) ORDER by partner_id")
	c_line.execute("SELECT DISTINCT move_id, partner_id FROM account_move_line ORDER by partner_id")
	row_count = 0
	for row in c_line:
		row_count += 1
		update_line="UPDATE account_move SET partner_id=%s where id=%s"
		try:
			c_move.execute(update_line,(row[1],row[0],))
			print update_line
			print "Cursor_row:%s - Partner_id:%s - Move_id:%s" %(row_count, row[1], row[0],)
		except psycopg2.DatabaseError, e:
			print e.pgcode
			print e.pgerror
			sys.exit()
	c_move.execute("COMMIT")
	c_move.close()
	conn.close()
	print row_count


if __name__ == "__main__":
	main()

elapsed = (time.clock() - start)	
print "End Update - Time:%s" %(elapsed)
