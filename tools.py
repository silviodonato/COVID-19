import ROOT
import csv
import copy
import array

fixSigma = 8
#maxPar3 = 1E4
maxPar3 = 1
#minPar2,maxPar2 = 7.9, 8.1
#minPar2,maxPar2 = 7, 9
#minPar2,maxPar2 = 8, 8
#minPar2,maxPar2 = 7.5, 8.5
#minPar2,maxPar2 = 7, 9
#minPar2,maxPar2 = 8, 8
#minPar2,maxPar2 = 3, 20
minPar2,maxPar2 = 5.5, 7.5
#minPar2,maxPar2 = 5, 11
#minPar2,maxPar2 = 6.5-3, 6.5+3

colors = [
ROOT.kBlack,

ROOT.kYellow+1,
ROOT.kRed,
ROOT.kMagenta,
ROOT.kBlue,
ROOT.kCyan+1,
ROOT.kGreen+1,

ROOT.kOrange,
ROOT.kPink,
ROOT.kViolet,
ROOT.kAzure,
ROOT.kTeal,
ROOT.kSpring,

ROOT.kGray,
] 

colors = colors *10

maps = {
"America" : ["US","Canada","Ecuador"],
"Africa" : ["Algeria"],
"Europe" : ["Austria", "Belarus", "Belgium", "Croatia", "Czech Republic", "Denmark", "Finland", "France", "Germany", "Greece", "Iceland", "Ireland", "Italy", "Netherlands", "Norway", "Spain", "Sweden", "Switzerland", "UK", "Romania", "San Marino", "Portugal"],
"MiddleEast" : ["Azerbaijan", "Bahrain", "Iran", "Iraq", "Israel", "Kuwait", "Lebanon", "Qatar", "Oman", "United Arab Emirates",],
"FarEast" : ["Hong Kong", "Japan", "Malaysia", "Macau", "Singapore", "South Korea", "Taiwan", "India", "Thailand", "Vietnam",],
}

def getData(row, i):
    try:
        value = int(row[i+4])
    except:
        print "WARNING: problems with '%s' '%s' at %i. The numeber is '%s'. I wil use 0."%(row[0],row[1],i+4,row[i+4])
        value = 0
    state = row[0]
    country = row[1]
    if "Hubei" == state:
        if i < 22:
            value = value*1.2
#        if i < 30:
#            value = value*1.1
    elif "Shandong" == state:
        if i < 30:
            value = value*1.35
    return value

def regions(state, country):
    state = state.replace(",","")
    country = country.replace(",","")
    regions = set(["World"])
    if state: regions.add(state)
    if country: regions.add(country)
    for zone in maps: 
        if country in maps[zone]: 
            regions.add(zone)
            if zone=="Europe" and country!="Italy": regions.add("Rest of Europe")
    if country=="Mainland China" and state!="Hubei": regions.add("Rest of China")
    if country!="Mainland China": regions.add("Rest of World")
    print (state, country, regions)
    return regions
    
def fillData(fileName):
    data = {}
    dates = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dates = row[4:]
            else:
                for place in regions(row[0], row[1]):
                    if not place in data: data[place]={}
                    for i, date in enumerate(dates):
                        if not date in data[place]: data[place][date] = 0
                        data[place][date] += getData(row, i)
            line_count += 1
    return data, dates

def newCases(cases, dates):
    newCases = {}
    for place in cases:
        newCases[place] = {}
        newCases[place][dates[0]] = 0
        for i in range(1, len(cases[place])):
            newCases[place][dates[i]] = cases[place][dates[i]] - cases[place][dates[i-1]]
    return newCases

def getRatio(numerators, denominators):
    ratios = {}
    for place in numerators:
        ratios[place] = numerators[place].Clone("ratio"+place)
        ratios[place].Divide(numerators[place],denominators[place])
    return ratios


