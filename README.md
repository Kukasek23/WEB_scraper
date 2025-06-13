# WEBOVÝ SCRAPER PRO ZJIŠŤOVÁNÍ VÝSLEDKŮ VOLEB Z ROKU 2017 ze stránky volby.cz

Webový scraper pro zjišťování výsledků volub z roku 2017

Tento Python skript slouží k automatickému stahování (scrapování) dat o výsledcích voleb z webové stránky volby.cz. Lze díky němu získat např. seznam obcí v každém kraji a pro každou obec podrobnosti o počtu registrovaných voličů, vydaných obálek. Data o každé obcci jsou uložena do CSV souboru.

###Funkce scriptu:
1) Načte seznam obcí - Navštíví sstránku s přehledem obcí v zadaném kraji a extrahuje jejich identifikační kódy a názvy
2) U každé obce načte detailní stránku s výsledky voleb
3) Z detailní stránky s výsledky voleb po každou obec scraper získává: a) počet registrovaných voličů
                                                                       b) počet vydaných obálek
                                                                       c) počet platných hlasů
                                                                       d) hlasy pro jednotlivé politické strany (názvy a počty hlasů)

4) Ukládá data do CSV souboru: Všechna získaná data o volbách v obci jsou systematicky zapsána do CSV souboru, jehož název je zvolen jako jeden z argumentů při spouštění programu

###Spouštění programu:
- Program je spouštěn přímo z příkazové řádky (command line)
- Pro jeho spuštění jsou vyžadovány dva argumenty: URL stránky pro sběr dat a název výstupního CSV souboru
1) Uložte kód do souboru s příponou .py (například volby_scraper.py)
2) Otevřete terminál nebo příkazový řádek
3) Přejděte do adresáře s tímto souborem
4) Spusťte skript příkazem: python volby_scraper.py <URL> <vystupni_soubor.csv> ; například: python volby_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "Vysledky_Benesov.csv"
   - V této ukázce je URL stránky pro skrapování (v tomto případě Benešov, volby 2017). Vysledky_Benesov.csv je název souboru, do kterého budou data uložena. Skript automaticky uloží vyscrapovaná data so douboru .csv.

###Požadavky a instalace:
- Před spuštěním se ujistěte, že máte nainstalované potřebné knihovny uvedené v souboru `requirements.txt`.
- Instalaci potřebných knihoven provedete v příkazovém řádku nebo terminálu ve stejném adresáři jako váš script a soubor `requirements.txt` spuštěním příkazu:
  pip install -r requirements.txt
  
```bash
pip install -r requirements.txt

