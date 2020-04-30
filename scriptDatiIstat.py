#import csv
#import copy
from tools import colors, fillDataISTATpickle, selectComuniDatesAgeGender, newCases, getRatio, makeHistos, fitDecessi, fitErf, fitGauss, fitExp, extendDates, saveCSV, savePlotNew, getPrediction, getPredictionErf, getColumn
from operator import itemgetter, attrgetter

useLog = True

import ROOT
#ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
#ROOT.gROOT.SetBatch(0)

resX, resY = 1920, 1080

dataISTAT, dates = fillDataISTATpickle('DatiISTAT/dati-giornalieri-comune/comune_giorno.csv', zerosuppression=100, pickleFileName = "temp_italia.pkl", writePickle = False)

decessi     = selectComuniDatesAgeGender(dataISTAT, dates[:], places=None, ages=range(0,30), genders=[0,1])
decessi_old = selectComuniDatesAgeGender(dataISTAT, dates[:], places=None, ages=range(0,30), genders=[2,3])

places = decessi.keys()

firstDate = 0
#lastDate = len(dates)-1
lastDate = dates.index("03/08/20")
#lastDate = dates.index("03/11/20")
predictionsDate = dates.index("04/30/20")
#predictionsDate = dates.index("03/08/20")
startDate = lastDate

decessi_h = makeHistos("histo_decessi", decessi,        dates[:], places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='sqrtN', lineWidth=2)
decessi_old_h = makeHistos("histo_storico", decessi_old,dates[:], places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='sqrtN', lineWidth=2)

fits, fits_res, fits_error              = fitExp(decessi_h,      places, firstDate, lastDate, predictionsDate, maxConstExp=10000)
fitGausss, fitGausss_res, fitGausss_error              = fitGauss(decessi_h,      places, firstDate, dates.index("04/04/20"), predictionsDate, maxPar3=10000)

d3 = ROOT.TCanvas("d1","",resX,resY)
leg = ROOT.TLegend(0.9,0.1,1.0,0.9)
leg.Draw()
d3.SetGridx()
d3.SetGridy()

fits_sigOnly={}
funct_const = ROOT.TF1("funct_const","[0]",firstDate,predictionsDate)
firstDeaths = {}

for place in places:
    fits[place].fitResult = fits_res[place]
    if fits[place].fitResult.Get():
        fit_val = fits[place].fitResult.GetParams()[1]
        fit_err = fits[place].fitResult.GetErrors()[1]
        if fit_val>0 and fit_val<lastDate and fit_err<3.5:
            firstDeaths[place] = (fit_val,  fit_err)


goodFits = []
firstDeath_f = open("firstDeath.csv","w")
firstDeathsInv = {v: k for k, v in firstDeaths.iteritems()}
firstDeath_f.write("%s,%s,%s\n"%("place","days since 1/1/2020", "date"))
for x in sorted(firstDeathsInv.keys()):
    print "%.2f +/- %.2f (%s)\t%s"%(x[0], x[1], dates[int(x[0]+0.5)], str(firstDeathsInv[x]))
    goodFits.append(str(firstDeathsInv[x]))
    firstDeath_f.write("%s,%.2f +/- %.2f,%s\n"%(str(firstDeathsInv[x]),x[0], x[1], dates[int(x[0]+0.5)] ))

firstDeath_f.close()

for place in places:
#for place in goodFits:
    decessi_h[place].SetLineColor(ROOT.kBlack)
    decessi_old_h[place].SetLineColor(ROOT.kMagenta+1)
    decessi_h[place].GetYaxis().SetTitle("Number of deaths / day")
#    decessi_h[place].SetMinimum(0.1)
    decessi_h[place].SetMaximum(2*decessi_h[place].GetMaximum())
    if decessi_old_h[place].Integral(0, dates.index("02/15/20"))>0: decessi_old_h[place].Scale(decessi_h[place].Integral(0, dates.index("02/15/20"))/decessi_old_h[place].Integral(0, dates.index("02/15/20")))
    decessi_excess_only_h = decessi_h[place].Clone(decessi_h[place].GetName()+"_excess")
    decessi_excess_only_h.Add(decessi_old_h[place],-1)
    fits[place].error = fits_error[place]
    fits[place].fitResult = fits_res[place]
    fits_sigOnly[place] = fits[place].Clone(fits[place].GetName()+"_sig")
    funct_const.SetParameter(0 , fits_sigOnly[place].GetParameter(2))
    fits_sigOnly[place].SetParameter(2, 0 )
    fits_sigOnly[place].error = fits_error[place].Clone(fits_error[place].GetName()+"_sig")
    fits_sigOnly[place].error.Add(funct_const, -1)
    fits[place].SetLineColor(ROOT.kBlue)
    fits_sigOnly[place].SetLineColor(ROOT.kRed)
    fits[place].label="Fit totale"
    fits_sigOnly[place].label="Fit solo eccesso"
    fitGausss[place].SetLineColor(ROOT.kBlack)
    fitGausss[place].error = fitGausss_error[place]
    fitGausss[place].fitResult = fitGausss_res[place]
    fitGausss[place].label="Fit Gaus"
    funct_const.label="Fit costante"
    funct_const.SetLineColor(ROOT.kGreen+2)
    funct_const.SetLineStyle(2)
    funct_const.error = None
    savePlotNew([decessi_h[place],decessi_old_h[place],decessi_excess_only_h], [fits[place], fits_sigOnly[place],funct_const, fitGausss[place]], "plotsISTAT/%s.png"%place, startDate, d3, True)



