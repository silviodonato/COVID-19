#import csv
#import copy
from tools import colors, fillData, newCases, getRatio, makeHistos, fitErf, fitGauss, fitExp, extendDates, saveCSV, savePlot, getPrediction, getPredictionErf

import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
#ROOT.gROOT.SetBatch(0)

resX, resY = 1920, 1080

#file_ = ROOT.TFile("data.root", "RECREATE")




confirmes, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

deaths, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')

recoveres, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

lastDateData = len(dates)-1
dates = extendDates(dates, 61)
################

firstDate = 0
#firstDate = dates.index("2/18/20")
#firstDate = 16
lastDate = lastDateData
#lastDate = dates.index("2/29/20")
#lastDate = dates.index("3/1/20")
#lastDate = 30
predictionsDate = dates.index("4/15/20")
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

###########################

places = []
for place in confirmes.keys():
    if place == "Others": continue
    if confirmes[place][dates[lastDate]]>50:
        places.append(place)

#places = ["Italy","South Korea","Japan","Iran","Hubei"]
#places = ["Italy"]
#places = ["Rest of Europe"]
#places = ["Italy","Japan","South Korea"]
#places = ["Guangdong","Henan","Zhejiang","Hunan","Anhui","Jiangxi","Italy"]
#places = ["Zhejiang"]
#places = ["Jiangxi"]
#places = ["Belgium"]


places = [p[1] for p in sorted([(confirmes[p][dates[lastDate]], p) for p in places], reverse=True)]

print "places:",places

################

fits   = {}
fits2   = {}
fitdiffs   = {}

c1 = ROOT.TCanvas("c1","",resX,resY)


positives_h = makeHistos(positives,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
confirmes_h = makeHistos(confirmes,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
recoveres_h = makeHistos(recoveres,        dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
deaths_h    = makeHistos(deaths,           dates, places, firstDate, lastDate, predictionsDate, 0, cutTails=False, errorType='cumulative', lineWidth=2)
#histos = makeHistos(confirmes, places, firstDate, lastDate, predictionsDate, cumulativeError=True)
newConfirmes_h  = makeHistos(newConfirmes, dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=True, lineWidth=2)
newRecoveres_h  = makeHistos(newRecoveres, dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
newDeaths_h     = makeHistos(newDeaths,    dates, places, firstDate, lastDate, predictionsDate, 1, cutTails=False, lineWidth=2)
#newPositives_h  = makeHistos(newPositives, dates, places, firstDate, lastDate, predictionsDate)

fits, fits_res, fits_error              = fitErf(confirmes_h, places, firstDate, lastDate, predictionsDate)
fitdiffs, fitdiffs_res, fitdiffs_error  = fitGauss(newConfirmes_h, places, firstDate, lastDate, predictionsDate)
fitexps, fitexps_res, fitexps_error     = fitExp(newConfirmes_h, places, firstDate, lastDate, predictionsDate)
fitexptotals, fitexptotals_res, fitexptotals_error = fitExp(confirmes_h, places, firstDate, lastDate, predictionsDate)



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
c1.SetGridx()
c1.SetGridy()
c1.SetLogy()
c1.Update()
c1.SaveAs("c1.png")

c2 = ROOT.TCanvas("c1","",resX,resY)

#diffs["Italy"].Draw()

#for place in ['Japan','Italy','Spain','France','South Korea']:
for place in places:
    newConfirmes_h[place].GetYaxis().SetTitle("Number of cases / day")
    newConfirmes_h[place].SetMinimum(1)
    newConfirmes_h[place].Draw("same")
    fitdiffs[place].Draw("same")



leg.Draw()
c2.SetGridx()
c2.SetGridy()
c2.SetLogy()
c2.Update()
c2.SaveAs("c2.png")

##########################################

c3 = ROOT.TCanvas("c1","",resX,resY)

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
c3.SetGridx()
c3.SetGridy()
c3.SetLogy()
c3.Update()
c3.SaveAs("c3.png")

#input()
########################################

##########################################

'''
c4 = ROOT.TCanvas("c1","",resX,resY)

#ratios = getRatio(newDeaths_h, newRecoveres_h)
ratios = getRatio(deaths_h, recoveres_h)
#ratios = getRatio(deaths_h, confirmes_h)
#ratios = getRatio(recoveres_h, confirmes_h)

for place in ratios:
    ratios[place].SetMaximum(1)
    ratios[place].SetMinimum(0)
    ratios[place].Draw("HIST,C,same")

leg.Draw()
c4.SetGridx()
c4.SetGridy()
c4.SetLogy(0)
c4.Update()
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
startDate = lastDate
predictions = getPrediction(places, dates, startDate, endDate, confirmes_h, fitdiffs, fitdiffs_res, confirmes)
#predictions = getPredictionErf(places, dates, startDate, endDate, confirmes_h, fits, fits_res, confirmes)

#predictionHistos = makeHistos(predictions, dates, startDate, endDate, predictionsDate, 0, errorType='dictionary')
predictions_h = makeHistos(predictions, dates, places, startDate, None, endDate, threshold=0, cutTails=False, errorType='dictionary', lineWidth=3)


saveCSV(predictions, places, dates, "prediction.csv", "prediction_error.csv")


c5 = ROOT.TCanvas("c5","",resX,resY)

#ratios = getRatio(newDeaths_h, newRecoveres_h)
ratios = getRatio(deaths_h, recoveres_h)
#ratios = getRatio(deaths_h, confirmes_h)
#ratios = getRatio(recoveres_h, confirmes_h)

for place in ratios:
    ratios[place].SetMaximum(1)
    ratios[place].SetMinimum(0)
    ratios[place].Draw("HIST,C,same")

leg.Draw()
c5.SetGridx()
c5.SetGridy()
c5.SetLogy(0)
c5.Update()

for place in places:
#    savePlot(confirmes_h[place], recoveres_h[place], deaths_h[place], predictions_h[place], fits[place], fits_res[place], fits_error[place], fitexptotals[place], "plots/%s.png"%place, lastDate, c5)
    savePlot(confirmes_h[place], recoveres_h[place], deaths_h[place], predictions_h[place], None, None, None, fitexptotals[place], "plots/%s.png"%place, lastDate, c3)
    savePlot(newConfirmes_h[place], newRecoveres_h[place], newDeaths_h[place], None, fitdiffs[place], fitdiffs_res[place], fitdiffs_error[place], fitexps[place], "plots/%s_newCases.png"%place, lastDate, c5)

'''



TFitResultPtr r = graph->Fit(myFunction,"S");

double x[1] = { x0 };
double err[1];  // error on the function at point x0

r->GetConfidenceIntervals(1, 1, 1, x, err, 0.683, false);
cout << " function value at " << x[0] << " = " << myFunction->Eval(x[0]) << " +/- " << err[0] << endl;
'''
