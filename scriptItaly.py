#import csv
#import copy
from tools import colors, fillDataRegioni, fillDataISTATpickle, newCases, getRatio, makeHistos, fitErf, fitGauss, fitGaussAsymmetric, fitExp, extendDates, saveCSV, savePlotNew, getPrediction, getPredictionErf, getColumn, selectComuniDatesAgeGender, makeCompatible, fitLinear

doProvince = False
useLog = True
useDatiISTAT = True

import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
#ROOT.gROOT.SetBatch(0)

resX, resY = 1920, 1080

#file_ = ROOT.TFile("data.root", "RECREATE")

if useDatiISTAT: 
    dataISTAT, datesISTAT = fillDataISTATpickle('DatiISTAT/dati-giornalieri-comune/comune_giorno.csv', zerosuppression=100, pickleFileName = "temp_italia.pkl", writePickle = False)
    dataISTAT = makeCompatible(dataISTAT, firstDateDay=24, firstDateMonth=2)

dataRegioni, dates = fillDataRegioni('dati-regioni/dpc-covid19-ita-regioni.csv')
if (doProvince): dataProvince, dates = fillDataRegioni('dati-province/dpc-covid19-ita-province.csv', "denominazione_provincia")

#data,stato,codice_regione,denominazione_regione,lat,long,ricoverati_con_sintomi,terapia_intensiva,totale_ospedalizzati,isolamento_domiciliare,totale_attualmente_positivi,nuovi_attualmente_positivi,dimessi_guariti,deceduti,totale_casi,tamponi

tests = getColumn(dataRegioni, "tamponi")
intensivas = getColumn(dataRegioni, "terapia_intensiva")
ricoveratis = getColumn(dataRegioni, "ricoverati_con_sintomi")
confirmes = getColumn(dataRegioni, "totale_casi")
deaths = getColumn(dataRegioni, "deceduti")
recoveres = getColumn(dataRegioni, "dimessi_guariti")
if (doProvince): confirmesProv = getColumn(dataProvince, "totale_casi")

if useDatiISTAT: 
#    datesISTAT = dataISTAT.values()[0].keys()
    newDeathIstats     = selectComuniDatesAgeGender(dataISTAT, dates, places=None, ages=range(0,30), genders=[0,1])
    newDeathIstats_old = selectComuniDatesAgeGender(dataISTAT, dates, places=None, ages=range(0,30), genders=[2,3])

lastDateData = len(dates)-1
dates = extendDates(dates, 140)
################

firstDate = 0
#firstDate = dates.index("2/18/20")
#firstDate = 16
lastDate = lastDateData - 1
#lastDate = dates.index("2/29/20")
#lastDate = dates.index("3/1/20")
#lastDate = 30
predictionsDate = dates.index("6/30/20")
#predictionsDate = 95


#firstDate = 10
#lastDate = 35
#predictionsDate = 35

################

#confirmes = deaths

positives = {}
for place in confirmes:
    positives[place] = {}
    for i in range(0, len(confirmes[place])):
        positives[place][dates[i]] = confirmes[place][dates[i]] - deaths[place][dates[i]] - recoveres[place][dates[i]]


newConfirmes = newCases(confirmes, dates)
newDeaths = newCases(deaths, dates)
newRecoveres = newCases(recoveres, dates)
newTests = newCases(tests, dates)
newIntensivas = newCases(intensivas, dates)
newRicoveratis = newCases(ricoveratis, dates)

if (doProvince): newConfirmesProv = newCases(confirmesProv, dates)

###########################

places = []
for place in confirmes.keys():
    if place == "Others": continue
    if confirmes[place][dates[lastDate]]>50:
        places.append(place)

if (doProvince): 
    province = []
    for place in confirmesProv.keys():
        if place == "Others": continue
        if confirmesProv[place][dates[lastDate]]>50:
            province.append(place)

places = [p[1] for p in sorted([(confirmes[p][dates[lastDate]], p) for p in places], reverse=True)]

if (doProvince): province = [p[1] for p in sorted([(confirmesProv[p][dates[lastDate]], p) for p in province], reverse=True)]

#places = ["Italia"]
#province = ["La Spezia", "Pisa", "Genova", "Milano", "Brescia", "Bergamo"]
#province = ["Pisa"]
#places = ["Lombardia"]

print "places:",places

