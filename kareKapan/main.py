def tahta_ciz(yatay, dikey):
    tahta = "\n"
    sutun_isimleri = "ABCDEFGH"
    if yatay < 3 or yatay > 7 or dikey - yatay != 1:  # yatay ve dikey değerleri 3 ile 7 arasında olmalı
        print("Oyun kurallarına uymuyor")
        return
    hamleler = []  # hamleleri tutacak liste
    for i in range(yatay):
        hamleler.append([])
        for j in range(dikey):
            hamleler[i].append(".")  # boş olan yerler için . koyuyoruz
    col = "   ".join([sutun_isimleri[i] for i in range(dikey)])  # sütun isimlerini yazdırıyoruz
    sep = "   ".join(["|" for i in range(dikey)])  # ayraç | ekliyoruz
    tahta += "    {}\n".format(col)  # sütun isimlerini ekliyoruz
    for r in range(yatay):
        rows = "___".join(["{}" for i in range(dikey)])  # satırları hazırlıyoruz
        tahta += "{}   {}\n    ".format(r+1, rows)  # satır numarasını ve satırları ekliyoruz
        if r < yatay-1:  # eğer satır sayısının sonuna gelmemişse bir ayraç daha ekliyoruz
            tahta += sep + '\n'
    return tahta, hamleler  # tahta ve hamleleri döndürüyoruz


def yazdir(tahta, hamleler):  # tahtayı yazdırıyoruz
    liste = []
    for i in hamleler:
        liste.extend(i)
    print(tahta.format(*liste))


def karemi(hamleler, tas):  # kare olup olmadığını kontrol ediyoruz
    # a, b = tas
    b, a = tas  # taş değişkeni iki index alıyor
    for x in range(len(hamleler)-1):  # satırlar kadar dönüyoruz
        for y in range(len(hamleler)):  # sütunlar kadar dönüyoruz
            # durum ile kare olup olmadığını kontrol ediyoruz
            durum = hamleler[x][y] == hamleler[x][y+1] == hamleler[x+1][y] == hamleler[x+1][y+1]
            # durum True ise ve taşının yerinde bir kare varsa True döndürüyoruz
            if durum and x == a and y == b:
                return True
            if durum and x+1 == a and y+1 == b:
                return True
            if durum and x+1 == a and y == b:
                return True
            if durum and x == a and y+1 == b:
                return True
    return False  # kare olmadığında False döndürüyoruz


def kare_say(hamleler):
    # oyununda ilk taşlar dizildikten sonra kare sayısını buluyoruz
    kareler = []
    for x in range(len(hamleler)-1):
        for y in range(len(hamleler)):
            durum = hamleler[x][y] == hamleler[x][y+1] == hamleler[x+1][y] == hamleler[x+1][y+1]
            if durum:  # bu kısım karemi ile aynı işi yapıyor
                kareler.append(hamleler[x][y])  # True ise renk değerini listeye ekliyoruz
    return kareler


def topla(tahta, hamleler, oyuncu, tas=None):
    # tahtadan taş alıyoruz
    baslik = "ABCDEFGH"
    if oyuncu == "B":
        hamle = input("\nBirinci (beyaz) oyuncu lütfen taşı almak için hamle yapınız: ")
    elif oyuncu == "S":
        hamle = input("\nİkinci (siyah) oyuncu lütfen taşı almak için hamle yapınız: ")
    try:
        x = baslik.index(hamle[1].upper())  # girilen hamle 2. indexindeki harfleri alıyoruz
        y = int(hamle[0])-1  # girilen hamlenin ilk değeri indexte -1 olduğundan çıkartıyoruz
        # örneğin 1A girildiğinde aslında listenin 0. indexi olacaktır
        kare = karemi(hamleler, (x, y))
        if kare:
            print("\nSeçilen yer bir kare")
            yazdir(tahta, hamleler)
            # seçilen yer bir kare olduğu için bu fonksiyon yeniden çağrılıyor
            return topla(tahta, hamleler, oyuncu)
    except ValueError:
        print("Hatalı hamle")  # girilen değer uygun değilse hata veriyoruz
        return topla(tahta, hamleler, oyuncu)
    if hamleler[y][x] == '.':  # hamle yapılacak yer boş ise
        print("Boş bir yer seçtiniz")
        yazdir(tahta, hamleler)
        return topla(tahta, hamleler, oyuncu)  # yeniden çağrılıyor
    elif hamleler[y][x] != oyuncu:  # hamle yapılacak yerde başka bir oyuncunun taşı varsa
        kare = karemi(hamleler, (x, y))
        if kare:  # karemi True ise
            print("\nSeçtiğiniz yer bir kare içeriyor")
            yazdir(tahta, hamleler)
            return topla(tahta, hamleler, oyuncu)  # yeniden çağrılıyor
        else:
            hamleler[y][x] = '.'  # taşın yerini boş yapıyoruz
        yazdir(tahta, hamleler)
        return hamleler
    elif hamleler[y][x] == oyuncu:  # hamle yapılacak yerde kendi taşı varsa
        print("Kendi taşınızı seçemezsiniz")
        yazdir(tahta, hamleler)
        return topla(tahta, hamleler, oyuncu)  # yeniden çağrılıyor
    else:
        print("Geçersiz hamle")  # geçersiz bir hamle girildiğinde hata veriyoruz
        yazdir(tahta, hamleler)
        return topla(tahta, hamleler, oyuncu)  # yeniden çağrılıyor


