import urllib.request
import json
from enum import Enum


class Podatak(Enum):
    """
    Lista mogućih podataka koji se mogu povući sa pojedinih funkcija.
    
    Mogući podatci:
    --------------
        SMJER_VJETRA        : Služi za dohvaćanje smjera vjetra.
        JACINA_VJETRA       : Služi za dohvaćanje jačine puhanja vjetra.
        NAZIV_SMJERA_VJETRA : Služi za dohvaćanje naziva vjetra.
        TEMPERATURA         : Služi za dohvaćanje temperature.
        VRIJEME_ID          : Služi za dohvaćanje numeričkog identifikatora vremena.
        TEXT                : Služi za dohvaćanje teksualne verzije funkcije.
        AUDIO               : Služi za dohvaćanje audio verzije funkcije.
        SAT                 : Služi za dohvaćanje trenutnog sata.
        MINUTA              : Služi za dohvaćanje trenutne minute.
        MBROLA              : Služi za dohvaćanje MBROLA verzije funkcije.
    """

    SMJER_VJETRA = 0
    JACINA_VJETRA = 1
    NAZIV_SMJERA_VJETRA = 2
    TEMPERATURA = 3
    VRIJEME_ID = 4
    TEXT = 5
    AUDIO = 6
    SAT = 7
    MINUTA = 8
    MBROLA = 9


