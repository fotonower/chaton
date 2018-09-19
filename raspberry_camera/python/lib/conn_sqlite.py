__author__ = 'moilerat'

# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime

class SqlLiteConn():

    def __init__(self, filepath = "test.db"):
        self.con = lite.connect(filepath)

# A faire dans le destructeur ?

#        finally:
#            if self.con:
#                self.con.close()

    def upsertAndCommit(self, query):
        ret = None
        try :
            cur = self.con.cursor()
            ret = cur.execute(query)

            # VR 28-8-18 : needed for insert or update
            self.con.commit()

        except lite.Error as e:

            print ("Error :" + str(e))

        return ret

    def version(self):
        value = ""
        try :
            cur = self.con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')

            data = cur.fetchone()

            value = "SQLite version: " + str(data)

        except lite.Error as e:

            print ("Error :" + str(e))

        return value

    def list_tables(self):

        try :
            cur = self.con.cursor()


            query_search = "SELECT * FROM sqlite_master;"
            cur.execute(query_search)

            data = cur.fetchall()

            value = " All tables : " + str(data)

            print(value)

        except lite.Error as e:

            print ("Error :" + str(e))


# ON CONFLICT REPLACE ?

    def increment_counter(self, date, action, count, verbose = False):

            try :
                cur = self.con.cursor()
                query_search = "SELECT `id`, `counter` FROM `mra_cache_counter` WHERE `created_at`=\"" + str(date.strftime("%Y%m%d")) + "\" AND action=\"" + str(action) + "\""
                cur.execute(query_search)
                res = cur.fetchall()
                if res == None or len(res) == 0 :
                    query_insert = "INSERT INTO `mra_cache_counter` (`created_at`, `action`, `counter`) VALUES (" + date.strftime("%Y%m%d") + ",\"" + str(action) + "\" ," + str(count) + ") ;"

                    ret2 = self.upsertAndCommit(query_insert)
                    if verbose :
                        print(ret2)
                else :
                    id = int(res[0][0])
                    prev_counter = int(res[0][1])
                    new_counter = prev_counter + count
                    query_update = "UPDATE `mra_cache_counter` SET `counter`=" + str(new_counter) + " WHERE id = " + str(id)
                    self.upsertAndCommit(query_update)

            except lite.Error as e:
                print ("Error :" + str(e))

    def insert_photo(self, date, photopath, to_upload = 1):
        query = "INSERT INTO `mra_photos` (`day_taken_at`, `hour_taken_at`, `filename`, `to_upload`) VALUES (\"" + str(date.strftime("%Y%m%d")) + "\", \"" + str(date.strftime("%H:%M:%S")) + "\" , \"" + str(photopath) + "\", " + str(to_upload) + ")"
        self.upsertAndCommit(query)




    def retrieve_photo_id_local(self):

        try :
            cur = self.con.cursor()

            cur.execute('SELECT last_insert_rowid()')

            data = cur.fetchone()

            photo_id_local = int(data[0])

            return photo_id_local
        except lite.Error as e:

            print ("Error :" + str(e))

        return 0



    def insert_photo_id_portfolio(self, photo_id_local, portfolio_id):
        query = " INSERT INTO `mra_portfolio_photos` (`id_local_photo`, `portfolio_id`, `created_at`) VALUES ("+str(photo_id_local)+"," +str(portfolio_id)+ ", CURRENT_TIMESTAMP);"
        self.upsertAndCommit(query)




    def append_photo(self, photopath, date, portfolio_id = 0, to_upload = 1):

        self.insert_photo(date, photopath, to_upload)

        if portfolio_id != 0:
            photo_id_local = self.retrieve_photo_id_local()

            self.insert_photo_id_portfolio(photo_id_local, portfolio_id)

        self.increment_counter(date, "photo_taken", 1)



    def upload_one(self, photopath, date, photo_id_global):
        query = "UPDATE mra_photos SET uploaded_at = current_timestamp, photo_id_global = " + str(photo_id_global) + " WHERE filename=\"" + str(photopath) + "\";"
        self.upsertAndCommit(query)



    def create_portfolio(self, portfolio_id, portfolio_name, date, datou_ids = ""):

        query = "INSERT INTO mra_portfolios (`mtr_portfolio_id`, `name`, `created_at`, `datou_ids`) VALUES (" \
                + str(portfolio_id)\
                + ", \"" + str(portfolio_name)\
                + "\", \"" + str(date.strftime("%d/%m/%Y %H:%M:%S"))\
                + "\", \"" + datou_ids + "\" )"

        self.upsertAndCommit(query)



    def purge_created_before(self, purge_before):
        query_delete_photos = "DELETE FROM mra_photos WHERE day_taken_at<" + str(purge_before.strftime("%Y%m%d"))

        self.upsertAndCommit(query_delete_photos)


    def get_hashtag_id_from_hashtag_aux(self, hashtag):
        query = "SELECT hashtag_id_local FROM mra_hashtags WHERE hashtag=\"" + str(hashtag) + "\""

        try :
            cur = self.con.cursor()
            cur.execute(query)

            data = cur.fetchone()

            if len(data) == 0:
                return -1

            return data[0]

        except lite.Error as e:

            print ("Error :" + str(e))

        except Exception as e:

            print ("Exception :" + str(e))
        return -1

    def insert_hashtag(self, hashtag):
        query = "INSERT INTO `mra_hashtags` (`hashtag`) VALUES (\"" + str(hashtag) + "\") "
        self.upsertAndCommit(query)

    def get_hashtag_id_from_hashtag(self, hashtag):
        hashtag_id = self.get_hashtag_id_from_hashtag_aux(hashtag)
        if hashtag_id == -1 :
            self.insert_hashtag(hashtag)
            hashtag_id = self.get_hashtag_id_from_hashtag_aux(hashtag)

        return hashtag_id

    def get_photo_id_from_photo_path(self, filename):
        query = "SELECT id_local FROM mra_photos WHERE filename=\"" + str(filename) + "\""

        try :
            cur = self.con.cursor()
            cur.execute(query)

            data = cur.fetchone()

            return data[0]

        except lite.Error as e:

            print ("Error :" + str(e))

        except Exception as e:

            print ("Exception :" + str(e))
        return 0



     # MG question : veux t-on plutot le photo_id_local
    def tag_photo(self, filename, hashtag, type = 311) :
            hashtag_id = self.get_hashtag_id_from_hashtag(hashtag)
            photo_id_local = self.get_photo_id_from_photo_path(filename)

            query_insert = "INSERT INTO `mra_photo_hashtag_ids` (`photo_id_local`, `hashtag_id`, `type`) VALUES (" +\
                str(photo_id_local) + ", " + str(hashtag_id) + ", " + str(type) + ");"

            self.upsertAndCommit(query_insert)



    def to_upload(self, filename) :
            print ("ERROR, to_upload not supported yet !")



    def get_stat_day(self, previous_day):
        try :
            next_day = previous_day + datetime.timedelta(days=1)
            query_count = "SELECT count(*) FROM mra_photos WHERE day_taken_at BETWEEN \"" +\
            str(previous_day.strftime("%Y%m%d")) + "\" AND \"" +\
            str(next_day.strftime("%Y%m%d")) + "\""

            cur = self.con.cursor()
            cur.execute(query_count)

            data = cur.fetchone()

            return {"nb_photos" : data[0]}
        except Exception as e :
            print (str(e))

        return {"nb_photos":0}


    def get_pic_to_treat(self,limit):
        try :
            query_select = "SELECT * FROM mra_photos WHERE to_upload = 1"
            if limit != 0:
                query_select += " LIMIT " + str(limit)
            cur = self.con.cursor()
            cur.execute(query_select)
            data = cur.fetchall()
            return data
        except Exception as e:
            print(str(e))
            return []
