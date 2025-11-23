# IULKFF_parkol-
A program célja:
- parkolóhelyek foglaltsági állapotának megjelenítése (zöld = szabad, piros = foglalt)
- rendszám megadása és parkolás indítása
- távozáskor a parkolási díj automatikus kiszámítása
- az állapotok tartós mentése SQLite adatbázisba
  
Használt osztály:
ParkingGUI_FÁ
 -teljes Tkinter felület
 
 -gombok, mezők
 -parkolás és távozás
 -fizetési ablak
 -adatok mentése SQL-be
AdatokSQL_FÁ
közvetlenül hívható: AdatokSQL.load_all()

Modulok:
Adatmento_FÁ
  -adatbázis létrehozása
  -adatok betöltése
  -adatok mentése
  -hiányzó rekordok automatikus létrehozása
datetime
tkinter
Függvények:
def __init__
  -ablak létrehozása
  -adatbázis inicializálás
  -adatok betöltése SQL-ből
  -UI két részre osztása
  -gombok és vezérlőpanel létrehozása
def create_parking_buttons_FÁ
     -10 db parkolóhely gomb generálása
     -gomb színe → adatok alapján
     -gombhoz kattintási esemény hozzáadása
def select_spot_FÁ
  eltárolja a kiválasztott parkolóhelyet
  frissíti a jobb oldali info panelt
  ha foglalt → rendszámot beírja a mezőbe
def create_control_panel_FÁ
    jobb oldali UI kialakítása:
    kiválasztott hely kiírása
    rendszám mező
    parkolás és távozás gombok
def occupy_spot_FÁ
ellenőrzések:
      kiválasztott-e hely?
      szabad-e?
      van-e rendszám?
      foglalás indítása
      SQL mentés
      UI frissítése (piros gomb)
def free_spot_FÁ
ellenőrzések:
    kiválasztott hely
    van-e kezdési idő → foglalt-e?
    parkolás időtartam számítása
    fizetési ablak létrehozása
    fizetés gomb logikája: visszaállítás + SQL mentés
def fizetes_gomb
def init_db
def load_all
def save_spot


