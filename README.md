# Ant-Colony-Algorithm-Optimization
 Sınırlı ve Sınırsız Araç Problemi İçin Karınca Kolonisi Algoritması 

Gidilecek duraklar belirlenir. Daha sonra random bir şekilde bir durak seçilir ve o durağa gidilir. \
Toplam araç kapasitesinden duraktaki yolcu sayısı kapasitesi çıkartılarak araç kapasitesi güncellenir. \
Bu durakta yolcu kaldıysa kalan yolcu sayısı güncellenir. \
Durakta alınacak yolcu kalmadıysa bekleyen kişi sayısı olarak güncellenir. \
Daha sonra bu duraktan sonra araç kapasitesi yeterli ise gidilecek başka durak seçilir. Seçilecek diğer durak belli bir olasılık değerine göre belirlenir. Bu olasılık değeri feromon değeri ile orantılı olarak belirlenmektedir. \
Araçlar sezgisel olarak gittiği yollarda belirli oranda izler bırakırlar. Bu izlere feromon denilmektedir. Bu izler araçların o yoldan geçme sayısıyla orantılı olarak güncellenmektedir. \
Yani gidilen yoldaki Feromon miktarı fazla ise orada bırakılan izler fazla demektir ve o yolun seçilme olasılığı artar. Bir aracın gittiği yol aracın kapasitesi dolunca biter. \
Biten yol sonuç listesine eklenir. Durakta bekleyen kişi sayıları güncellenir ve yeni rota için gidilecek yollar seçilir.3 araç kapasitesi kadar yolcu alındıktan sonra fonksiyon biter ve başka bir rota oluşmaz. \
Oluşturulan yollar hesaplanmak üzere alınır. Seçilen yolların aralarındaki mesafeler hesaplanır. \
Hesaplama yapılırken 3 araçtan sonra kullanılan her araç başına belirli bir maliyet miktarı da toplam maliyete eklenir. \
Hesaplama sonrası oluşturulan yollar feromon güncellemesi ile bir takım matematiksel işlemler yapıldıktan sonra en az maliyetli yol belirlenir.