def hamle_kontrol(hamleler, nereden, nereye):
    # üçüncü aşamada yapılan hamleleri kontrol ediyoruz
    y1, x1 = nereden  # hamle yapılan yerin koordinatlarını alıyoruz
    y2, x2 = nereye  # hamle yapılacak yerin koordinatlarını alıyoruz
    if y1 == y2:  # hamle yapılan yerden hamle yapılacak yere aynı satır ise
        if x1 < x2:  # hamle yapılan yerden hamle yapılacak yere soldan sağa doğru ise
            for i in range(x1+1, x2):  # hamle yapılan yerden hamle yapılacak yere kadar dönüyoruz
                if hamleler[y1][i] != '.':  # hamle yapılacak yer boş değilse
                    return False  # False döndürüyoruz
            return True  # bu kurallar dışındaysa True döndürüyoruz
        elif x1 > x2:  # hamle yapılan yerden hamle yapılacak yere soldan sola doğru ise
            for i in range(x1-1, x2, -1):
                if hamleler[y1][i] != '.':
                    return False
            return True
    elif x1 == x2:  # hamle yapılan yerden hamle yapılacak yere aynı sütun ise
        if y1 < y2:
            for i in range(y1+1, y2):
                if hamleler[i][x1] != '.':
                    return False
            return True
        elif y1 > y2:
            for i in range(y1-1, y2, -1):
                if hamleler[i][x1] != '.':
                    return False
            return True
    return False


def hamle_yap(tahta, hamleler, oyuncu, surukle=False):
    baslik = "ABCDEFGH"  # karelerin yerlerini belirleyen değişken
    if oyuncu == "B":  # oyuncu B ise
        name = "Birinci"  # oyuncu adını belirleyen değişken
    else:
        name = "İkinci"
    try:  # girilen değer uygun değilse hata veriyoruz
        if surukle:  # surukle parametresi True ise
            hamle = input("\n{} oyuncu lütfen taşı sürüklemek için hamle yapınız(1C 1B): ".format(name))
            if hamle.upper() == 'Q':
                import sys
                sys.exit()
            _from, to = hamle.split()  # girilen değerleri ayırıyoruz
            x1 = baslik.index(_from[1].upper())  # harfin index karşılığını alıyoruz
            y1 = int(_from[0])-1  # girilen değerin ilk değerini indexte -1 olduğundan çıkartıyoruz
            x2 = baslik.index(to[1].upper())
            y2 = int(to[0])-1
            if hamleler[y1][x1] == oyuncu and hamleler[y2][x2] == '.':
                # hamle yapılan yerde kendi taşı varsa ve hamle yapılacak yer boş ise
                kontrol = hamle_kontrol(hamleler, (y1, x1), (y2, x2))
                # kuralları kontrol ediyoruz
                if kontrol:  # kurallara uygunsa hamle yapıyoruz
                    hamleler[y2][x2] = oyuncu
                    hamleler[y1][x1] = '.'
                    yazdir(tahta, hamleler)
                    kare = karemi(hamleler, (x2, y2))
                    if kare:  # hamle yapıldıktan sonra kare oluşuyorsa
                        print("Tebrikler! Kare yaptınız.")
                        sonuc = topla(tahta, hamleler, oyuncu)
                        if sonuc:
                            hamleler = sonuc
                    return hamleler
                else:  # kurallara uymuyorsa hata veriyoruz
                    print("Geçersiz hamle")
                    yazdir(tahta, hamleler)
                    return hamle_yap(tahta, hamleler, oyuncu, True)
            else:  # hamle yapılan yerde kendi taşı yoksa hata veriyoruz
                print("Geçersiz hamle")
                return hamle_yap(tahta, hamleler, oyuncu, True)
        hamle = input("\n{} oyuncu lütfen hamle yapınız: ".format(name))
        # surukle parametresi yoksa girilen değerleri ayırıyoruz
        x = baslik.index(hamle[1].upper())
        y = int(hamle[0])-1
        if hamleler[y][x] == '.':  # hamle yapılan yer boş ise
            hamleler[y][x] = oyuncu  # hamle yapılan yerine oyuncunun taşını atıyoruz
            yazdir(tahta, hamleler)
            return hamleler
        else:
            print("Geçersiz hamle")
            return hamle_yap(tahta, hamleler, oyuncu)
    except Exception:
        print("Geçersiz hamle")
        return False


