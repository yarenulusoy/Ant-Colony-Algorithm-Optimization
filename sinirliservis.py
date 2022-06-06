import googlemaps
gmaps =googlemaps.Client(key='yourapikey')
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
import numpy as np
import firebase_admin
from firebase_admin import credentials
import math
import random
import numpy
from functools import reduce
alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
iterations =10
ants = 5
sondurak = 1
app = Flask(__name__)
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'adminveriler').document(u'maliyet')

doc = doc_ref.get()
if doc.exists:
    a=doc.to_dict()

arac_kiralama_maaliyeti=a['mali']


class Duraklar(object):
    def __init__(self, durakAdi, id, latitude, longitude, yolcuSayisi):
        self.durakAdi = durakAdi
        self.id= id
        self.latitude= latitude
        self.longitude= longitude
        self.yolcuSayisi =yolcuSayisi

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        city = Duraklar( source[u'durakAdi'],source[u'id'],source[u'latitude'],source[u'longitude'],source[u'yolcuSayisi'])
        return city

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'durakAdi': self.durakAdi,
            u'id': self.id,
            u'latitude': self.latitude,
            u'longitude': self.longitude,
            u'yolcuSayisi': self.yolcuSayisi,
        }

        return dest

    def __repr__(self):
        return(
            f'City(\
                durakAdi={self.durakAdi}, \
                id={self.id}, \
                latitude={self.latitude}, \
                longitude={self.longitude}, \
                yolcuSayisi={self.yolcuSayisi}\
            )'
        )
def generateGraph():
 feromones = 1
 doc_ref2 = db.collection(u'adminveriler').document(u'kapasite')
 doc = doc_ref2.get()
 if doc.exists:
     a = doc.to_dict()

 capacityLimit = a['kapa']

 docs = db.collection(u'yoltakip').stream()
 durakmatris = dict()
 demand = dict()
 demand2 = dict()
 demandkalan = dict()
 edges = dict()
 admatris=[]
 for doc in docs:
    duraklar = Duraklar.from_dict(doc.to_dict())
    a=duraklar.id,float(duraklar.latitude),float(duraklar.longitude),duraklar.yolcuSayisi,duraklar.durakAdi
    b=duraklar.id,duraklar.yolcuSayisi
    demand2[duraklar.id] = duraklar.yolcuSayisi
    demand[duraklar.id] = duraklar.yolcuSayisi
    demandkalan[duraklar.id] = duraklar.yolcuSayisi
    admatris.append(duraklar.durakAdi)
    durakmatris[duraklar.id] = float(duraklar.latitude),float(duraklar.longitude)
   # liste = [a for i in range(1)]
 print("veriler", durakmatris)
 print("demand:",demand)
 print("ilceler",admatris)
 vertices = list(durakmatris.keys())
 print("vertices",vertices)
 vertices.remove(1)
 print("remove 1 den sonra vertices",vertices)
 yenivertice=list()
 for i in demand.keys():
     if(demand[i]!=0):
         yenivertice.append(i)
 print("yeni vertice: ",yenivertice)

 for i in range(len(admatris)):
    for j in range(len(admatris)):
        con=gmaps.distance_matrix(admatris[i],admatris[j])['rows'][0]['elements'][0]['distance']['value']
        edges[i+1,j+1] = con
 print("edges ",edges)
 feromones = {(min(a, b), max(a, b)): 1 for a in durakmatris.keys() for b in durakmatris.keys() if a != b}
 print("fero", feromones)
 print("edges12",edges[(1,2)])
 return yenivertice, edges, capacityLimit, demand, feromones ,demandkalan