################

fits   = {}
fits2   = {}
fitdiffs   = {}

d1 = ROOT.TCanvas("d1","",resX,resY)


positives_h = makeHistos("histo_positives", positives,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
confirmes_h = makeHistos("histo_confirmes", confirmes,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
recoveres_h = makeHistos("histo_recoveres", recoveres,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
deaths_h    = makeHistos("histo_deaths", deaths,           dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
tests_h    = makeHistos("histo_tests", tests,           dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
ricoveratis_h    = makeHistos("histo_ricoveratis", ricoveratis,           dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
intensivas_h    = makeHistos("histo_intensivas", intensivas,           dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)

#histos = makeHistos(confirmes, places, firstDate, lastDate, predictionsDate, cumulativeError=True)
newConfirmes_h  = makeHistos("histo_newConfirmes", newConfirmes, dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=True, lineWidth=2)
newRecoveres_h  = makeHistos("histo_newRecoveres", newRecoveres, dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
newDeaths_h     = makeHistos("histo_newDeaths", newDeaths,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
newTests_h     = makeHistos("histo_newTests", newTests,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
newRicoveratis_h = makeHistos("histo_newRicoveratis", newRicoveratis,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
newIntensivas_h     = makeHistos("histo_newIntensivas", newIntensivas,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
#newPositives_h  = makeHistos("histo_newpositives", newPositives, dates, places, firstDate, lastDate, predictionsDate)

fits, fits_res, fits_error              = fitErf(confirmes_h,      places, firstDate, lastDate, predictionsDate)
fitdiffs, fitdiffs_res, fitdiffs_error  = fitGaussAsymmetric(newConfirmes_h, places, firstDate, lastDate, predictionsDate)
fitexps, fitexps_res, fitexps_error                = fitExp(newConfirmes_h, places, lastDate-8, lastDate, predictionsDate,)
fitexptotals, fitexptotals_res, fitexptotals_error = fitExp(confirmes_h,    places, lastDate-8, lastDate, predictionsDate)
fitexptotals, fitexptotals_res, fitexptotals_error = fitExp(confirmes_h,      places, lastDate-8, lastDate, predictionsDate)
fitdiffDeaths, fitdiffDeaths_res, fitdiffDeaths_error = fitGaussAsymmetric(newDeaths_h, places, firstDate, lastDate, predictionsDate)
fitdiffRecoveres, fitdiffRecoveres_res, fitdiffRecoveres_error = fitGaussAsymmetric(newRecoveres_h, places, firstDate, lastDate, predictionsDate)

if useDatiISTAT: 
    newDeathIstats_h        = makeHistos("histo_ISTAT",     newDeathIstats,        dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2, errorType='sqrtN')
    newDeathIstats_old_h    = makeHistos("histo_ISTAT_old", newDeathIstats_old,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2, errorType='sqrtN')
    newDeathIstatExcess_h = {}
    for place in newDeathIstats_old_h:
        if newDeathIstats_old_h[place].Integral(0, dates.index("2/28/20"))>0: newDeathIstats_old_h[place].Scale(newDeathIstats_h[place].Integral(0, dates.index("2/28/20"))/newDeathIstats_old_h[place].Integral(0, dates.index("2/28/20")))
        feb29_bin = dates.index("3/1/20")
        newDeathIstats_old_h[place].SetBinContent(feb29_bin, newDeathIstats_old_h[place].GetBinContent(feb29_bin-1))
        newDeathIstats_old_h[place].SetBinError(  feb29_bin, newDeathIstats_old_h[place].GetBinContent(feb29_bin-1))
    fitLinears, fitLinears_res, fitLinears_error              = fitLinear(newDeathIstats_old_h,      newDeathIstats_old_h.keys(), firstDate+1, dates.index("4/4/20"), predictionsDate, maxConstExp=10000, tail=True, fitOption="SEQ0L")
    for place in newDeathIstats_old_h:
        newDeathIstatExcess_h[place] = newDeathIstats_h[place].Clone(newDeathIstats_h[place].GetName()+"Excess")
        newDeathIstatExcess_h[place].Add(fitLinears[place],-1)

#1/0

if (doProvince): 
    confirmesProv_h = makeHistos("histo_confirmes", confirmesProv,        dates, province, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
    newConfirmesProv_h  = makeHistos("histo_newConfirmes", newConfirmesProv, dates, province, firstDate, lastDate, predictionsDate, 1, cutTails=True, lineWidth=2)


#for place in places:
#    fits2[place] = copy.copy(ROOT.TF1("function"+place,"[0]*(1+TMath::Erf((x-[1])/[2])) + [3]",0,predictionsDate))
#    mea = fitdiffs[place].GetParameter(1)
#    sig = abs(fitdiffs[place].GetParameter(2))
#    print "mean, sigma 0 = ", mea, sig
#    fits2[place].SetParameters(confirmes[place][dates[lastDate]], mea, sig)
#    histos[place].Fit(fits2[place],"0","",mea - 2*sig,lastDate)
#    for i in range(10):
#        mea = fits2[place].GetParameter(1)
#        sig = abs(fits2[place].GetParameter(2))
#        print "mean, sigma %i = ", mea, sig
#        histos[place].Fit(fits2[place],"0","",mea - 2*sig ,lastDate)
#    histos[place].Fit(fits2[place],"0","",mea - 2*sig,lastDate)
#    color = colors[confirmes.keys().index(place)]
#    fits2[place].SetLineColor(color)

#histos["Italy"].Draw()

#for place in confirmes.keys():
leg = ROOT.TLegend(0.9,0.1,1.0,0.9)

for place in places:
    confirmes_h[place].GetYaxis().SetTitle("Number of cases")
    confirmes_h[place].SetMinimum(1)
#    confirmes_h[place].SetBinError(confirmes_h[place].FindBin(lastDate-0.5),1E-9)
    leg.AddEntry(confirmes_h[place], place, "lep")
    confirmes_h[place].Draw("ERR,same")
    recoveres_h[place].SetLineStyle(2)
#    recoveres_h[place].Draw("ERR,same")
    deaths_h[place].SetLineStyle(3)
#    deaths_h[place].Draw("ERR,same")
#    fits[place].Draw("same")

leg.Draw()
d1.SetGridx()
d1.SetGridy()
d1.SetLogy(useLog)
d1.Update()

d1.SaveAs("d1.png")


leg = ROOT.TLegend(0.9,0.1,1.0,0.9)

if (doProvince): 
    confirmesProv_h.values()[0].Draw("ERR")
    for place in province:
        confirmesProv_h[place].GetYaxis().SetTitle("Number of cases")
        confirmesProv_h[place].SetMinimum(1)
    #    confirmes_h[place].SetBinError(confirmes_h[place].FindBin(lastDate-0.5),1E-9)
        leg.AddEntry(confirmesProv_h[place], place, "lep")
        confirmesProv_h[place].Draw("ERR,same")
    #    recoveresProv_h[place].SetLineStyle(2)
    #    recoveresProv_h[place].Draw("ERR,same")
    #    deathsProv_h[place].SetLineStyle(3)
    #    deathsProv_h[place].Draw("ERR,same")
    #    fits[place].Draw("same")

    d1.SaveAs("d1_prov.png")

d2 = ROOT.TCanvas("d2","",resX,resY)

#diffs["Italy"].Draw()

#for place in ['Japan','Italy','Spain','France','South Korea']:
for place in places:
    newConfirmes_h[place].GetYaxis().SetTitle("Number of cases / day")
    newConfirmes_h[place].SetMinimum(1)
    newConfirmes_h[place].Draw("same")
    fitdiffs[place].Draw("same")



leg.Draw()
d2.SetGridx()
d2.SetGridy()
d2.SetLogy(useLog)
d2.Update()
d2.SaveAs("d2.png")

if (doProvince): 
    d2 = ROOT.TCanvas("d2_prov","",resX,resY)


    leg = ROOT.TLegend(0.9,0.1,1.0,0.9)

    newConfirmesProv_h.values()[0].Draw("ERR")

    #for place in ['Japan','Italy','Spain','France','South Korea']:
    for place in province:
        newConfirmesProv_h[place].GetYaxis().SetTitle("Number of cases / day")
        newConfirmesProv_h[place].SetMinimum(1)
        newConfirmesProv_h[place].Draw("same")


    leg.Draw()
    d2.SetGridx()
    d2.SetGridy()
    d2.SetLogy(useLog)
    d2.Update()
    d2.SaveAs("d2_prov.png")

##########################################

d3 = ROOT.TCanvas("d1","",resX,resY)
leg = ROOT.TLegend(0.9,0.1,1.0,0.9)

histo_sigma1 = ROOT.TH1F("histo_sigma1","",100,0,30)
histo_sigma2 = ROOT.TH1F("histo_sigma2","",100,0,30)

for place in places:
    histo_sigma1.Fill(abs(fitdiffs[place].GetParameter(2)))
#    histo_sigma2.Fill(abs(fits[place].GetParameter(2)))

histo_sigma1.Draw()
histo_sigma2.Draw("same")
histo_sigma1.Fit("gaus")
print "Mean=",histo_sigma1.GetMean()
print "RMS=",histo_sigma1.GetRMS()

leg.Draw()
d3.SetGridx()
d3.SetGridy()
d3.SetLogy(useLog)
d3.Update()
d3.SaveAs("d3.png")

#input()
########################################

##########################################

'''
d4 = ROOT.TCanvas("d1","",resX,resY)

#ratios = getRatio(newDeaths_h, newRecoveres_h)
ratios = getRatio(deaths_h, recoveres_h)
#ratios = getRatio(deaths_h, confirmes_h)
#ratios = getRatio(recoveres_h, confirmes_h)

for place in ratios:
    ratios[place].SetMaximum(1)
    ratios[place].SetMinimum(0)
    ratios[place].Draw("HIST,C,same")

leg.Draw()
d4.SetGridx()
d4.SetGridy()
d4.SetLogy(0)
d4.Update()
'''

########################################

#print confirmes
#print confirmes["Italy"]["2/2/20"]

#file_.Write()
#file_.Close()

'''
print "############"
print "PREDICTION From %s to %s"%(dates[lastDate], dates[predictionsDate])
print "############"


for place in places:
    print "#### ",place," ####"
    print "Confirmed (%s): %d"%(dates[lastDate], confirmes_h[place].GetBinContent(confirmes_h[place].FindBin(lastDate)))
    val = confirmes_h[place].GetBinContent(confirmes_h[place].FindBin(lastDate))
    print "Expected fit total (%s): %f"%(dates[predictionsDate], val + (fits[place].Eval(predictionsDate)-fits[place].Eval(lastDate)))
    integr = fitdiffs[place].Integral(lastDate + 0.5, predictionsDate + 0.5)
    interr = fitdiffs[place].IntegralError(lastDate + 0.5, predictionsDate + 0.5, fitdiffs_res[place].GetParams(), fitdiffs_res[place].GetCovarianceMatrix().GetMatrixArray())
    print "Expected fit new cases (%s): %f +/- %f"%(dates[predictionsDate],  val + integr, interr)
#    for d in range(lastDate,predictionsDate):
#        val = val + fitdiffs[place].Eval(d+1)
#    print "Expected fit new cases (%s): %f"%(dates[predictionsDate],  val)
    try:
        print "Real Confirmed (%s): %d"%(dates[predictionsDate], confirmes[place][dates[predictionsDate]])
        print "Error (sigma) : %f"%( (confirmes[place][dates[predictionsDate]] - (val + integr)) / interr)
    except:
        pass
'''

endDate = predictionsDate
startDate = lastDate + 1
predictions = getPrediction(places, dates, startDate, endDate, confirmes_h, fitdiffs, fitdiffs_res, confirmes)
#predictions = getPredictionErf(places, dates, startDate, endDate, confirmes_h, fits, fits_res, confirmes)

#predictionHistos = makeHistos(predictions, dates, startDate, endDate, predictionsDate, 0, errorType='dictionary')
predictions_h = makeHistos("histo_prediction", predictions, dates, places, startDate, None, endDate, threshold=0, cutTails=False, errorType='dictionary', lineWidth=3)

predictionDeaths = getPrediction(places, dates, startDate, endDate, deaths_h, fitdiffDeaths, fitdiffDeaths_res, deaths)
predictionDeaths_h = makeHistos("histo_predictionDeaths",    predictionDeaths, dates, places, startDate, None, endDate, threshold=0, cutTails=False, errorType='dictionary', lineWidth=3)

predictionRecoveres = getPrediction(places, dates, startDate, endDate, recoveres_h, fitdiffRecoveres, fitdiffRecoveres_res, recoveres)
predictionRecoveres_h = makeHistos("histo_predictionRecoveres",    predictionRecoveres, dates, places, startDate, None, endDate, threshold=0, cutTails=False, errorType='dictionary', lineWidth=3)


saveCSV(predictions, places, dates, "predictionRegioni.csv", "predictionRegioni_error.csv")
saveCSV(predictionDeaths, places, dates, "predictionRegioniMorti.csv", "predictionRegioniMorti_error.csv")
saveCSV(predictionRecoveres, places, dates, "predictionRegioniGuariti.csv", "predictionRegioniGuariti_error.csv")


d5 = ROOT.TCanvas("d5","",resX,resY)

#ratios = getRatio(newDeaths_h, newRecoveres_h)
ratios = getRatio(deaths_h, recoveres_h)
#ratios = getRatio(deaths_h, confirmes_h)
#ratios = getRatio(recoveres_h, confirmes_h)

for place in ratios:
    ratios[place].SetMaximum(1)
    ratios[place].SetMinimum(0)
    ratios[place].Draw("HIST,C,same")

leg.Draw()
d5.SetGridx()
d5.SetGridy()
d5.SetLogy(useLog)
d5.Update()

for place in places:
#    savePlot(confirmes_h[place], recoveres_h[place], deaths_h[place], predictions_h[place], fits[place], fits_res[place], fits_error[place], fitexptotals[place], "plots/%s.png"%place, lastDate, d5)
    fitexptotals[place].error = fitexptotals_error[place]
    fitexptotals[place].fitResult = fitexptotals_res[place]
    fitdiffs[place].error = fitdiffs_error[place]
    fitdiffs[place].fitResult = fitdiffs_res[place]
    fitdiffDeaths[place].error = fitdiffDeaths_error[place]
    fitdiffDeaths[place].fitResult = fitdiffDeaths_res[place]
    fitdiffRecoveres[place].error = fitdiffRecoveres_error[place]
    fitdiffRecoveres[place].fitResult = fitdiffRecoveres_res[place]
    fitexps[place].error = None
    fitexps[place].fitResult = None
    if not place in fitLinears: fitLinears[place] = None
    else:
        fitLinears[place].error = fitLinears_error[place]
        fitLinears[place].res = fitLinears_res[place]
    if not place in newDeathIstatExcess_h: newDeathIstatExcess_h[place] = None
    savePlotNew([confirmes_h[place], recoveres_h[place], deaths_h[place], predictions_h[place], predictionDeaths_h[place], predictionRecoveres_h[place], intensivas_h[place], ricoveratis_h[place], tests_h[place]], [fitexptotals[place]], "plotsRegioni/%s.png"%place, startDate, d3)
    savePlotNew([newConfirmes_h[place], newRecoveres_h[place], newDeaths_h[place], newDeathIstatExcess_h[place], newIntensivas_h[place], newRicoveratis_h[place], newTests_h[place]], [fitdiffs[place], fitdiffRecoveres[place], fitdiffDeaths[place], fitexps[place]], "plotsRegioni/%s_newCases.png"%place, startDate, d3)
#    savePlotNew([newDeathIstats_old_h[place]], [fitLinears[place]], "plotsRegioni/%s_newCases.png"%place, startDate, d3)

if (doProvince): 
    for place in province:
    #    savePlot(confirmesProv_h[place], confirmesProv_h[place], confirmesProv_h[place], None, None, None, None, None, None, None, None, "plotsProvince/%s.png"%place, lastDate, d3)
    #    savePlot(newConfirmesProv_h[place], newConfirmesProv_h[place], newConfirmesProv_h[place], None, None, None, None, None, None, None, None, "plotsProvince/%s_newCases.png"%place, lastDate, d3)
        savePlotNew([confirmesProv_h[place]], [], "plotsProvince/%s.png"%place, startDate, d3)
        savePlotNew([newConfirmesProv_h[place]], [], "plotsProvince/%s_newCases.png"%place, startDate, d3)


ROOT.gROOT.SetBatch(0)

'''



TFitResultPtr r = graph->Fit(myFunction,"S");

double x[1] = { x0 };
double err[1];  // error on the function at point x0

r->GetConfidenceIntervals(1, 1, 1, x, err, 0.683, false);
cout << " function value at " << x[0] << " = " << myFunction->Eval(x[0]) << " +/- " << err[0] << endl;
'''
