import fotonower as FC
import os
import datetime
import shutil
import sys
if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--folder", action="store", type="string", dest="folder", default="/home/pi/Desktop/images",
                      help="folder where are photo to upload")
    parser.add_option("-t", "--token", action="store", type="string", dest="token",
                      default="", help=" token ")
    parser.add_option("-u", "--root_url", action="store", type="string", dest="root_url", default="vision.fotonower.com",
                      help="root_url to upload photos")
    parser.add_option("-d", "--datou", action="store", type="string", dest="datou",
                      default="2",help="datou id to be treated")
    parser.add_option("-P", "--protocol", action="store", type="string", dest="protocol",
                      default="https", help="http or https")
    parser.add_option("-D", "--day", type='string', dest='day', default="", help="day of folder to upload")
    parser.add_option("-v",'--verbose',action="store_true", dest='verbose', default=False,help='verbose mode')
    (x, args) = parser.parse_args()
    verbose = x.verbose
    current = datetime.datetime.now()
    print(current)
    if x.token == "":
        print("please provide a token")
        exit(1)
    try:
        fc = FC.FotonowerConnect(x.token, x.root_url, x.protocol)
    except :
        print("please provide a valid token")
        exit(1)
    if not os.path.isdir(x.folder):
        print("please provide a valid folder")
        exit(2)
    folder = x.folder
    day = x.day
    if day == "":
        day = current.strftime("%d%m%Y")
    hour = current.strftime("%H")
    minutes = current.strftime("%M")
    port_id = ""
    try:
        with open(os.path.join(os.getenv("HOME"), '.fotonower_config/port_id_{}.txt'.format(day)), 'r') as f:
            port_id = f.read()
    except Exception as e:
        print('no port, creating one')
        port_id = str(fc.create_portfolio("raspberry_{}".format(day)))
        if int(port_id) == 0:
            print("error with portfolio, creating one with hour/min")
            port_id = str(fc.create_portfolio("raspberry_{}{}{}".format(day,hour,minutes)))
        with open(os.path.join(os.getenv("HOME"), '.fotonower_config/port_id_{}.txt'.format(day)),'w') as f:
            f.write(port_id)
    if int(port_id) == 0:
        print("erreur creation portfolio")
        exit(1)
    folders_to_upload = []
    folder = os.path.join(folder,'{}'.format(day))
    folders_hours = [os.path.join(folder,x) for x in os.listdir(folder)]
    for fold in folders_hours:
        folders_to_upload = folders_to_upload + [os.path.join(fold,x) for x in os.listdir(fold)]
    uploaded = 0
    not_uploaded = 0
    for dir in folders_to_upload:
        files = [os.path.join(dir, x) for x in os.listdir(dir)]
        try:
            map_result_insert_aux = fc.upload_medias(files, portfolio_id=int(port_id), upload_small=True,
                                                     verbose=verbose, compute_classification=True, arg_aux="",auto_treatment= False)
            test = map_result_insert_aux[0].keys()
            if verbose:
                print("uploaded " + str (len(files)) + " files")
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
            uploaded += 1
            if verbose:
                print("deleting folder " + dir)
            shutil.rmtree(dir)
        except Exception as e:
            print(e)
            not_uploaded += 1
    print("uploaded " + str(uploaded) + " folders, missing " + str(not_uploaded))