# bu fonksiyonda bi karıncanın gittiği yollar ve oluşturdugu rotalar cıkartılıyor kapasite dikkate alınarak
# ve son aşamada her rotanın sonuna 1 ekleniyor

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, feromones,demandkalan):
    solution = list()         #kenarlar              #köşedeki kişi sayisi
    otosay=0
    demandkalan=demand.copy()
    print("kalan koseler bas : ", vertices)
    print("demantlar bas: ",demand)
            #köşeler
    while(len(vertices)!=0): #köşe sayısı 0 olana kadar devam ediyor
        path = list()
        dene =list()
        print("kalan koseler: ", vertices)
        city = numpy.random.choice(vertices) # başlayacağı rastgele köşeyi seciyor
        print("secilen durak : ",city)
        print("duraktaki kisi sayisi : ",demand[city])
        if( demand[city]==0):
            vertices.remove(city)
        else:
          capacity = capacityLimit - demand[city] # araç kapasitesinden gittiği köşedeki kişi sayısını çıkartıyor
          if(capacity<0):
              demandkalan[city] = capacity * (-1)
              path.append(city)  # yola gittiği durağı ekliyor
              vertices.remove(city)  # köşe olan duraklardan gittiği durağı çıkartıyor
              print("kalan koseler: ", vertices)
          else:
            demandkalan[city]=0
            path.append(city) #yola gittiği durağı ekliyor
            vertices.remove(city) #köşe olan duraklardan gittiği durağı çıkartıyor
            print("kalan koseler: ",vertices)
          while(len(vertices)!=0):#yol listesi 0 olana kadar
            #olasılık listesi bir sonraki yolun seçilme olasılığına göre seçiyor feromon sayısına falan göre
            probabilities = list(map(lambda x: ((feromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta), vertices))
            probabilities = probabilities/numpy.sum(probabilities)
            city = numpy.random.choice(vertices, p=probabilities) # olasılığa göre yeni gideceği duragı seciyor
            if (demand[city] == 0):#seçilen yerde kişi yoksa
                vertices.remove(city)
                print("kalan koseler: ", vertices)
            else:# seçilen yerde kişi varsa
             if(capacity>0): # gittiği duraktan sonra otobüste kapasite hala varsa :
                print("      secilenin altlari", city)
                print("      duraktaki kisi sayisi : ", demand[city])
                path.append(city) # o durağı da yol listesine ekler
                capacity = capacity - demand[city]  # gittiği duraktaki kişi sayısını kapasiteden çıkarttı
                vertices.remove(city)
                print("kalan koseler: ", vertices)
                if(capacity==0):#duraktaki herkesi aldım
                    demandkalan[city] = 0
                    print("kalan koseler: ", vertices)
                elif(capacity>0):
                    demandkalan[city] = 0
                    #vertices.remove(city)  # gidilen yolu yol listesinden çıkarır
                    print("kalan koseler: ", vertices)
                elif(capacity<0):#durakta kalan kişiler var
                    demandkalan[city]=capacity*(-1)
                    print("kalan koseler: ", vertices)
             else:
                 print("bitti")
                 print("demand:", demandkalan)
                 for i in  demandkalan.keys():
                     print("kalan",i,demandkalan[i])
                     if(demandkalan[i]!=0):
                       dene.append(i)
                 print("deneeeeeee ",dene)
                 vertices=dene.copy()
                 print("verticeeeeeee",vertices)
                 demand=demandkalan.copy()
                 print("demant kopy: ",demand)
                 break
        if(otosay<3):
         path.insert(0,sondurak)
         solution.append(path) # sonuç listesine gidilen durak listesini ekler
        else:
            break
        print("1 karıncanın yolu : ",solution)
        otosay += 1
        print("otosay: ", otosay)
        print("son kalan demandlar .... ", demandkalan)

    return solution

def rateSolution(solution, edges): # her bulunan yolun rotalarini hesapliyor tek  tek toplam mesafelerini buluyor
    lokal = 0 # rota toplam maaliyet
    kiralamamaaliyeti=0
    print("edges ",edges) #koseler arası uzaklı kmatrisi
    otobussay = 0
    for i in solution:
        s=0
        a = 1 # 1. koseden baslar
        for j in i:
            b = j #solution dan gelen yolları sıradan alıyor 1. sini 2. sini sırayla b ye atıyor
            lokal = lokal + edges[(min(a,b), max(a,b))] #rotaya a ve b arasınındaki uzunluğu ekliyor
            print("a-b iki nokta arası mesafe ",a,b,edges[(min(a,b), max(a,b))])
            a = b # b yi a yapıyor ki 1-2 2-3 gibi olsun diye
            print("rota toplam1 m lokal ", lokal)
        otobussay +=1
        print("rota toplam m lokal",lokal)
        s+=lokal
        s = s / 1000

        print("rota toplam km ", s)
    print("otobus sayisi : ", otobussay)
    print("rota toplam hepsi ",s)
    if(otobussay>3):
        kiralamamaaliyeti=(otobussay-3)*arac_kiralama_maaliyeti
        print("arac kiralama maaliyeti: ",kiralamamaaliyeti)
        s=s+kiralamamaaliyeti
        print("rota toplam otobuslu ", s)

    return s

def updateFeromone(feromones, solutions, bestSolution):
    # solutions olası tüm ihtimallerin rotaları ve toplam maaliyetler [yollar][maaliyet]
    # freeromones ilk başta tüm rotalar arası feromon degeri 1 kednimiz belirledik

    print("solutions",solutions)
    print("feromones1:",feromones)
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions) # oluşan tüm maaliyetlerin ortalaması
    feromones = { k : (ro + th/Lavg)*v  for (k,v) in feromones.items() }
    # degisen rotaya göre feromone hesaplanıyor formülü anlamadım
    solutions.sort(key = lambda x: x[1]) #solutionsları kucukten buyuge siraliyor
    if(bestSolution!=None): #onceden belirlenen bir en iyi yol varsa
        if(solutions[0][1] < bestSolution[1]): # solutionsun ilk elemanı yani en küçüğü önceki en iyiden daha küçükse
            bestSolution = solutions[0]    # yeni en iyi o olur
        for path in bestSolution[0]: # en iyi yolun rotasını aldı
            for i in range(len(path)-1): # rota bitene kadar
                # o yoldaki iki nokta arası fenomone degeri =  bi hesabı+ fenomon degerine ekle
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]

    else: #onceden belirlenen bir en iyi yol yoksa

        bestSolution = solutions[0]#o noktayı en iyi yap


    for l in range(sigm): #sigm =3
        paths = solutions[l][0] # gidilen yolların rotalarını alıyor tek tek ve
        L = solutions[l][1]     # gidilen yolların maaliyetlerini alıyor         maaliyet arttıkça fenomon azalır şeklinde fenomonları güncelliyor
        for path in paths:
            for i in range(len(path)-1):                                          # maliyet arttıkça bırakılan fenomon miktarı azalır
                feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + feromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]

    return bestSolution
