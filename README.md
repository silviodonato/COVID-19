# 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE


This is the data repository for the 2019 Novel Coronavirus Visual Dashboard operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). Also, Supported by ESRI Living Atlas Team and the Johns Hopkins University Applied Physics Lab (JHU APL).

<<<<<<< HEAD
<<<<<<< HEAD
<br>

<b>Visual Dashboard (desktop):</b><br>
https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6
<br><br>
<b>Visual Dashboard (mobile):</b><br>
http://www.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61
<br><br>
<b>Lancet Article:</b><br>
[An interactive web-based dashboard to track COVID-19 in real time](https://doi.org/10.1016/S1473-3099(20)30120-1)
<br><br>
<b>Provided by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE):</b><br>
https://systems.jhu.edu/
<br><br>
<b>Data Sources:</b><br>
* World Health Organization (WHO): https://www.who.int/ <br>
* DXY.cn. Pneumonia. 2020. http://3g.dxy.cn/newh5/view/pneumonia.  <br>
* BNO News: https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/  <br>
* National Health Commission of the People’s Republic of China (NHC): <br>
 http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml <br>
* China CDC (CCDC): http://weekly.chinacdc.cn/news/TrackingtheEpidemic.htm <br>
* Hong Kong Department of Health: https://www.chp.gov.hk/en/features/102465.html <br>
* Macau Government: https://www.ssm.gov.mo/portal/ <br>
* Taiwan CDC: https://sites.google.com/cdc.gov.tw/2019ncov/taiwan?authuser=0 <br>
* US CDC: https://www.cdc.gov/coronavirus/2019-ncov/index.html <br>
* Government of Canada: https://www.canada.ca/en/public-health/services/diseases/coronavirus.html <br>
* Australia Government Department of Health: https://www.health.gov.au/news/coronavirus-update-at-a-glance <br>
* European Centre for Disease Prevention and Control (ECDC): https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases 
* Ministry of Health Singapore (MOH): https://www.moh.gov.sg/covid-19
* Italy Ministry of Health: http://www.salute.gov.it/nuovocoronavirus
* 1Point3Arces: https://coronavirus.1point3acres.com/en
* WorldoMeters: https://www.worldometers.info/coronavirus/

<br>
<b>Additional Information about the Visual Dashboard:</b><br>
https://systems.jhu.edu/research/public-health/ncov/
<br><br>
=======
## README e Wiki in aggiornamento (nuova versione - 28/03/2020 @ 08:00)
## README and Wiki under update (new version - 28/03/2020 @ 08:00)
=======
## README e Wiki in aggiornamento (nuova versione - 01/04/2020 @ 08:00)
## README and Wiki under update (new version - 01/04/2020 @ 08:00)

## Stiamo lavorando per fornire nuovi dataset e dashboard e perfezionamento di quelli esistenti.
## We are working to provide new datasets and dashboard and refinement of existing ones.
>>>>>>> 259cf42f36086e81c9825f0f2b676ac205b90263

## Aggiornamenti dataset 
## Dataset update

In note_it e note_en sarà riportato il codice del messaggio definito nel dataset "note"<br>
In note_it and note_en will be reported the message code defined in "note" dataset

* dati_regioni
data,stato,codice_regione,denominazione_regione,lat,long,ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,note_it,note_en
2020-03-24T17:00:00,ITA,13,Abruzzo,42.35122196,13.39843823,234,57,291,331,622,17,21,46,689,4294,,

* dati_province
data,stato,codice_regione,denominazione_regione,codice_provincia,denominazione_provincia,sigla_provincia,lat,long,totale_casi,note_it,note_en
2020-03-24T17:00:00,ITA,13,Abruzzo,069,Chieti,CH,42.35103167,14.16754574,133,Adnp-IT-01,Adnp-EN-01

* dati_andamento_nazionale
data,stato,ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi,note_it,note_en
2020-03-24T17:00:00,ITA,21937,3396,25333,28697,54030,3612,8326,6820,69176,296964,Adnp-IT-01,Adnp-EN-01

* note_it
codice,data,dataset,stato,codice_regione,regione,codice_provincia,provincia,sigla_provincia,tipologia_avviso,avviso,note
nd-IT-01,2020-03-24T17:00:00,ITA,13,Abruzzo,069,Chieti,CH,dati non pervenuti,mancata comunicazione dati,

* note_en
codice,data,dataset,stato,codice_regione,regione,codice_provincia,provincia,sigla_provincia,tipologia_avviso,avviso,note
nd-EN-01,2020-03-24T17:00:00,ITA,13,Abruzzo,069,Chieti,CH,no data received,no data communication,

