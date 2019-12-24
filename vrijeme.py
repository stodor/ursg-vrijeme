import urllib.request
from enum import Enum

class Vrijeme:

 #   def __Print2():
    #    print("B")

  #  def Print():
  #      Vrijeme._Vrijeme__Print2()

    global SMJER_VJETRA, JACINA_VJETRA, NAZIV_VJETRA, TEMPERATURA, VRIJEME_ID
    SMJER_VJETRA = 0
    JACINA_VJETRA = 1
    NAZIV_VJETRA = 2
    TEMPERATURA = 3
    VRIJEME_ID = 4

    def NazivVjetra(smjer):
      nazivi_vjetrova = ["sjeverni","sjeveroistočni","istočni","jugoistočni","južni","jugozapadni","zapadni","sjeverozapadni"]
      naziv = nazivi_vjetrova[int(((float(smjer)+(360/(len(nazivi_vjetrova)*2)))%360)/(360/len(nazivi_vjetrova)))]

      return naziv
    
    def OpisVremena():
      opisi_vremena = {
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
      vrijeme_id = Vrijeme.DobaviPodatke(VRIJEME_ID)
      return opisi_vremena.get(int(vrijeme_id))



    def CepanjeBrojeva(broj):
      broj = list(str(broj))
      negativni_broj = broj[0] == "-"

      if(negativni_broj):
        broj.remove(broj[0])

      indeks = 0 
      for brojka in broj :
        brojka = int(brojka) * pow(10, (len(broj)-(indeks+1)))        
        broj[indeks] = str(brojka)
        indeks +=1
    
      if(len(broj) > 1 and int(broj[-2])+int(broj[-1]) > 10 and int(broj[-2])+int(broj[-1]) < 20):
        broj[-2] = str(int(broj[-2])+int(broj[-1]))
        broj.remove(broj[-1])
        
      broj = [brojka for brojka in broj if brojka != '0' or (broj[0] == '0' and len(broj)==1)]
    
      if(negativni_broj):
        broj.insert(0, "minus")
        
      return broj



    def DobaviSat():
      stranica = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())
      sat = int(stranica.split()[3][11:13])
  
      return sat

    def DobaviMinutu():
      stranica = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())
      minuta = int(stranica.split()[3][14:16])

      return minuta


    def UvodniPozdrav():
      sat = Vrijeme.DobaviSat()
      pozdrav = "Dobro jutro dragi slušatelji" if 5 <= sat < 12 else "Dobar dan dragi slušatelji" if 12<= sat < 17 else "Dobra večer dragi slušatelji"

      return pozdrav


    def DobaviPodatke(potreban_podatak):
      lista_podataka = []

      stranica = str(urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=b0cf9d4de9f5ff964a853090bd6cb6b2&units=metric").read()).replace('}','').replace('{','').replace('[','').replace(']','')
      stranica = stranica[2:].replace('"','').replace(',',':').split(':')
      for i in stranica:
        lista_podataka.append(i)
      stranica = None

      
      smjer_vjetra = 0 if "deg" not in lista_podataka else lista_podataka[lista_podataka.index("deg")+1]
      naziv_vjetra = Vrijeme.NazivVjetra(smjer_vjetra)
      jacina_vjetra = 0 if "wind" not in lista_podataka else lista_podataka[lista_podataka.index("wind")+2]
      temperatura = 0 if "temp" not in lista_podataka else lista_podataka[lista_podataka.index("temp")+1]
      vrijeme_id = lista_podataka[lista_podataka.index("id")+1]

      if(potreban_podatak == SMJER_VJETRA):
        return smjer_vjetra
      elif(potreban_podatak == JACINA_VJETRA):
        return jacina_vjetra
      elif(potreban_podatak == NAZIV_VJETRA):
        return naziv_vjetra
      elif(potreban_podatak == TEMPERATURA):
        return temperatura
      elif(potreban_podatak == VRIJEME_ID):
        return vrijeme_id
      
      stranica = None

    def TekstualnaPrognoza():
      uvod = Vrijeme.UvodniPozdrav()
      sat = Vrijeme.DobaviSat()
      sat_nastavak = "" if (int(str(sat)[-1]) == 1 and sat != 11) else "a" if (int(str(sat)[-1]) in [2,3,4] and int(str(sat)[0]) != 1) else "i"
      minuta = Vrijeme.DobaviMinutu()
      minuta_nastavak = "e" if (int(str(minuta)[-1]) in [2,3,4] and int(str(minuta)[0]) != 1) else "a"
      minuta_tekst = "i {0} minut{1}".format(Vrijeme.DobaviMinutu(), minuta_nastavak) if (minuta != 0) else ""
      temperatura = Vrijeme.DobaviPodatke(TEMPERATURA)
      opis_vremena = Vrijeme.OpisVremena()

      print("{0}. {1} je sat{2} {3}. Vani je {4}°C te je {5}.".format(Vrijeme.UvodniPozdrav(), Vrijeme.DobaviSat(), sat_nastavak, minuta_tekst, Vrijeme.DobaviPodatke(TEMPERATURA), Vrijeme.OpisVremena()))