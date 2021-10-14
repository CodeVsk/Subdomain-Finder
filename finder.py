import requests, json, socket, threading

validates=[]

thread = 4

print('''
 (                (         )     *             (        )  
 )\ )          (  )\ )   ( /(   (  `     (      )\ )  ( /(  
(()/(    (   ( )\(()/(   )\())  )\))(    )\    (()/(  )\()) 
 /(_))   )\  )((_)/(_)) ((_)\  ((_)()\((((_)(   /(_))((_)\  
(_))  _ ((_)((_)_(_))_    ((_) (_()((_))\ _ )\ (_))   _((_) 
/ __|| | | | | _ )|   \  / _ \ |  \/  |(_)_\(_)|_ _| | \| | 
\__ \| |_| | | _ \| |) || (_) || |\/| | / _ \   | |  | .` | 
|(__/ \(__/  |__)/|(__/  \___/ (_|  |_|/_/ \_\ |___| |_|\_| 
            )\ )  )\ )  ( /(  )\ )        )\ )                         
            (()/( (()/(  )\())(()/(   (   (()/(                         
            /(_)) /(_))((_)\  /(_))  )\   /(_))                       
            (_))_|(_))   _((_)(_))_  ((_) (_))                          
            | |_  |_ _| | \| | |   \ | __|| _ \                         
            | __|  | |  | .` | | |) || _| |   /                         
            |_|   |___| |_|\_| |___/ |___||_|_\                         
                                                            
''')

query = input("Insert url: ")

r = requests.get("https://dns.bufferover.run/dns?q="+query)
j = r.json()

if (j["RDNS"] == None) and (j["FDNS_A"] == None):
    print("[+] Not domains avaliable [+]")
elif (j["RDNS"] == None):
    res = list(dict.fromkeys(j["FDNS_A"]))
elif (j["FDNS_A"] == None):
    res = list(dict.fromkeys(j["RDNS"]))
else:
    res = list(dict.fromkeys(list(dict.fromkeys(j["FDNS_A"]+j["RDNS"]))))


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

def dnsValidate(ar,id_):
    with open("data.txt", "a+") as file:
        for x in ar:
            try:
                print(x)
                data = x.split(",")
                r = requests.get("http://"+data[1], timeout=10)
                if r.status_code == 200:
                    file.write(data[1]+"\n")
            except:
                pass
    file.close()
    print('[+] THREAD',id_,'COMPLETED [+]')

data=list(chunker_list(res, thread))

for i in range(0,thread):
    t = threading.Thread(target=dnsValidate, args = (data[i],i))
    t.start()
