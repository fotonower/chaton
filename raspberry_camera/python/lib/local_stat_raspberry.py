__author__ = 'moilerat'

from conn_sqlite import SqlLiteConn as SLC
from conn_folder import FolderReadWrite as FRW

import datetime



class LocalStatRaspberry():

    def __init__(self, sqlfile = "", folder = ""):
        if sqlfile != "":
            self.sql_conn = SLC(sqlfile)
        else :
            self.sql_conn = None

        if folder != "":
            self.folder_read_write = FRW(folder)
        else :
            self.folder_read_write = None



    def append_photo(self, photopath, date = None, portfolio_id = 0):
        if date == None :
            date = datetime.datetime.now()

        if self.sql_conn != None:
            self.sql_conn.append_photo(photopath, date, portfolio_id)

        if self.folder_read_write != None :
            self.folder_read_write.append_photo(photopath, date)



    def create_portfolio(self, portfolio_id, port_name, date = None, datou_ids = ""):
        if date == None :
            date = datetime.datetime.now()

        if self.sql_conn != None:
            self.sql_conn.create_portfolio(portfolio_id, port_name, date)
        else :
            if datou_ids != "" :
                print ("ERROR : datou launching is not supported without sqlite !")

        if self.folder_read_write != None :
            self.folder_read_write.create_portfolio(portfolio_id, date)



    def upload_one(self, photopath, date = None, photo_id_global = 0):
        if date == None :
            date = datetime.datetime.now()

        if self.sql_conn != None:
            self.sql_conn.upload_one(photopath, date, photo_id_global)

        if self.folder_read_write != None :
            self.folder_read_write.upload_one(photopath, date)



    def purge_created_before(self, nb_day = 1):
        purge_before = datetime.datetime.now() - datetime.timedelta(days=nb_day)

        if self.sql_conn != None :
                self.sql_conn.purge_created_before(purge_before)
        else :
                print ("ERROR, purge_created_before not supported yet !")



     # MG quaestion : veux t-on plutot le photo_id_local
    def tag_photo(self, filename, hashtag) :
            if self.sql_conn != None :
                self.sql_conn.tag_photo(filename, hashtag)
            else :
                print ("ERROR, tag_photo not supported yet !")




    def to_upload(self, filename) :
            if self.sql_conn != None :
                self.sql_conn.to_upload(filename)
            else :
                print ("ERROR, to_upload not supported yet !")



    def get_stat_days(self, nb_day = 1):
        stats = []
        for i in range(0, nb_day):
            previous_day = datetime.datetime.now() - datetime.timedelta(days=i)

            if self.sql_conn != None :
                stat = self.sql_conn.get_stat_day(previous_day)
                stats.append(stat)
            else :
                print ("ERROR, get_stat_days not supported yet !")

        return stats

    def delete_one(self,photopath, date= None):
        if date == None :
            date = datetime.datetime.now()

        if self.sql_conn != None:
            self.sql_conn.delete_one(photopath)
        if self.folder_read_write != None :
            self.folder_read_write.delete_one(photopath, date)


def test(sqlfile, folder):
    import datetime

    current = datetime.datetime.now()

    lsr = LocalStatRaspberry(sqlfile, folder)

    lsr.sql_conn.list_tables()


    lsr.append_photo("test_path5")



    port_name = "suffix_20180808"

    port_id = 1000666

    print ("create_portfolio :")
    lsr.create_portfolio(port_id, port_name, current)



    print ("append_photo :")
    lsr.append_photo("test_path7", current, port_id)

    photo_id_global = 1667

    print ("upload_one :")
    lsr.upload_one("test_path1", None, photo_id_global)


    print ("purge_created_before :")
    lsr.purge_created_before(1)

    hashtag = "no_nageur"
    lsr.append_photo(filename, current, port_id)
    print ("tag_photo :")
    lsr.tag_photo(filename, hashtag) # MG quaestion : veux t-on plutot le photo_id_local
    print ("to_upload :")
    lsr.to_upload(filename)

    print ("get_stat_days :")
    stat = lsr.get_stat_days() #(s)
    print (str(stat))

    # TODO VR 28082018 :
    exit(0)



    print ("Test finished !")


if __name__ == "__main__" :
    print("To be tested")

    filename = "/Users/moilerat/Documents/Fotonower/data/sqlite_mtr_raspberry/raspberry.db"
    folder = "" # "~/.fotonower_config"

    test(filename, folder)