# `hour_taken_at

    def set_pic_to_upload(self,list_ids):
        try:
            query_update = "UPDATE mra_photos SET to_upload = 2 where id in (" + ','.join(list_ids) + ");"
            cur = self.con.cursor()
            cur.upsertAndCommit(query_update)
        except Exception as e:
            print(str(e))

    def update_one(self,id,col= [],values = []):
        try:
            to_update = []
            for i in range(0,len(col)):
                to_update.append(col[i] + " = " + values[i])
            if len(to_update) > 0:
                query_update = "UPDATE mra_photos SET " + ','.join(to_update) + " where id = " + str(id)
                cur = self.con.cursor()
                cur.upsertAndCommit(query_update)
        except Exception as e:
            print(str(e))


    # VR needs maybe to be changed to be by name !
    def get_today_portfolio_id(self, date):
        return 0

    def delete_one(self,photo_path):
        query = "UPDATE mra_photos SET deleted_at = current_timestamp WHERE filename=\"" + str(photo_path) + "\";"
        self.upsertAndCommit(query)

def test(filename):
    sc = SqlLiteConn(filename)
    version = sc.version()
    print(" version : " + str(version))

if __name__ == "__main__" :
    print("To be tested")

    test("/Users/moilerat/Documents/Fotonower/data/sqlite_mtr_raspberry/raspberry.db")


