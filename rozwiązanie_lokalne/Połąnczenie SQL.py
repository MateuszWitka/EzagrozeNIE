# trzeba zainstalować biblioteki: pip install psycopg2-binary pandas scikit-learn
import psycopg2
import pandas as pd

# --- KONFIGURACJA POŁĄCZENIA ---
DB_CONFIG = {
    "host": "psql.wmi.amu.edu.pl",
    "database": "s453969_proj",
    "user": "s453969_proj",
    "password": "iallintingskedd",
    "port": "5432"
}

def analyze_wypadki_2020(conn):
    """
    Funkcja wykonująca zestaw analiz na tabeli 'dane.wypadki_lubuskie_przetworzone_2020'
    """
    print("\n" + "="*60)
    print(" RAPORT DANYCH: Wypadki Lubuskie 2020")
    print("="*60)

    # 1. Podgląd danych
    print("\n---> [1] Podgląd przykładowych 5 wierszy:")
    query_preview = """
        SELECT id, miejscowosc, ulica, predkosc_dopuszczalna, warunki_atmosferyczne 
        FROM dane.wypadki_lubuskie_przetworzone_2020 
        LIMIT 5;
    """
    df_preview = pd.read_sql(query_preview, conn)
    print(df_preview.to_string(index=False))

    # 2. Ranking miast (Gdzie było najwięcej wypadków?)
    print("\n---> [2] Top 5 miejscowości z największą liczbą wypadków:")
    query_cities = """
        SELECT miejscowosc, COUNT(*) as liczba_wypadkow
        FROM dane.wypadki_lubuskie_przetworzone_2020
        GROUP BY miejscowosc
        ORDER BY liczba_wypadkow DESC
        LIMIT 5;
    """
    df_cities = pd.read_sql(query_cities, conn)
    print(df_cities.to_string(index=False))

    # 3. Analiza nawierzchni
    print("\n---> [3] Statystyka: Rodzaj nawierzchni a liczba zdarzeń:")
    query_surface = """
        SELECT rodzaj_nawierzchni, COUNT(*) as ilosc
        FROM dane.wypadki_lubuskie_przetworzone_2020
        GROUP BY rodzaj_nawierzchni
        ORDER BY ilosc DESC;
    """
    df_surface = pd.read_sql(query_surface, conn)
    print(df_surface.to_string(index=False))

def connect_and_run():
    conn = None
    try:
        print(f"--> Łączenie z bazą: {DB_CONFIG['database']} na serwerze {DB_CONFIG['host']}...")

        # Nawiązanie połączenia
        conn = psycopg2.connect(**DB_CONFIG)
        print("--> Połączono pomyślnie!")

        # Uruchomienie analizy dla tabeli 2020
        analyze_wypadki_2020(conn)

    except psycopg2.OperationalError as e:
        print("\n[BŁĄD POŁĄCZENIA] Nie udało się połączyć z serwerem.")
        print(f"Szczegóły błędu: {e}")
        print("Wskazówka: Sprawdź czy jesteś w sieci uniwersyteckiej (VPN) i czy pole 'user' jest poprawne.")

    except Exception as e:
        print(f"\n[INNY BŁĄD]: {e}")

    finally:
        if conn:
            conn.close()
            print("\n--> Połączenie zamknięte.")

if __name__ == "__main__":
    connect_and_run()