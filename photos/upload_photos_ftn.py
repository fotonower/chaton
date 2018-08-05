
import os, sys
import fotonower as FC



def upload_folder(main_folder, portfolio_id, token, limit, offset,
                  verbose, order, root_url, upload_small, new, batch_size, private, datou):
    """
        Cette fonction permet l upload des photos qui se trouve dans 
        le meme dossier on peut utliser le param batch_size pour envoyer
        par lot de photos 
    """
    print(" In upload_folder : ")
    fc = FC.FotonowerConnect(token)
    list_files = os.listdir(main_folder)

    # MR 13 le order like_folder ne marche pas pour la fonction upload_folder
    file_order(order, list_files)

    if limit != 0:
        list_files_used = list_files[offset:offset+limit]
    else :
        list_files_used = list_files



    count = 0
    files_to_send = {}
    mtr_photo_id = []

    # , 'id' : basename

    url_to_upload_loc = "http://"+root_url+"/api/v1/secured/photo/upload?token=" + token
    if new :
        url_to_upload_loc += "&new_port=true"
        portfolio_id = None
    if datou:
        url_to_upload_loc += "&datou=" + str(datou)
    if private : 
        url_to_upload_loc += "&upload_photo_private=true"
    if upload_small :
        url_to_upload_loc += "&upload_small=true"

    print(url_to_upload_loc + "\n")

    begin_time = time.time()
    print("Number of file = " + str(len(list_files_used)) + "\n")
    for f in list_files_used :
        if not f.lower().endswith(("jpg", "jpeg", "png", "mp4")):
            sys.stdout.write('X')
            sys.stdout.flush()
            continue
        sys.stdout.write('.')
        sys.stdout.flush()
        print(f)
        filepath = os.path.join(main_folder, f)
        files_to_send["file" + str(count)] = open(filepath, 'rb')

        # MR envoie par batch de photo 
        if count == batch_size :
            basename = os.path.basename(main_folder)
            print (basename)
            r = requests.post(url_to_upload_loc, files=files_to_send, data={'portfolio_id':portfolio_id})
            if verbose:
                print("\nbatch_size  = " + str(batch_size) + " | count : " + str(count))
                print ("\n" + r.content)
            else:
                sys.stdout.write('=> ')
                sys.stdout.flush()
                print("count : " + str(count))
            count = 0
            files_to_send = {}
            json_parsed = json.loads(r.content)
            portfolio_id = json_parsed["portfolio_id"]
            begin_time = count_and_display_elapsed_time(begin_time)
        else :
            count = count + 1

    if count > 0 :
        r = requests.post(url_to_upload_loc, files=files_to_send, data={'portfolio_id':portfolio_id})
        if verbose:
            print ("\n" + r.content)
            print("\ncount : " + str(count))
        else:
            for i in range(0,count):
                sys.stdout.write('.')
                sys.stdout.flush()
    print("\nFinished uploaded !")



if __name__ == '__main__' :
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-l", "--limit", action="store", type="int", dest="limit", default=0, help="limit")
    parser.add_option("-o", "--offset", action="store", type="int", dest="offset", default=0, help="offset")
    parser.add_option("-p", "--feed_id", action="store", type="int", dest="feed_id", default=0, help="feed_id")
    parser.add_option("-b", "--batch_size", action="store", type="int", dest="batch_size", default=200, help="batch_size")
    parser.add_option('-d', '--datou_id', action='store', dest='datou', type="int", default=0, help='datou_id for treatment, if none provided using default user one, if 0 is set, no datou batch')

    parser.add_option("-j", "--job", action="store", type="string", dest="job", default="test_autonower", help="test_autonower upload_folder upload_sub_folder")
    parser.add_option("-t", "--token", action="store", type="string", dest="token", default="78d09a0790ec6ecbf119343125a81fdc", help=" token ")
    parser.add_option("-f", "--folder", action="store", type="string", dest="folder", default="/home/fotonower/", help="folder where are photo to upload")
    parser.add_option("-u", "--root_url", action="store", type="string", dest="root_url", default="www.fotonower.com", help=" token ")
    parser.add_option("-O", "--order", action="store", type="string",dest="order", default="lexicographic", help="order : numeric, lexicographic, like_folder")

    parser.add_option("-s", "--private", action="store_true", dest="private", default=False, help="upload_photo_private")
    parser.add_option("-U", "--upload_small", action="store_true", dest="upload_small", default=False, help=" upload_small ")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help=" verbose ")
    parser.add_option("-n", "--new", action="store_true", dest="new", default=False, help="new_feed")
    parser.add_option('-a', '--args', action='store', dest='args', default={'custom_size':224, 'compute_classification' : False})

    (x, args) = parser.parse_args()

    if os.path.exists(x.folder):
        if x.job == "upload_folder" :
            upload_folder(x.folder, x.feed_id, x.token, x.limit, x.offset, x.verbose, x.order, x.root_url, x.upload_small, x.new, x.batch_size, x.private, x.datou)
        else :
            print("Unknow job " + str(x.job))
    else :
        print ("dir : " + str(x.folder) + " not exist")

