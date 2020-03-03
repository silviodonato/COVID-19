#import csv
#import copy

from tools import colors, fillData, newCases, getRatio, makeHistos, fitErf,fitGauss, extendDates, saveCSV

import ROOT
ROOT.gStyle.SetOptStat(0)




#file_ = ROOT.TFile("data.root", "RECREATE")




confirmes, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

if "Hubei" in confirmes:
    for i in range(22):
        confirmes["Hubei"][dates[i]] = confirmes["Hubei"][dates[i]]*1.4

deaths, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')

recoveres, dates = fillData('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')


################

firstDate = 16
lastDate = len(dates)-1
#predictionDate = lastDate+30
predictionDate = 68

#firstDate = 10
#lastDate = 35
#predictionDate = 35

################

dates = extendDates(dates, 31)
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

selection = []
for place in confirmes.keys():
    if place == "Others": continue
    if confirmes[place][dates[lastDate]]>50:
        selection.append(place)

#selection = ["Italy","South Korea","Japan","Iran","Hubei"]
#selection = ["Italy"]
#selection = ["Italy","Japan","South Korea"]
#selection = ["Guangdong","Henan","Zhejiang","Hunan","Anhui","Jiangxi","Italy"]
#selection = ["Zhejiang"]

selection = [p[1] for p in sorted([(confirmes[p][dates[lastDate]], p) for p in selection], reverse=True)]

print "selection:",selection

################

fits   = {}
fits2   = {}
fitdiffs   = {}

c1 = ROOT.TCanvas()


positives_h = makeHistos(positives,        dates, selection, firstDate, lastDate, predictionDate, 20)
confirmes_h = makeHistos(confirmes,        dates, selection, firstDate, lastDate, predictionDate, 20)
recoveres_h = makeHistos(recoveres,        dates, selection, firstDate, lastDate, predictionDate, 20)
deaths_h    = makeHistos(deaths,           dates, selection, firstDate, lastDate, predictionDate, 20)
#histos = makeHistos(confirmes, selection, firstDate, lastDate, predictionDate)
newConfirmes_h  = makeHistos(newConfirmes, dates, selection, firstDate, lastDate, predictionDate, 5)
newRecoveres_h  = makeHistos(newRecoveres, dates, selection, firstDate, lastDate, predictionDate, 5)
newDeaths_h     = makeHistos(newDeaths,    dates, selection, firstDate, lastDate, predictionDate, 5)
#newPositives_h  = makeHistos(newPositives, dates, selection, firstDate, lastDate, predictionDate)

fits,     fits_res     = fitErf(confirmes_h, selection, firstDate, lastDate, predictionDate)
fitdiffs, fitdiffs_res = fitGauss(newConfirmes_h, selection, firstDate, lastDate, predictionDate)





#for place in selection:
#    fits2[place] = copy.copy(ROOT.TF1("function"+place,"[0]*(1+TMath::Erf((x-[1])/[2])) + [3]",0,predictionDate))
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
for place in selection:
    leg.AddEntry(confirmes_h[place], place, "lep")

for place in selection:
    confirmes_h[place].SetMinimum(1)
    confirmes_h[place].SetBinError(confirmes_h[place].FindBin(lastDate-0.5),1E-9)
    leg.AddEntry(confirmes_h[place], place, "lep")
    confirmes_h[place].Draw("HIST,C,same")
    recoveres_h[place].SetLineStyle(2)
    recoveres_h[place].Draw("HIST,C,same")
    deaths_h[place].SetLineStyle(3)
    deaths_h[place].Draw("HIST,C,same")
    fits[place].Draw("same")

leg.Draw()
c1.SetGridx()
c1.SetGridy()
c1.SetLogy()
c1.Update()

c2 = ROOT.TCanvas()

#diffs["Italy"].Draw()

#for place in ['Japan','Italy','Spain','France','South Korea']:
for place in selection:
    newConfirmes_h[place].SetMinimum(1)
    newConfirmes_h[place].Draw("same")
    fitdiffs[place].Draw("same")



leg.Draw()
c2.SetGridx()
c2.SetGridy()
c2.SetLogy()
c2.Update()