def makeHistos(data, dates, places, firstDate, lastDate, predictionDate, threshold=-1, cutTails=False, errorType=None, lineWidth=3):
    histos = {}
    for place in places:
        histos[place] = copy.copy(ROOT.TH1F("histo"+place, place, predictionDate-firstDate+1, firstDate-0.5, predictionDate+0.5))
	assert(histos[place].GetXaxis().GetBinWidth(1)==1.0)
	stop = False
	start = False
        for i in reversed(range(firstDate, predictionDate)):
            binx = histos[place].FindBin(i)
            date = dates[i]
#            print(binx,date)
            histos[place].GetXaxis().SetBinLabel(  binx, date )
            error = 0.
            if date in data.values()[0]:
                if errorType=='dictionary': ## if dictionary, data is (value, error)
                    value = data[place][date][0]
                    error = data[place][date][1]
                else:
                    value = data[place][date]
                    if errorType=='cumulative':
                        error = 1.+(data[place][dates[lastDate]] - data[place][date])**0.5    if (data[place][dates[lastDate]] - data[place][date]) >=0 else 0
                    else:
                        error = 10.+(data[place][date])**0.5 if data[place][date]>0 else abs(data[place][date])*2                   
                if value>threshold:
		    if not stop:
		            histos[place].SetBinContent(binx, value)
		            histos[place].SetBinError(binx, error)
			    start = True
        if cutTails: ### remove tail, if there are 2 days without new cases from the peak
                maxBin = histos[place].GetMaximumBin()
                for i in range(maxBin, predictionDate):
                        if histos[place].GetBinContent(i-1)==0 and histos[place].GetBinContent(i-2)==0: 
                                histos[place].SetBinContent(i, 0)
                                histos[place].SetBinError(i, 0)
                for i in reversed(range(firstDate, maxBin)):
                        if histos[place].GetBinContent(i+1)==0 and histos[place].GetBinContent(i+2)==0: 
                                histos[place].SetBinContent(i, 0)
                                histos[place].SetBinError(i, 0)

        color = colors[places.index(place)]
        histos[place].SetLineWidth(lineWidth)
        histos[place].SetLineColor(color)
    return histos

def fitErf(h, places, firstDate, lastDate, predictionDate):
    functs = {}
    functs_res = {}
    for place in places:
        functs[place] = copy.copy(ROOT.TF1("function"+place,"[0]*(1+TMath::Erf((x-[1])/[2])) + [3]",0,predictionDate))
        functs[place].SetParLimits(3,0,100)
        functs[place].SetParLimits(2,2,20)
        functs[place].SetParLimits(1,0,100)
        functs[place].SetParameters(6.60369e+02, 25, fixSigma, 0)
        functs[place].FixParameter(2, fixSigma)
        functs[place].FixParameter(3, 0)
#        h[place].Fit(functs[place],"0W","",0,lastDate)
        functs_res[place] = h[place].Fit(functs[place],"0S","",0,lastDate+0.5)
        functs[place].ReleaseParameter(3)
        functs[place].SetParLimits(3,0,maxPar3)
        functs_res[place] = h[place].Fit(functs[place],"0S","",0,lastDate+0.5)
        if minPar2 != maxPar2:
            functs[place].ReleaseParameter(2)
            functs[place].SetParLimits(2,minPar2,maxPar2)
        functs_res[place] = h[place].Fit(functs[place],"0S","",0,lastDate+0.5)
        color = colors[places.index(place)]
        functs[place].SetLineColor(color)
    return functs, functs_res

def fitGauss(h, places, firstDate, lastDate, predictionDate):
    functs = {}
    functs_res = {}
    functs_err = {}
    for place in places:
        print "### Fit %s ###"%place
        functs[place] = copy.copy(ROOT.TF1("function"+place,"gaus + [3]",firstDate,predictionDate))
        functs[place].SetParameters(h[place].Integral(), h[place].GetMean(), fixSigma)
        functs[place].FixParameter(2, fixSigma)
        functs[place].FixParameter(3, 0)