@app.route("/")
def showHomePage():
    return str(liste)
def main():
    bestSolution = None
    vertices, edges, capacityLimit, demand, feromones ,demandkalan = generateGraph()

    for i in range(iterations):
        solutions = list()
        for _ in range(ants):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, feromones,demandkalan)
            solutions.append((solution, rateSolution(solution, edges)))
        bestSolution = updateFeromone(feromones, solutions, bestSolution) # gönderilen solutions antte oluşturulup maaliyeti hesaplanan aslında maaliyet
    return bestSolution

if __name__ == "__main__":
    solution = main()
    print("Solution: ", solution)
    liste = list()
    print("Solution: ", str(solution))
    yollar = str(solution[0][:])
    rotalar = yollar.replace("[", "")
    rotalar = rotalar.replace("]", "")
    rotalar = rotalar.replace(" ", "")
    rotalar2 = list()
    rotalar3 = list()
    rotalar2 = rotalar.split(",");
    rotalar3 = [int(i) for i in rotalar2]

    db = firestore.client()

    for i in range(len(rotalar3)):
        docs = db.collection(u'yoltakip').where(u'id', u'==', rotalar3[i]).stream()
        for doc in docs:
            duraklar = Duraklar.from_dict(doc.to_dict())
            liste.append(duraklar.latitude)
            liste.append(duraklar.longitude)

    ref = db.collection(u'rotalar').document(u'2')
    ref2 = db.collection(u'maliyetler').document(u'2')
    ref2.update({u'maliyet': str(solution[1])})
    ref.update({u'rota': str(liste)})
    ref3 = db.collection(u'rotadizi').document(u'2')
    ref3.update({u'rota': str(solution[0])})

    app.run(host="0.0.0.0")