def ucuncu_asama(tahta, hamleler, oyuncu):
    # oyunda kareleri saydıktan sonra taşların hareket ettirildiği kısım
    while True:  # oyun bitene kadar devam ediyoruz
        score1 = 0  # oyuncu 1 için puan değişkeni
        score2 = 0  # oyuncu 2 için puan değişkeni
        for i in hamleler:  # hamleleri döngüye sokuyoruz
            score1 += i.count('B')  # hamlelerdeki B değerlerini sayıyoruz
            score2 += i.count('S')  # hamlelerdeki S değerlerini sayıyoruz
        if score1 < 4:  # oyuncu 1 için taşı 4 den az ise
            print("İkinci oyuncu SİYAH renk ile kazandı")
            break  # oyunu bitiriyoruz
        elif score2 < 4:  # oyuncu 2 için taşı 4 den az ise
            print("Birinci oyuncu BEYAZ renk ile kazandı")
            break  # oyunu bitiriyoruz
        if oyuncu == 'B':
            hamle = hamle_yap(tahta, hamleler, oyuncu, True)
            # taş sürükleme değişkeni true olacak şekilde hamle yapıyoruz
            if hamle:  # hamle yapıldıysa
                hamleler = hamle  # hamleleri dönen değere atıyoruz
                oyuncu = 'S'  # oyuncu değişkenini değiştiriyoruz
        elif oyuncu == 'S':
            hamle = hamle_yap(tahta, hamleler, oyuncu, True)
            if hamle:
                hamleler = hamle
                oyuncu = 'B'


def ikinci_asama(tahta, hamleler, kareler=None):
    # oyunda karelerin toplandığı kısım
    if kareler is None:  # kareler sayılmadıysa
        kareler = kare_say(hamleler)  # kareleri sayıyoruz
        print("\nBeyaz kare sayısı: {}".format(kareler.count("B")))
        print("Siyah kare sayısı: {}".format(kareler.count("S")))
        kareler.sort()  # kareleri sıralıyoruz
        # örnek çıktı ["B", "S", "S"]
    for oyuncu in kareler:  # kareleri döngüye sokuyoruz
        sonuc = topla(tahta, hamleler, oyuncu)
        if sonuc:  # toplama işlemi başarılı ise
            hamleler = sonuc  # hamleleri dönen değere atıyoruz
        else:  # toplama işlemi başarısız ise
            kareler.remove(oyuncu)  # karelerden sırayı çıkartıyoruz
            ikinci_asama(tahta, hamleler, kareler)  # tekrar çağırıyoruz
    if oyuncu == 'S':  # oyuncu değişkenini değiştiriyoruz
        oyuncu = 'B'
    else:
        oyuncu = 'S'
    # toplama işlemi bittikten sonra üçüncü aşamaya geçiyoruz
    ucuncu_asama(tahta, hamleler, oyuncu)


def main(yatay, dikey):  # ilk fonksiyon
    tahta, hamleler = tahta_ciz(yatay, dikey)
    # tahta ve hamleler değişkenlerini oluşturuyoruz
    print("Kare Toplama Oyunu")
    yazdir(tahta, hamleler)
    bos_yer = yatay*dikey  # toplam boş yer sayısı
    oyuncu = 'B'  # Beyaz taş ilk oyuncu
    while bos_yer > 0:  # boş yer sayısı 0 dan büyük olduğu sürece
        hamle = hamle_yap(tahta, hamleler, oyuncu)
        if hamle:  # hamle yapıldıysa
            hamleler = hamle  # hamleleri dönen değere atıyoruz
            bos_yer -= 1  # boş yer sayısını azaltıyoruz
            if oyuncu == 'B':  # oyuncu değişkenini değiştiriyoruz
                oyuncu = 'S'
            else:
                oyuncu = 'B'
        else:  # hamle yapılamadıysa
            continue  # tekrar başa döndürüyoruz
    ikinci_asama(tahta, hamleler)  # boş yer sayısı 0 olduğunda ikinci aşamaya geçiyoruz


if __name__ == "__main__":
    while True:
        try:
            yatay = int(input("Lütfen yatay çizgi sayısını giriniz: "))
            main(yatay, yatay+1)
        except Exception:
            print("Geçersiz değer")