#        print h[place]
#        print functs[place]
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        functs[place].ReleaseParameter(3)
        functs[place].SetParLimits(3,0,maxPar3)
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        if minPar2 != maxPar2:
            functs[place].ReleaseParameter(2)
            functs[place].SetParLimits(2,minPar2,maxPar2)
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        color = colors[places.index(place)]
        functs[place].SetLineColor(color)
        functs_err[place] = copy.copy(h[place].Clone(("err"+h[place].GetName())))
        functs_err[place].Reset()
        ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(functs_err[place], 0.68)
        functs_err[place].SetStats(ROOT.kFALSE)
        functs_err[place].SetLineColor(color)
        functs_err[place].SetFillColor(color)
    return functs, functs_res, functs_err


def extendDates(dates, nextend):
    ndates = len(dates)
    for i in range(1,nextend):
    #    dates.append(dates[ndates-1]+"+"+str(i))
        if i<=31:
            newDate = "3/%d/20"%i
        else:
            newDate = "4/%d/20"%(i-31)
        if not newDate in dates: dates.append(newDate)
    return dates

def saveCSV(predictions, places, dates, fn_predictions, fn_predictions_error):
    f_predictions_error = open(fn_predictions_error,"w")
    f_predictions       = open(fn_predictions,"w")
    f_predictions.write( "place" )
    f_predictions_error.write( "place" )
    for date in dates:
        if date in predictions[predictions.keys()[0]]:
            f_predictions.write( ",%s"%date )
            f_predictions_error.write( ",%s"%date )
    f_predictions.write( "\n" )
    f_predictions_error.write( "\n" )
    for place in places:
        f_predictions.write( place )
        f_predictions_error.write( place )
        for date in dates:
            if date in predictions[place]:
                (pred, pred_err) = predictions[place][date]
                f_predictions.write( ",%.1f +/- %.1f"%(pred,pred_err) )
                f_predictions_error.write( ",%.1f"%pred_err )
        f_predictions.write( "\n" )
        f_predictions_error.write( "\n" )
    f_predictions_error.close()
    f_predictions.close()
                

def savePlot(histoConfirmed, histoRecovered, histoDeaths, histoPrediction, function, function_res, function_error, fName, xpred, canvas):
    if function: 
        fres = function_res.Get()
    canvas.SetLogy()
    canvas.cd()
    canvas.SetTitle("")
    leg = ROOT.TLegend(0.9,0.1,1.0,0.9)
    maxim = 0
    for item in [histoConfirmed, histoRecovered, histoDeaths, histoPrediction, function]:
        if item: 
            maxim = max(maxim, item.GetMaximum())
            if item == histoConfirmed: leg.AddEntry(item, "Confirmed", "lep")
            if item == histoRecovered: leg.AddEntry(item, "Recovered", "lep")
            if item == histoDeaths: leg.AddEntry(item, "Deaths", "lep")
            if item == histoPrediction: leg.AddEntry(item, "Prediction", "lep")
            if item == function and fres: leg.AddEntry(item, "#splitline{Gaussian fit}{#splitline{#mu=%.1f #pm %.1f}{ #sigma=%.1f #pm %.1f}} "%(fres.GetParams()[1],fres.GetErrors()[1],fres.GetParams()[2],fres.GetErrors()[2]), "lep")
    if function: maxim = min(maxim, histoConfirmed.GetMaximum()*100)
    if maxim>0:
        maxim = 10**int(ROOT.TMath.Log10(maxim)+1)
    histoRecovered.SetLineStyle(1)
    histoDeaths.SetLineStyle(1)
    histoConfirmed.SetLineColor(ROOT.kBlue)
    histoRecovered.SetLineColor(ROOT.kRed)
    histoDeaths.SetLineColor(ROOT.kBlack)
    histoConfirmed.SetMinimum(1)
    histoConfirmed.SetMaximum(maxim)
    histoConfirmed.Draw()
    line = ROOT.TLine(xpred+0.5,0,xpred+0.5,histoConfirmed.GetMaximum())
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    if function:
        function.SetMinimum(1)
        function.SetLineColor(ROOT.kBlue)
