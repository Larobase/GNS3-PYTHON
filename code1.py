import json

def max(a,b):
    if a>b:return a
    return b
def min(a,b):
    if a<b:return a
    return b

def loopback(r):
    configfile.write("interface loopback0\nno ip address\n"
    "ipv6 address 2001:ABCD\n"
    "ipv6 enable\n"
    "ipv6 "+data["AS_details"][int(r["router_as"])-1]["AS_protocol"]+"\n"
    "!\n")
    #configurer variation d'addresse de loopback
def interface(r):
    it=0
    interface_utilisee=[False,False,False,False]
    for interface in r['router_int']:
        configfile.write("interface ")
        if interface=="F" :
            configfile.write("FastEthernet0/0\n")
        else : 
            interface_utilisee[int(interface)-1]=True
            configfile.write("GigabitEthernet"+interface+"/0\n")
        configfile.write("no ip address\nnegociation auto\nipv6 address 2001:200:"+network(r,r["router_voisin"][it]-1)+"/64\n"
        "ipv6 enable\n"
        "ipv6 "+data["AS_details"][int(r["router_as"])-1]["AS_protocol"]+"\n"
        "!\n")
        it+=1
    for i in range(4):
        if interface_utilisee[i]==False :
            configfile.write("GigabitEthernet"+str(i+1)+"/0\n"
                             "no ip address\n"
                             "shutdown\n"
                             "negociation auto\n"
                             "!\n")

def network(r,v) :
    as1=data['router_details'][v]["router_as"]
    as2=r["router_as"]
    name_r=r["router_name"]
    name_voisin=data['router_details'][v]["router_name"]
    net=str(int(as1)+int(as2))+":"+str(100*min(int(name_r),int(name_voisin))+max(int(name_r),int(name_voisin)))+"::"+r["router_name"]
    return net
            
# Opening JSON file
f = open('Input.json')

# returns JSON object as
# a dictionary
data = json.loads(f.read())

# Iterating through the json
# list

for i in data['router_details']:
    with open(r"configfile"+i["router_name"]+".cfg", 'w') as configfile:
        configfile.write("------------------CECI EST LE ROUTEUR "+i["router_name"]+"----------------\n")
        loopback(i) #loopback
        interface(i) #gère les interfaces 
    #router bgp
    #address family ipv4
    #address family ipv6
    #ip forward protocolnd
    #line con 0
        configfile.write("\n\n\n\n")
    # Closing file
f.close()