import MySQLdb

def connection():
	conn=MySQLdb.connect(host="localhost",user="root", passwd="utkarsh@mit", db="legion")
	cur= conn.cursor()
	return cur, conn

def simulate_data():
	cur, conn = connection()
	name = "FullName"
	username = "username"
	suffix = "@gmail.com"
	location = "location"
	talk_points = "I am an alcoholic"
	for i in xrange(500000):
		q_name = name + str(i)
		q_username = username + str(i)
		email = username + str(i) + suffix
		q_location = location + str(i%50)
		cur.execute("INSERT into user_details values(%s, %s, %s, %s, %s)", (q_username, q_name, email, q_location, talk_points))
		cur.execute("INSERT into user_prefs(user_name) values(%s)", (q_username))
		is_online = str(0)
		cur.execute("INSERT into online_users values(%s, %s)", (q_username, 0))
		cur.execute("INSERT into user_problems values(%s, %s)", (q_username, talk_points))

	conn.commit()
	conn.close()
	cur.close()

# def modify_locations():
# 	cur, conn = connection()
# 	for i in xrange(500000):
# 		cur.execute("UPDATE user_details set location=%s where user_name=%s", (("location" + str(i%50)), ("username" + str(i))))
# 	conn.commit()
# 	conn.close()
# 	cur.close()


simulate_data()
#modify_locations()