#        ci = copy.copy(histoConfirmed.Clone("ci"+histoConfirmed.GetName()))
#        function_res.Get().GetConfidenceIntervals(ci, 0.68)
#        ci.SetStats(kFALSE);
#        ci.SetFillColor(2);
#        ci.Draw("e3 same");
        function.Draw("same")
    if function_error:
        function_error.SetFillColor(ROOT.kBlue)
        function_error.SetFillStyle(3144)
        function_error.SetLineColor(ROOT.kBlue)
        function_error.Draw("e3same")
    histoRecovered.Draw("same")
    histoDeaths.Draw("same")
    leg.Draw("same")
    if histoPrediction: 
        histoPrediction.SetLineColor(ROOT.kGreen+2)
        histoPrediction.SetLineStyle(1)
        histoPrediction.Draw("same")
        histoConfirmed.Draw("same")
    line.Draw()
    canvas.SaveAs(fName)
    print fName

def getPrediction(places, dates, firstDate, finalDate, histo, functNewCases, functNewCases_res, realData=None):
    predictions = {}
    for place in places:
        print "### Prediction %s ###"%(place)
        predictions[place] = {}
        for predictionDate in range(firstDate, finalDate):
            val = histo[place].GetBinContent(histo[place].FindBin(firstDate))
            integr = functNewCases[place].Integral(firstDate + 0.5, predictionDate + 0.5)
            interr = functNewCases[place].IntegralError(firstDate + 0.5, predictionDate + 0.5, functNewCases_res[place].GetParams(), functNewCases_res[place].GetCovarianceMatrix().GetMatrixArray()) if functNewCases_res[place].Get() else 1E9
            if interr>1: 
                interr = (interr**2 + integr)**0.5 # Err = (Syst^2 + Stat(ie sqrtN)^2)^0.5
            else:
                interr = (interr**2 + integr)**0.5 # Err = (Syst^2 + Stat(ie sqrtN)^2)^0.5
                print "WARNING interr=%f"%interr
            print "Expected fit new cases (%s): %.1f +/- %.1f"%(dates[predictionDate],  val + integr, interr)
            predictions[place][dates[predictionDate]] = (val + integr, interr) if float(interr)/(1.+val+integr)<0.5 else (0,0)
#            predictions[place][dates[predictionDate]] = (val + integr, interr)
            try:
                print "Real Confirmed (%s): %d"%(dates[predictionDate], realData[place][dates[predictionDate]])
                print "Error (sigma) : %.1f"%( (realData[place][dates[predictionDate]] - (val + integr)) / interr)
            except:
                pass
    return predictions

def getPredictionErf(places, dates, firstDate, finalDate, histo, functErfs, functErfs_res, realData=None):
    predictions = {}
    for place in places:
        print "### Prediction (from Erf)%s ###"%(place)
        predictions[place] = {}
        valErf0 = functErfs[place].Eval( firstDate  )
        for predictionDate in range(firstDate, finalDate):
            valErf = functErfs[place].Eval( predictionDate  )
            err = array.array('d',[0])
            x   = array.array('d',[predictionDate ])
            functErfs_res[place].GetConfidenceIntervals(2, 1, 1, x, err, 0.683)
            err = (err[0]**2 + abs(valErf-valErf0))**0.5 ## add statistical error
            print "Expected fit erf (%s): %.1f +/- %.1f"%(dates[predictionDate], valErf, err)
            predictions[place][dates[predictionDate]] = (valErf, err)
            try:
                print "Real Confirmed (%s): %d"%(dates[predictionDate], realData[place][dates[predictionDate]])
                print "Error (sigma) : %.1f"%( (realData[place][dates[predictionDate]] - (val + integr)) / interr)
            except:
                pass
    return predictions
