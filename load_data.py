from checkin import Checkin
import sqlite3
import DAO
def load_checkin():
    checkin_file = '../brightkite/Brightkite_totalCheckins.txt'

    with open(checkin_file, "r") as f2 :
        conn = sqlite3.connect('brightkite.db')
        c = conn.cursor()
        i = 0
        lines = f2.readlines()
        for line in lines:
            i+=1
            if i%10000 == 0:
                print(i)
            line0 = line.strip().split()
            if len(line0) == 5:
                usr_id, checkin_time, latitude,longitude, loc_id = line.strip().split()
                if loc_id=='0':
                    continue
                checkin_time = checkin_time[:-1]
                checkin = Checkin(user = usr_id,location_id = loc_id,checkin_time = checkin_time,latitude = latitude,longitude = longitude)
                
                DAO.execute_checkin(c,checkin)
        conn.commit()


                







if __name__ == '__main__':
    DAO.generate_db()
    
    load_checkin()
    DAO.add_index()