##########################################

c3 = ROOT.TCanvas()

histo_sigma1 = ROOT.TH1F("histo_sigma1","",100,0,100)
histo_sigma2 = ROOT.TH1F("histo_sigma2","",100,0,100)

for place in selection:
    histo_sigma1.Fill(abs(fits[place].GetParameter(2)))
    histo_sigma2.Fill(abs(fitdiffs[place].GetParameter(2)))

histo_sigma1.Draw()
histo_sigma2.Draw("same")

leg.Draw()
c3.SetGridx()
c3.SetGridy()
c3.SetLogy()
c3.Update()

########################################

##########################################


c4 = ROOT.TCanvas()

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

########################################

#print confirmes
#print confirmes["Italy"]["2/2/20"]

#file_.Write()
#file_.Close()


print "############"
print "PREDICTION From %s to %s"%(dates[lastDate], dates[predictionDate])
print "############"

for place in selection:
    print "#### ",place," ####"
    print "Confirmed (%s): %d"%(dates[lastDate], confirmes_h[place].GetBinContent(confirmes_h[place].FindBin(lastDate)))
    val = confirmes_h[place].GetBinContent(confirmes_h[place].FindBin(lastDate))
    print "Expected fit total (%s): %f"%(dates[predictionDate], val + (fits[place].Eval(predictionDate)-fits[place].Eval(lastDate)))
    integr = fitdiffs[place].Integral(lastDate + 0.5, predictionDate + 0.5)
    interr = fitdiffs[place].IntegralError(lastDate + 0.5, predictionDate + 0.5, fitdiffs_res[place].GetParams(), fitdiffs_res[place].GetCovarianceMatrix().GetMatrixArray())
    print "Expected fit new cases (%s): %f +/- %f"%(dates[predictionDate],  val + integr, interr)
#    for d in range(lastDate,predictionDate):
#        val = val + fitdiffs[place].Eval(d+1)
#    print "Expected fit new cases (%s): %f"%(dates[predictionDate],  val)
    try:
        print "Real Confirmed (%s): %d"%(dates[predictionDate], confirmes[place][dates[predictionDate]])
        print "Error (sigma) : %f"%( (confirmes[place][dates[predictionDate]] - (val + integr)) / interr)
    except:
        pass

prediction = {}
#for place in ["Italy"]:
for place in selection:
    prediction[place] = {}
    for predictionDate in range(lastDate,lastDate+29):
        val = confirmes_h[place].GetBinContent(confirmes_h[place].FindBin(lastDate))
        integr = fitdiffs[place].Integral(lastDate + 0.5, predictionDate + 0.5)
        interr = fitdiffs[place].IntegralError(lastDate + 0.5, predictionDate + 0.5, fitdiffs_res[place].GetParams(), fitdiffs_res[place].GetCovarianceMatrix().GetMatrixArray())
        if interr>1: 
            interr = (interr**2 + integr)**0.5 # Err = (Syst^2 + Stat(ie sqrtN)^2)^0.5
        else:
            interr = (interr**2 + integr)**0.5 # Err = (Syst^2 + Stat(ie sqrtN)^2)^0.5
            print "WARNING interr=%f"%interr
        print "Expected fit new cases (%s): %.1f +/- %.1f"%(dates[predictionDate],  val + integr, interr)
        prediction[place][dates[predictionDate]] = (val + integr, interr)
        try:
            print "Real Confirmed (%s): %d"%(dates[predictionDate], confirmes[place][dates[predictionDate]])
            print "Error (sigma) : %.1f"%( (confirmes[place][dates[predictionDate]] - (val + integr)) / interr)
        except:
            pass

saveCSV(prediction, dates, "prediction.csv", "prediction_error.csv")

'''



TFitResultPtr r = graph->Fit(myFunction,"S");

double x[1] = { x0 };
double err[1];  // error on the function at point x0

r->GetConfidenceIntervals(1, 1, 1, x, err, 0.683, false);
cout << " function value at " << x[0] << " = " << myFunction->Eval(x[0]) << " +/- " << err[0] << endl;
'''