```diff
Da mercoledì 25/03/2020 (aggiornamento 18:30)
1. ogni data sarà convertita nel formato standard ISO8601: *YYYY-MM-DDTHH:MM:SS* - *2020-03-18T19:14:29*. Tutte le date saranno in UTC.
2. ad ogni dataset sarà aggiunto un campo note per dare informazioni sul dato specifico
3. sarà realizzato un nuovo dataset per fornire informazioni sui dati

From Wednesday 25/03/2020 (update 18:30)
1. every date will be converted in ISO8601 format standard: *YYYY-MM-DDTHH:MM:SS* - *2020-03-18T19:14:29*. All dates will be in UTC.
2. a note field will be added to each dataset to give informations on the specific data
3. a new dataset will be released to give informations on data
```

## Wiki (in costruzione/under construction)

[Wiki](https://github.com/pcm-dpc/COVID-19/wiki)<br>
[Esempio di pagina](https://github.com/pcm-dpc/COVID-19/wiki/1.it-Dati:-andamento-nazionale)

## Avvisi

```diff
- 29/03/2020: dati Regione Emilia Romagna parziali (dato tampone non aggiornato).
- 26/03/2020: dati Regione Piemonte parziali (-50 deceduti - comunicazione tardiva).
- 18/03/2020: dati Regione Campania non pervenuti.
- 18/03/2020: dati Provincia di Parma non pervenuti.
- 17/03/2020: dati Provincia di Rimini non aggiornati.
- 16/03/2020: dati P.A. Trento e Puglia non pervenuti.
- 11/03/2020: dati Regione Abruzzo non pervenuti.
- 10/03/2020: dati Regione Lombardia parziali.
- 07/03/2020: dati Brescia +300 esiti positivi
```
 

[Sito del Dipartimento della Protezione Civile - Emergenza Coronavirus: la risposta nazionale](http://www.protezionecivile.it/attivita-rischi/rischio-sanitario/emergenze/coronavirus)


Il 31 gennaio 2020, il Consiglio dei Ministri dichiara lo stato di emergenza, per la durata di sei mesi, in conseguenza del rischio sanitario connesso all'infezione da Coronavirus.

Al Capo del Dipartimento della Protezione Civile, Angelo Borrelli, è affidato il coordinamento degli interventi necessari a fronteggiare l'emergenza sul territorio nazionale.  
  
Le principali azioni coordinate dal Capo del Dipartimento sono volte al soccorso e all'assistenza della popolazione eventualmente interessata dal contagio, al potenziamento dei controlli nelle aree aeroportuali e portuali, in continuità con le misure urgenti già adottate dal Ministero della salute, al rientro in Italia dei cittadini che si trovano nei Paesi a rischio e al rimpatrio dei cittadini stranieri nei Paesi di origine esposti al rischio.

Per informare i cittadini e mettere a disposizione i dati raccolti, utili ai soli fini comunicativi e di informazione, il Dipartimento della Protezione Civile ha elaborato un cruscotto geografico interattivo raggiungibile agli indirizzi  [http://arcg.is/C1unv](http://arcg.is/C1unv) (versione desktop) e [http://arcg.is/081a51](http://arcg.is/081a51) (versione mobile) e mette a disposizione, con licenza CC-BY-4.0, le seguenti informazioni aggiornate quotidianamente alle 18:30 (successivamente la conferenza stampa del Capo Dipartimento):

- Andamento nazionale
- Dati json
- Dati province
- Dati regioni
- Schede riepilogative
- Aree

## Struttura del repository
```
COVID-19/
│
├── andamento-nazionale/
│   ├── dpc-covid19-ita-andamento-nazionale-yyyymmdd.csv
├── aree/
│   ├── geojson
│   │   ├── dpc-covid19-ita-aree.geojson
│   ├── shp
│   │   ├── dpc-covid19-ita-aree.shp
├── dati-province/
│   ├── dpc-covid19-ita-province-yyyymmdd.csv
├── dati-json/
│   ├── dpc-covid19-ita-*.json
├── dati-regioni/
│   ├── dpc-covid19-ita-regioni-yyyymmdd.csv
├── schede-riepilogative/
│   ├── province
│   │   ├── dpc-covid19-ita-scheda-province-yyyymmdd.pdf
│   ├── regioni
│   │   ├── dpc-covid19-ita-scheda-regioni-yyyymmdd.pdf
```


## Formato dei dati

### Dati per Regione

**Directory:**  dati-regioni<br>
**Struttura file giornaliero:** dpc-covid19-ita-regioni-yyyymmdd.csv (dpc-covid19-ita-regioni-20200224.csv)<br>
**File complessivo:** dpc-covid19-ita-regioni.csv<br>
**File ultimi dati (latest):** dpc-covid19-ita-regioni-latest.csv

| Nome campo                  | Descrizione                       | Description                            | Formato                       | Esempio             |
|-----------------------------|-----------------------------------|----------------------------------------|-------------------------------|---------------------|
| **data**                        | Data dell’informazione            | Date of notification                   | YYYY-MM-DD HH:MM:SS (ISO 8601) Ora italiana | 2020-03-05 12:15:45 |
| **stato**                       | Stato di riferimento              | Country of reference                   | XYZ (ISO 3166-1 alpha-3)      | ITA                 |
| **codice_regione**              | Codice della Regione (ISTAT 2019) | Code of the Region (ISTAT 2019)        | Numero                        | 13                  |
| **denominazione_regione**       | Denominazione della Regione       | Name of the Region                     | Testo                         | Abruzzo             |
| **lat**                         | Latitudine                        | Latitude                               | WGS84                         | 42.6589177          |
| **long**                        | Longitudine                       | Longitude                              | WGS84                         | 13.70439971         |
| **ricoverati_con_sintomi**      | Ricoverati con sintomi            | Hospitalised patients with symptoms    | Numero                        | 3                   |
| **terapia_intensiva**           | Ricoverati in terapia intensiva   | Intensive Care                         | Numero                        | 3                   |
| **totale_ospedalizzati**        | Totale ospedalizzati              | Total hospitalised patients            | Numero                        | 3                   |
| **isolamento_domiciliare**      | Persone in isolamento domiciliare | Home confinement                       | Numero                        | 3                   |
| **totale_attualmente_positivi** | Totale attualmente positivi (ospedalizzati + isolamento domiciliare)      | Total amount of current positive cases (Hospitalised patients + Home confinement)  | Numero                        | 3                   |
| **nuovi_attualmente_positivi**  | Nuovi attualmente positivi (Totale attualmente positivi attuali - Totale attualmente positivi del giorno prima)       | News amount of current positive cases (Actual total amount of current positive cases - total amount of current positive cases of the previous day)  | Numero                        | 3                   |
| **dimessi_guariti**             | Persone dimesse guarite           | Recovered                              | Numero                        | 3                   |
| **deceduti**                    | Persone decedute                  | Death                                  | Numero                        | 3                   |
| **totale_casi**                 | Totale casi positivi              | Total amount of positive cases         | Numero                        | 3                   |
| **tamponi**                     | Totale tamponi                    | Tests performed                        | Numero                        | 3                   |


*Le Province autonome di Trento e Bolzano sono indicate in "denominazione regione" e con il codice 04 del Trentino Alto Adige.*<br>
*Viene messo a disposizione un file JSON complessivo di tutte le date nella cartella "dati-json": dpc-covid19-ita-regioni.json* e rispettivo file ultimi dati (latest) dpc-covid19-ita-regioni-latest.json

### Dati per Provincia

**Directory:**  dati-province<br>
**Struttura file giornaliero:** dpc-covid19-ita-province-yyyymmdd.csv (dpc-covid19-ita-province-20200224.csv)<br>
**File complessivo:** dpc-covid19-ita-province.csv<br>
**File ultimi dati (latest):** dpc-covid19-ita-province-latest.csv

| Nome campo              | Descrizione                         | Description                     | Formato            | Esempio              |
|-------------------------|-------------------------------------|---------------------------------|--------------------|----------------------|
| **data**                    | Data dell’informazione              | Date of notification            | YYYY-MM-DD HH:MM:SS (ISO 8601) Ora italiana           | 2020-03-05 12:15:45 |                   |
| **stato**                   | Stato di riferimento                | Country of reference            | ISO 3166-1 alpha-3 | ITA                  |
| **codice_regione**          | Codice della Regione (ISTAT 2019)   | Code of the Region (ISTAT 2019) | Numero             | 13                   |
| **denominazione_regione**   | Denominazione della Regione         | Name of the Region              | Testo              | Abruzzo              |
| **codice_provincia**        | Codice della Provincia (ISTAT 2019) | Code of the Province            | Numero             | 067                  |
| **denominazione_provincia** | Denominazione della provincia       | Name of the Province            | Testo              | Teramo               |
| **sigla_provincia**         | Sigla della Provincia               | Province abbreviation           | Testo              | TE                   |
| **lat**                     | Latitudine                          | Latitude                        | WGS84              | 42.6589177           |
| **long**                    | Longitudine                         | Longitude                       | WGS84              | 13.70439971          |
| **totale_casi**             | Totale casi positivi                | Total amount of positive cases  | Numero             | 3                    |

*Le Province autonome di Trento e Bolzano sono indicate in "denominazione regione" e con il codice 04 del Trentino Alto Adige.*<br>
*Ogni Regione ha una Provincia denominata "In fase di definizione/aggiornamento" con il codice provincia da 979 a 999, utile ad indicare i dati ancora non assegnati alle Province.*<br>
*Viene messo a disposizione un file JSON complessivo di tutte le date nella cartella "dati-json": dpc-covid19-ita-province.json* e rispettivo file ultimi dati (latest) dpc-covid19-ita-province-latest.json

### Andamento nazionale

**Directory:**  dati-andamento-nazionale<br>
**Struttura file giornaliero:** dpc-covid19-ita-andamento-nazionale-yyyymmdd.csv (dpc-covid19-ita-andamento-nazionale-20200224.csv)<br>
**File complessivo:** dpc-covid19-ita-andamento-nazionale.csv<br>
**File ultimi dati (latest):** dpc-covid19-ita-regioni-latest.csv


| Nome campo                  | Descrizione                       | Description                            | Formato                       | Esempio             |
|-----------------------------|-----------------------------------|----------------------------------------|-------------------------------|---------------------|
| **data**                        | Data dell’informazione            | Date of notification                   | YYYY-MM-DD HH:MM:SS (ISO 8601) Ora italiana | 2020-03-05 12:15:45 |
| **stato**                       | Stato di riferimento              | Country of reference                   | XYZ (ISO 3166-1 alpha-3)      | ITA                 |
| **ricoverati_con_sintomi**      | Ricoverati con sintomi            | Hospitalised patients with symptoms    | Numero                        | 3                   |
| **terapia_intensiva**           | Ricoverati in terapia intensiva   | Intensive Care                         | Numero                        | 3                   |
| **totale_ospedalizzati**        | Totale ospedalizzati              | Total hospitalised patients            | Numero                        | 3                   |
| **isolamento_domiciliare**      | Persone in isolamento domiciliare | Home confinement                       | Numero                        | 3                   |
| **totale_attualmente_positivi** | Totale attualmente positivi (ospedalizzati + isolamento domiciliare)      | Total amount of current positive cases (Hospitalised patients + Home confinement)  | Numero                        | 3                   |
| **nuovi_attualmente_positivi**  | Nuovi attualmente positivi (ospedalizzati + isolamento domiciliare)       | News amount of current positive cases (Hospitalised patients + Home confinement)  | Numero                        | 3                   |
| **dimessi_guariti**             | Persone dimesse guarite           | Recovered                              | Numero                        | 3                   |
| **deceduti**                    | Persone decedute                  | Death                                  | Numero                        | 3                   |
| **totale_casi**                 | Totale casi positivi              | Total amount of positive cases         | Numero                        | 3                   |
| **tamponi**                     | Totale tamponi                    | Tests performed                        | Numero                        | 3                   |
>>>>>>> 201ba01d6d948d19eb4b9fabfa1baf81f12fc23e

<b>Contact Us: </b><br>
* Email: jhusystems@gmail.com
<br><br>

<b>Terms of Use:</b><br>

<<<<<<< HEAD
This GitHub repo and its contents herein, including all data, mapping, and analysis, copyright 2020 Johns Hopkins University, all rights reserved, is provided to the public strictly for educational and academic research purposes.  The Website relies upon publicly available data from multiple sources, that do not always agree. The Johns Hopkins University hereby disclaims any and all representations and warranties with respect to the Website, including accuracy, fitness for use, and merchantability.  Reliance on the Website for medical guidance or use of the Website in commerce is strictly prohibited.
=======
*Viene messo a disposizione un file JSON complessivo di tutte le date nella cartella "dati-json": dpc-covid19-ita-andamento-nazionale.json* e rispettivo file ultimi dati (latest) dpc-covid19-ita-andamento-nazionale-latest.json
<br><br>
**Licenza:** [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/deed.en) - [Visualizza licenza](https://github.com/pcm-dpc/COVID-19/blob/master/LICENSE)
<br><br><br>
**Editore/Autore del dataset:** Dipartimento della Protezione Civile<br>
**Temi del dataset:** [Salute umana e sicurezza - Human health and safety](http://inspire.ec.europa.eu/theme/hh) (Inspire)<br>
**Categoria ISO 19115:** Salute<br>
*Dati forniti dal Ministero della Salute*<br>
*Elaborazione e gestione dati a cura del Dipartimento della Protezione Civile*
>>>>>>> 201ba01d6d948d19eb4b9fabfa1baf81f12fc23e
