import urllib.request
import json
from enum import Enum

class Podatak(Enum):
  SMJER_VJETRA = 0
  JACINA_VJETRA = 1
  NAZIV_SMJERA_VJETRA = 2
  TEMPERATURA = 3
  VRIJEME_ID = 4
  TEXT = 5
  AUDIO = 6
  SAT = 7
  MINUTA = 8

class Vrijeme:
    podatci = json.loads(urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=b0cf9d4de9f5ff964a853090bd6cb6b2&units=metric").read().decode())
    stranica = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())

    def DobaviPodatke(self, potreban_podatak):      
      
      #podatci = json.loads(urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=b0cf9d4de9f5ff964a853090bd6cb6b2&units=metric").read().decode())
      
      smjer_vjetra = 0 if "deg" not in Vrijeme.podatci["wind"] else Vrijeme.podatci["wind"]["deg"]
      naziv_smjera_vjetra = Vrijeme().NazivSmjerVjetra(smjer_vjetra)
      jacina_vjetra = 0 if "speed" not in Vrijeme.podatci["wind"] else Vrijeme.podatci["wind"]["speed"]
      temperatura = 0 if "temp" not in Vrijeme.podatci["main"] else Vrijeme.podatci["main"]["temp"]
      vremena_u_podacima = Vrijeme.podatci["weather"]
      vremena_idjevi = []

      i = 0
      while(i < len(vremena_u_podacima)):
        vremena_idjevi.append(vremena_u_podacima[i]["id"])
        i +=1
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
      smjerovi_vjetrova = ["sjeverni","sjeveroistočni","istočni","jugoistočni","južni","jugozapadni","zapadni","sjeverozapadni"]
      naziv = smjerovi_vjetrova[int(((float(smjer)+(360/(len(smjerovi_vjetrova)*2)))%360)/(360/len(smjerovi_vjetrova)))]

      return naziv

    def NazivVjetra(self, vrsta_prognoze):
      nazivi_vjetrova = ["tišina","lahor","povjetarac","slab vjetar","umjeren vjetar","umjereno jak vjetar","jak vjetar","žestoki vjetar","olujni vjetar","jak olujni vjetar","orkanski vjetar","jak orkanski vjetar","orkan"]
      # Beaufortova ljestvica

      brzina = float(Vrijeme().DobaviPodatke(Podatak.JACINA_VJETRA))
      
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

      smjer = Vrijeme().DobaviPodatke(Podatak.SMJER_VJETRA)
      smjer_vjetra_naziv = Vrijeme().NazivSmjerVjetra(smjer)
      prognoza_tekst = "." if(vjetar_indeks==0) else ", te puše {0} {1}.".format(smjer_vjetra_naziv, nazivi_vjetrova[vjetar_indeks])
      prognoza_audio = "" if(vjetar_indeks==0) else " te puše {0} {1}".format(smjer_vjetra_naziv, nazivi_vjetrova[vjetar_indeks])
      
      if(vrsta_prognoze == Podatak.TEXT):
        return prognoza_tekst
      elif(vrsta_prognoze == Podatak.AUDIO):
        return prognoza_audio
    
    def OpisVremena(self):
      lista_opisa = {
        200 : "thunderstorm with light rain",
        201 : "thunderstorm with rain",
        202 : "thunderstorm with heavy rain",
        210 : "light thunderstorm",
        211 : "thunderstorm",
        212 : "ragged thunderstorm",
        221 : "thunderstorm with light drizzle",
        231 : "thunderstorm with drizzle",
        232 : "thunderstorm with heavy drizzle",
        300 : "light intensity drizzle",
        301 : "drizzle",
        302 : "heavy intensity drizzle",
        310 : "light intensity drizzle rain",
        311 : "drizzle rain",
        312 : "heavy intensity drizzle rain",
        313 : "shower rain and drizzle",
        314 : "heavy shower rain and drizzle",
        321 : "shower drizzle",
        500 : "light rain" ,
        501 : "moderate rain",
        502 : "heavy intensity rain",
        503 : "very heavy rain",
        504 : "extreme rain",
        511 : "freezing rain",
        520 : "light intensity shower rain",
        521 : "shower rain",
        522 : "heavy intensity shower rain",
        531 : "ragged shower rain",
        600 : "light snow",
        601 : "Snow",
        602 : "Heavy snow",
        611 : "Sleet",
        612 : "Light shower sleet	",
        613 : "Shower sleet	",
        615 : "Light rain and snow",
        616 : "Rain and snow",
        620 : "Light shower snow",
        621 : "Shower snow",
        622 : "Heavy shower snow",
        701 : "Mist",
        711 : "Smoke",
        721 : "Haze",
        731 : "sand/ dust whirls",
        741 : "fog",
        751 : "sand",
        761 : "dust",
        762 : "volcanic ash",
        771 : "squalls",
        781 : "tornado",
        800 : "clear sky",
        801 : "few clouds: 11-25%",
        802 : "scattered clouds: 25-50%",
        803 : "broken clouds: 51-84%",
        804 : "overcast clouds: 85-100%"
      }
      vrijeme_id = Vrijeme().DobaviPodatke(Podatak.VRIJEME_ID)
      opisi_vremena = []

      i = 0
      while(i < len(vrijeme_id)):
        opisi_vremena.append(lista_opisa[vrijeme_id[i]])
        i += 1
      i = 0
      
      return "".join(opisi_vremena) if (len(opisi_vremena) == 1) else " i ".join(opisi_vremena)



    def CepanjeBrojeva(self, broj):
      broj = list(str(broj))
      negativni_broj = broj[0] == "-"

      if(negativni_broj):
        broj.remove(broj[0])

      i = 0 
      for brojka in broj :
        brojka = int(brojka) * pow(10, (len(broj)-(i+1)))        
        broj[i] = str(brojka)
        i +=1
      i = 0 
    
      if(len(broj) > 1 and int(broj[-2])+int(broj[-1]) > 10 and int(broj[-2])+int(broj[-1]) < 20):
        broj[-2] = str(int(broj[-2])+int(broj[-1]))
        broj.remove(broj[-1])
        
      broj = [brojka for brojka in broj if brojka != '0' or (broj[0] == '0' and len(broj)==1)]
    
      if(negativni_broj):
        broj.insert(0, "minus")
        
      return broj



    def DobaviSatIMinutu(self, podatak):
      #stranica = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())
      sat = int(Vrijeme.stranica.split()[3][11:13])
      minuta = int(Vrijeme.stranica.split()[3][14:16])

      if(podatak == Podatak.SAT):
        return sat
      elif(podatak == Podatak.MINUTA):
        return minuta


    def UvodniPozdrav(self):
      sat = Vrijeme().DobaviSatIMinutu(Podatak.SAT)
      pozdrav = "Dobro jutro dragi slušatelji" if 5 <= sat < 12 else "Dobar dan dragi slušatelji" if 12 <= sat < 17 else "Dobra večer dragi slušatelji"

      return pozdrav

    def Prognoza(self, vrsta_prognoze):
      uvod = Vrijeme().UvodniPozdrav()
      naziv_vjetra_tekst = Vrijeme().NazivVjetra(Podatak.TEXT)
      naziv_vjetra_audio = Vrijeme().NazivVjetra(Podatak.AUDIO)
      sat = Vrijeme().DobaviSatIMinutu(Podatak.SAT)
      sat_audio = " ".join(Vrijeme().CepanjeBrojeva(Vrijeme().DobaviSatIMinutu(Podatak.SAT)))
      sat_nastavak = "" if (int(str(sat)[-1]) == 1 and sat != 11) else "a" if (int(str(sat)[-1]) in [2,3,4] and int(str(sat)[0]) != 1) else "i"
      minuta = Vrijeme().DobaviSatIMinutu(Podatak.MINUTA)
      minuta_nastavak = "e" if (int(str(minuta)[-1]) in [2,3,4] and int(str(minuta)[0]) != 1) else "a"
      minuta_tekst = "i {0} minut{1}".format(Vrijeme().DobaviSatIMinutu(Podatak.MINUTA), minuta_nastavak) if (minuta != 0) else ""
      minuta_tekst_audio = "i {0} minut{1}".format(" i ".join(Vrijeme().CepanjeBrojeva(Vrijeme().DobaviSatIMinutu(Podatak.MINUTA))), minuta_nastavak) if (minuta != 0) else ""
      temperatura = Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)
      temperatura_audio = " ".join(Vrijeme().CepanjeBrojeva(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA))))
      temperatura_nastavak = "anj" if (int(str(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)))[-1]) == 1 and int(str(int(Vrijeme().DobaviPodatke(Podatak.TEMPERATURA)))) != 11) else "nja"
      opis_vremena = Vrijeme().OpisVremena()

      if(vrsta_prognoze == Podatak.TEXT):
        print("{0}. {1} je sat{2} {3}. Vani je {4}°C, {5} je{6}".format(uvod, sat, sat_nastavak, minuta_tekst, temperatura, opis_vremena, naziv_vjetra_tekst))
      elif(vrsta_prognoze == Podatak.AUDIO):
        return "{0} {1} je sat{2} {3} Vani je {4} stup{5} {6} je{7}".format(uvod, sat_audio, sat_nastavak, minuta_tekst_audio, temperatura_audio, temperatura_nastavak, opis_vremena, naziv_vjetra_audio).lower().split()