class Vrijeme:
    """
    Klasa koja sadrži funkcije programa.

    Funkcije:
    --------
        DobaviPodatke    : Funkcija koja služi za dohvaćanje potrebnih vremenskih podataka.
        NazivSmjerVjetra : Funkcija za dohvaćanje smjera puhanja vjetra ovisno o kutu.
        NazivVjetra      : Funkcija za određivanje naziva vjetra bazirano na Beaufortovoj ljestvici.
        OpisVremena      : Funkcija koja vraća opis vremena ovisno o vremenskom id-u.
        CepanjeBrojeva   : Funkcija koja dijeli brojeve na jedinice, desetice, stotice...
        BrojURijeci      : Funkcija koja pretvara broj u njegov rječni ekvivalent.
        DobaviSatIMinutu : Funkcija koja dobavlja trenutni sat, ili minutu.
        UvodniPozdrav    : Funkcija koja vraća uvodni pozdrav ovisno o dobu dana.
        Prognoza         : Funkcija koja vraća prognozu vremena.
        ZapisMBROLA      : Funkcija koja zapisuje prognozu u tekstualnu datoteku, za čitanje u MBROLA-i.
    """
    podatci = json.loads(urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=b0cf9d4de9f5ff964a853090bd6cb6b2&units=metric").read().decode())
    stranica = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())

    def DobaviPodatke(self, potreban_podatak):
        """
        Funkcija dobavlja vremenske podatke sa OpenWeatherMap API-a.

        Argument:
        --------
            potreban_podatak    : Podatak
                Vrsta podatka kojeg želimo iz funkcije.

        Vraća:
        -----
            ukoliko potreban_podatak:
                    Podatak.SMJER_VJETRA 
                        int     : Numerička vrijednost kuta sa kojeg vjetar puše.
                                    npr. 234
                    Podatak.JACINA_VJETRA
                        float   : Numerička vrijednost jačine puhanja vjetra mjereno u m/s.
                                    npr. 2.5
                    Podatak.NAZIV_SMJERA_VJETRA
                        string  : Naziv smjera sa kojeg vjetar puše (8-smjerni) - poziva funkciju NazivSmjerVjetra().
                                    npr. "istočni"
                    Podatak.TEMPERATURA
                        float   : Numerička vrijednost temperature zraka.
                                    npr. -2.74
                    VRIJEME_ID
                        int     : Identifikator opisa vremenskog stanja.
                                    npr. 804
        """

        smjer_vjetra = 0 if "deg" not in Vrijeme.podatci["wind"] else Vrijeme.podatci["wind"]["deg"]
        naziv_smjera_vjetra = Vrijeme().NazivSmjerVjetra(smjer_vjetra)
        jacina_vjetra = 0 if "speed" not in Vrijeme.podatci["wind"] else Vrijeme.podatci["wind"]["speed"]
        temperatura = 0 if "temp" not in Vrijeme.podatci["main"] else Vrijeme.podatci["main"]["temp"]
        vremena_u_podacima = Vrijeme.podatci["weather"]
        vremena_idjevi = []

        i = 0
        while(i < len(vremena_u_podacima)):
            vremena_idjevi.append(vremena_u_podacima[i]["id"])
            i += 1
        i = 0

        if(potreban_podatak == Podatak.SMJER_VJETRA):
            return smjer_vjetra
        elif(potreban_podatak == Podatak.JACINA_VJETRA):
            return jacina_vjetra
        elif(potreban_podatak == Podatak.NAZIV_SMJERA_VJETRA):
            return naziv_smjera_vjetra
        elif(potreban_podatak == Podatak.TEMPERATURA):
            return temperatura
        elif(potreban_podatak == Podatak.VRIJEME_ID):
            return vremena_idjevi

    def NazivSmjerVjetra(self, smjer):
        """
        Funkcija vraća naziv smjera sa kojeg vjetar puše.
        
        Argument:
        --------
            smjer  : int / string
                Numerička vrijednost kuta iz kojeg puše vjetar.
        
        Vraća:
        -----
            string : Naziv smjera ovisno o kutu (0° je 12h).
                        npr. 153 -> "jugoistočni"
        """

        smjerovi_vjetrova = ["sjeverni", "sjeveroistočni", "istočni", "jugoistočni", "južni", "jugozapadni", "zapadni", "sjeverozapadni"]
        naziv = smjerovi_vjetrova[int(((float(smjer)+(360/(len(smjerovi_vjetrova)*2))) % 360)/(360/len(smjerovi_vjetrova)))]

        return naziv

    def NazivVjetra(self, vrsta_prognoze, brzina, smjer):
        """
        Funkcija vraća naziv vjetra ovisno o brzini puhanja vjetra.

        Argumenti:
        ---------
            vrsta_prognoze      : Podatak
                Vrsta podatka kojeg želimo iz funkcije.
            brzina              : float
                Numerička vrijednost brzine puhanja vjetra.
            smjer               : int
                Numerička vrijednost kuta puhanja vjetra.

        Vraća:
        -----
            ukoliko vrsta_prognoze:
                    Podatak.TEXT
                        string  : Prognoza vjetra koja uključuje interpunkcijske znakove.
                                    npr. (2.5, 325) -> ", te puše sjeveroistočni povjetarac."
                    Podatak.AUDIO
                        string  : Prognoza vjetra koja ne uključuje interpunkcijske znakove.
                                    npr. (2.5, 325) -> "te puše sjeveroistočni povjetarac"
        """

        nazivi_vjetrova = ["tišina", "lahor", "povjetarac", "slab vjetar", "umjeren vjetar", "umjereno jak vjetar",
                           "jak vjetar", "žestoki vjetar", "olujni vjetar", "jak olujni vjetar", "orkanski vjetar", "jak orkanski vjetar", "orkan"]

        if(brzina <= 0.3):
            vjetar_indeks = 0
        elif(0.3 < brzina <= 1.5):
            vjetar_indeks = 1
        elif(1.5 < brzina <= 3.3):
            vjetar_indeks = 2
        elif(3.3 < brzina <= 5.5):
            vjetar_indeks = 3
        elif(5.5 < brzina <= 7.9):
            vjetar_indeks = 4
        elif(7.9 < brzina <= 10.7):
            vjetar_indeks = 5
        elif(10.7 < brzina <= 13.8):
            vjetar_indeks = 6
        elif(13.8 < brzina <= 17.1):
            vjetar_indeks = 7
        elif(17.1 < brzina <= 20.7):
            vjetar_indeks = 8
        elif(20.7 < brzina <= 24.4):
            vjetar_indeks = 9
        elif(24.4 < brzina <= 28.4):
            vjetar_indeks = 10
        elif(28.4 < brzina <= 32.6):
            vjetar_indeks = 11
        else:
            vjetar_indeks = 12

        smjer_vjetra_naziv = Vrijeme().NazivSmjerVjetra(smjer)
        prognoza_tekst = "." if(vjetar_indeks == 0) else ", te puše {0} {1}.".format(smjer_vjetra_naziv, nazivi_vjetrova[vjetar_indeks])
        prognoza_audio = "" if(vjetar_indeks == 0) else " te puše {0} {1}".format(smjer_vjetra_naziv, nazivi_vjetrova[vjetar_indeks])

        if(vrsta_prognoze == Podatak.TEXT):
            return prognoza_tekst
        elif(vrsta_prognoze == Podatak.AUDIO):
            return prognoza_audio

    def OpisVremena(self, potreban_podatak, vrijeme_id):
        """
        Funkcija vraća opis trenutnog vremena.

        Argumenti:
        ---------
            potreban_podatak    : Podatak
                Vrsta podatka kojeg želimo iz funkcije.
            vrijeme_id          : int
                ID vremena koji koristimo za dohvaćanje tekstualnog opisa istog.

        Vraća:
        -----
            ukoliko potreban_podatak:
                     Podatak.TEXT
                        string  : Opis trenutnog vremena.
                            npr. 714 -> "magla"
                    Podatak.AUDIO
                        string  : Ime audio datoteke vezane uz trenutni opis vremena.
                            npr. 741 -> "741_v"
        """

        lista_opisa = {
            200: "grmljavina s malo kiše",
            201: "grmljavina s kišom",
            202: "grmljavina s obilnom kišom",
            210: "slaba grmljavina",
            211: "grmljavina",
            212: "razbijena grmljavina",
            221: "grmljavina s laganom rosuljom",
            231: "grmljavina s rosuljom ",
            232: "grmljavina s jakom rosuljom",
            300: "slaba sitna kiša",
            301: "sitna kiša",
            302: "jaka sitna kiša",
            310: "slaba rosulja",
            311: "rosulja",
            312: "jaka rosulja",
            313: "rosulja uz pljuskove",
            314: "jaki pljuskovi i rosulja",
            321: "pljusak i rosulja",
            500: "lagana kiša",
            501: "kiša",
            502: "pljuskovi",
            503: "obilni pljuskovi",
            504: "ekstremni pljuskovi",
            511: "ledena kiša",
            520: "lagani pljusak",
            521: "pljusak",
            522: "jaki pljusak",
            531: "isprekidani pljuskovi",
            600: "lagani snijeg",
            601: "snijeg",
            602: "obilni snijeg",
            611: "susnježica",
            612: "promjenjivo oblačno uz laganu susnježicu",
            613: "promjenjivo oblačno uz susnježicu",
            615: "blaga susnježica",
            616: "susnježica",
            620: "promjenjivo oblačno uz lagani snijeg",
            621: "mećava",
            622: "jaka mećava",
            701: "izmaglica",
            711: "dim",
            721: "sumaglica",
            731: "pješčani ili prašinski vrtlog",
            741: "magla",
            751: "pijesak",
            761: "prašina",
            762: "vulkanski pepeo",
            771: "naleti vjetra",
            781: "tornado",
            800: "vedro",
            801: "blaga naoblaka",
            802: "pretežno vedro",
            803: "promjenjivo oblačno",
            804: "oblačno"

        }
        opisi_vremena = []

        i = 0
        while(i < len(vrijeme_id)):
            if(potreban_podatak == Podatak.TEXT):
                opisi_vremena.append(lista_opisa[vrijeme_id[i]])
            elif(potreban_podatak == Podatak.AUDIO):
                opisi_vremena.append(str(vrijeme_id[i])+"_v")
            i += 1
        i = 0

        return "".join(opisi_vremena) if (len(opisi_vremena) == 1) else " i ".join(opisi_vremena)

    def CepanjeBrojeva(self, broj):
        """
        Funkcija dijeli broj na jedinice, desetice, stotice,...

        Argument:
        --------
            broj          : int / string
                Broj kojeg želimo razdijeliti.

        Vraća:
        -----
            list (string) : Lista brojeva koji su razdijeljeni.
                                npr. 158 -> ["100", "50", "8"]
        """

        broj = list(str(broj))
        negativni_broj = broj[0] == "-"

        if(negativni_broj):
            broj.remove(broj[0])

        i = 0
        for brojka in broj:
            brojka = int(brojka) * pow(10, (len(broj)-(i+1)))
            broj[i] = str(brojka)
            i += 1
        i = 0

        if(len(broj) > 1 and int(broj[-2])+int(broj[-1]) > 10 and int(broj[-2])+int(broj[-1]) < 20):
            broj[-2] = str(int(broj[-2])+int(broj[-1]))
            broj.remove(broj[-1])

        broj = [brojka for brojka in broj if brojka != '0' or (broj[0] == '0' and len(broj) == 1)]

        if(negativni_broj):
            broj.insert(0, "minus")

        return broj

    def BrojURijeci(self, brojevi):
        """
        Funkcija pretvara broj u njegov tekstualni ekvivalent - vrijednosti u rangu 0 - 999.

        Argument:
        --------
            brojevi       : int / list (string)
                Broj kojeg želimo pretvoriti u riječi.
            
        Vraća:
        -----
            list (string) : Lista riječi pretvorenog broja.
                                npr. 218 -> ["dvjesto", "osamnaest"]

        """

        if(type(brojevi)==int):
            brojevi = Vrijeme().CepanjeBrojeva(brojevi)
        izlazRijeci = []
        zadnjiJednoznamenkast = len(brojevi[-1])==1 and (len(brojevi) > 1)
        listaRijeciBrojeva = {
            0: "nula",
            1: "jedan",
            2: "dva",
            3: "tri",
            4: "četiri",
            5: "pet",
            6: "šest",
            7: "sedam",
            8: "osam",
            9: "devet",
            10: "deset",
            -10: "naest",
            100: "sto"
        }

        for broj in brojevi:
            
            if(int(broj) in [11, 12, 13, 14, 15, 16, 17, 18, 19]):
                if(int(broj) == 11):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[-1])] + listaRijeciBrojeva[-10][1:])
                elif(int(broj) == 14):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[-1])][0:3]+'r' + listaRijeciBrojeva[-10])
                elif(int(broj) == 16):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[-1])][0:-1] + listaRijeciBrojeva[-10])
                else:
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[-1])] + listaRijeciBrojeva[-10])

            elif(len(broj) == 2):
                if(int(broj[0])==4):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])][:3]+'r' + listaRijeciBrojeva[int(broj)/int(broj[0])])
                elif(int(broj[0]) in [5,6,9]):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])][:-1] + listaRijeciBrojeva[int(broj)/int(broj[0])])
                else:
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])] + listaRijeciBrojeva[int(broj)/int(broj[0])])

            elif(len(broj) == 3):
                if(int(broj[0])== 1):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj)])
                elif(int(broj[0])== 2):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])][:2]+'je' + listaRijeciBrojeva[int(broj)/int(broj[0])])
                elif(int(broj[0])== 4):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])][:3]+'r' + listaRijeciBrojeva[int(broj)/int(broj[0])])
                elif(int(broj[0]) == 6):
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])][:2] + listaRijeciBrojeva[int(broj)/int(broj[0])])
                else:
                    izlazRijeci.append(listaRijeciBrojeva[int(broj[0])] + listaRijeciBrojeva[int(broj)/int(broj[0])])
            else:
                izlazRijeci.append(listaRijeciBrojeva[int(broj)])
            
        if(zadnjiJednoznamenkast):
            izlazRijeci.insert(-1, "i")

        return izlazRijeci

    def DobaviSatIMinutu(self, podatak):
        """
        Funkcija dobavlja internetsko vrijeme.

        Argument:
        --------
            podatak         : Podatak
                Vrsta podatka kojeg želimo iz funkcije.

        Vraća:
        -----
            ukoliko podatak:
                    Podatak.SAT
                        int : Vraća trenutni sat.
                    Podatak.MINUTA
                        int : Vraća trenutnu minutu.
        """

        sat = int(Vrijeme.stranica.split()[3][11:13])
        minuta = int(Vrijeme.stranica.split()[3][14:16])

        if(podatak == Podatak.SAT):
            return sat
        elif(podatak == Podatak.MINUTA):
            return minuta

    def UvodniPozdrav(self, potreban_podatak, sat):
        """
        Funkcija vraća pozdrav ovisno o satu.

        Argumenti:
        ---------
            potreban_podatak   : Podatak
                Vrsta podatka kojeg želimo iz funkcije.
            sat                : int
                Vrijednost sata koji se koristi za određivanje dijela dana.

        Vraća:
        -----
            ukoliko potreban_podatak:
                    Podatak.TEXT
                        string : Vraća tekstualni pozdrav ovisno o dobu dana.
                                    npr. 7 -> "Dobro jutro..."
                    Podatak.AUDIO
                        string : Vraća ime audio datoteke vezane uz pozdrav.
                                    npr. 21 -> "vecer_pozdrav"
        """

        pozdrav_tekst = "Dobro jutro dragi slušatelji" if 5 <= sat < 12 else "Dobar dan dragi slušatelji" if 12 <= sat < 17 else "Dobra večer dragi slušatelji"
        pozdrav_audio = "jutro_pozdrav" if 5 <= sat < 12 else "dan_pozdrav" if 12 <= sat < 17 else "vecer_pozdrav"

        if(potreban_podatak == Podatak.TEXT):
            return pozdrav_tekst
        elif(potreban_podatak == Podatak.AUDIO):
            return pozdrav_audio

    def Prognoza(self, vrsta_prognoze):
        """
        Funkcija vraća vremensku prognozu.

        Argument:
        --------
            vrsta_prognoze            : Podatak

        Vraća:
        -----
            ukoliko vrsta_prognoze:
                    Podatak.TEXT
                        string        : Ispisuje se vremenska prognoza u tekstualnom obliku.
                    Podatak.TEXT
                        list (string) : Lista riječi koje označavaju imena audio datoteka vezanih za audioreprodukciju.
                    Podatak.MBROLA
                        string        : Tekst vremenske prognoze bez interpunkcijskih znakova najmjenjen za kasniju upotrebu sa MBROLA-om.
        """
        brzina_vjetra = float(Vrijeme().DobaviPodatke(Podatak.JACINA_VJETRA))
        smjer_vjetra = Vrijeme().DobaviPodatke(Podatak.SMJER_VJETRA)
        sat = Vrijeme().DobaviSatIMinutu(Podatak.SAT)
        vrijeme_id = Vrijeme().DobaviPodatke(Podatak.VRIJEME_ID)
        uvod_tekst = Vrijeme().UvodniPozdrav(Podatak.TEXT, sat)
        uvod_audio = Vrijeme().UvodniPozdrav(Podatak.AUDIO, sat)
        naziv_vjetra_tekst = Vrijeme().NazivVjetra(Podatak.TEXT, brzina_vjetra, smjer_vjetra)
        naziv_vjetra_audio = Vrijeme().NazivVjetra(Podatak.AUDIO, brzina_vjetra, smjer_vjetra)
        sat_audio = " ".join(Vrijeme().CepanjeBrojeva(Vrijeme().DobaviSatIMinutu(Podatak.SAT)))
        sat_nastavak = "" if (int(str(sat)[-1]) == 1 and sat != 11) else "a" if (int(str(sat)[-1]) in [2, 3, 4] and int(str(sat)[0]) != 1) else "i"
        minuta = Vrijeme().DobaviSatIMinutu(Podatak.MINUTA)
        minuta_nastavak = "e" if (int(str(minuta)[-1]) in [2, 3, 4] and int(str(minuta)[0]) != 1) else "a"
        minuta_tekst = "i {0} minut{1}".format(Vrijeme().DobaviSatIMinutu(Podatak.MINUTA), minuta_nastavak) if (minuta != 0) else ""
        minuta_tekst_audio = "i {0} minut{1}".format(" i ".join(Vrijeme().CepanjeBrojeva(Vrijeme().DobaviSatIMinutu(Podatak.MINUTA))), minuta_nastavak) if (minuta != 0) else ""
        temperatura = Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)
        temperatura_audio = " ".join(Vrijeme().CepanjeBrojeva(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA))))
        temperatura_nastavak = "anj" if (int(str(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)))[-1]) == 1 and int(str(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)))) != 11) else "nja"
        opis_vremena_tekst = Vrijeme().OpisVremena(Podatak.TEXT, vrijeme_id)
        opis_vremena_audio = Vrijeme().OpisVremena(Podatak.AUDIO, vrijeme_id)

        mbrola_sat = " ".join(Vrijeme().BrojURijeci(Vrijeme().CepanjeBrojeva(sat)))
        mbrola_minuta = " ".join(Vrijeme().BrojURijeci(Vrijeme().CepanjeBrojeva(minuta)))
        mbrola_minuta_tekst = "i {0} minut{1}".format(mbrola_minuta, minuta_nastavak) if (minuta != 0) else ""
        mbrola_temperatura_podatak = Vrijeme().CepanjeBrojeva(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)))
        mbrola_temperatura_minus = mbrola_temperatura_podatak[0]=="minus"
        mbrola_temperatura_tekst = (mbrola_temperatura_podatak[0] + " " if (mbrola_temperatura_minus) else "") + (" ".join(Vrijeme().BrojURijeci(mbrola_temperatura_podatak)) if(not mbrola_temperatura_minus) else " ".join(Vrijeme().BrojURijeci(mbrola_temperatura_podatak[1:])))


        if(vrsta_prognoze == Podatak.TEXT):
            print("{0}. {1} je sat{2} {3}. Vani je {4}°C, {5} je{6}".format(uvod_tekst, sat, sat_nastavak, minuta_tekst, temperatura, opis_vremena_tekst, naziv_vjetra_tekst))
        elif(vrsta_prognoze == Podatak.AUDIO):
            return "{0} {1} je sat{2} {3} Vani je {4} stup{5} {6} je{7}".format(uvod_audio, sat_audio, sat_nastavak, minuta_tekst_audio, temperatura_audio, temperatura_nastavak, opis_vremena_audio, naziv_vjetra_audio).lower().split()
        elif(vrsta_prognoze == Podatak.MBROLA):
            return "{0} {1} je sat{2} {3} vani je {4} stup{5} {6} je{7}".format(uvod_tekst, mbrola_sat, sat_nastavak, mbrola_minuta_tekst, mbrola_temperatura_tekst, temperatura_nastavak, opis_vremena_tekst, naziv_vjetra_tekst[1:-1])

    def ZapisMBROLA(self, tekst):
        """
        Funkcija dijeli tekst u hrvatska slova, te ih zapisuje u tekstualnu datoteku u paru sa njihovim trajanjem (ms).

        Argument:
        --------
            tekst : string
                Tekst koji se dijeli na slova.

        Rezultat:
        --------
            file   : Datoteka sa ispisanim parovima slova i trajanja istih, prilagođena za upotrebu sa MBROLA-om.
                        npr. "Riječ" -> r - 25
                                        i - 49
                                        j - 53
                                        e - 53
                                        č - 90

        """

        tekst = tekst.lower()
        trajanjeSlova = {
            "a" : 61,
            "b" : 65,
            "c" : 113,
            "č" : 90,
            "ć" : 98,
            "d" : 54,
            "dž" : 56,
            "đ" : 61,
            "e" : 53,
            "f" :  86,
            "g" : 56,
            "h" :  68,
            "i" : 49,
            "j" : 53,
            "k" : 81,
            "l" : 35,
            "lj" : 59,
            "m" : 56,
            "n" : 45,
            "nj" : 60,
            "o" : 54,
            "p" : 85,
            "r" : 25,
            "s" : 91,
            "š" : 99,
            "t" : 76,
            "u" : 50,
            "v" : 40,
            "z" : 68,
            "ž" : 74

        }
        zapis = open("mbrola_zapis.txt", 'w+', encoding = "UTF-8")

        tekst = list("".join(tekst.split()))
        duljinaTeksta = len(tekst)
        i=0
        while(i < duljinaTeksta):
            dvoslov = tekst[i-1]+tekst[i]
            if(dvoslov in ["dž","lj","nj"]):
                zapis.write("{0} - {1}".format(dvoslov, trajanjeSlova[dvoslov]))
                i +=1
            else:
                slovo = tekst[i]
                zapis.write("{0} - {1}".format(slovo, trajanjeSlova[slovo]))
            if(i < duljinaTeksta-1):
                zapis.write('\n')
            i += 1
        zapis.close()
