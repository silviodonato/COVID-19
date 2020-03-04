import ROOT
import csv
import copy

fixSigma = 8
maxPar3 = 1E4

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

def fillData(fileName):
    data = {}
    data["Outside China"] = {}
    dates = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                dates = row[4:]
            else:
                state  = row[0]
                region = row[1]
                if len(state)>0:
                    place = state
                else:
                    place = region
                place = region
                if state=="Hubei": 
                    place = "Hubei"
#                    continue
#                if region=="Mainland China": place = state
                
                if not place in data: data[place]={}
                for i, date in enumerate(dates):
                    if not date in data[place]: data[place][date] = 0
                    data[place][date] += int(row[i+4])
                if region!="Mainland China": 
                    place = "Outside China"
                    if not place in data: data[place]={}
                    for i, date in enumerate(dates):
                        if not date in data[place]: data[place][date] = 0
                        data[place][date] += int(row[i+4])
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


def makeHistos(data, dates, selection, firstDate, lastDate, predictionDate, threshold=-1, cumulativeError=False):
    histos = {}
    for place in selection:
        histos[place] = copy.copy(ROOT.TH1F("histo"+place, place, predictionDate-firstDate, firstDate+0.5, predictionDate+0.5))
        suppress = False
        for i in reversed(range(firstDate, lastDate+1)):
            if data[place][dates[i]]>threshold and not suppress:
                histos[place].SetBinContent(histos[place].FindBin(i), data[place][dates[i]])
#            else:
#                suppress = True
        for i in range(firstDate, predictionDate):
                histos[place].GetXaxis().SetBinLabel(  histos[place].FindBin(i), dates[i])
        if cumulativeError:
            for i in range(firstDate, lastDate+1):
                histos[place].SetBinError(histos[place].FindBin(i), 1+abs(data[place][dates[lastDate]] - data[place][dates[i]])**0.5)                        
        else:
            for i in range(firstDate, lastDate+1):
                histos[place].SetBinError(histos[place].FindBin(i), 10+abs(data[place][dates[i]])**0.5)                        
        color = colors[selection.index(place)]
        histos[place].SetLineWidth(3)
        histos[place].SetLineColor(color)
    return histos

def fitErf(h, selection, firstDate, lastDate, predictionDate):
    functs = {}
    functs_res = {}
    for place in selection:
        functs[place] = copy.copy(ROOT.TF1("function"+place,"[0]*(1+TMath::Erf((x-[1])/[2])) + [3]",0,predictionDate))
        functs[place].SetParLimits(3,0,100)
        functs[place].SetParLimits(2,2,20)
        functs[place].SetParLimits(1,0,100)
        functs[place].SetParameters(6.60369e+02, 25, fixSigma, 0)
        functs[place].FixParameter(2, fixSigma)
        functs[place].FixParameter(3, 0)
#        h[place].Fit(functs[place],"0W","",0,lastDate)
        functs_res[place] = h[place].Fit(functs[place],"0S","",0,lastDate+1)
        functs[place].ReleaseParameter(3)
        functs[place].SetParLimits(3,0,maxPar3)
        functs_res[place] = h[place].Fit(functs[place],"0S","",0,lastDate+1)
        color = colors[selection.index(place)]
        functs[place].SetLineColor(color)
    return functs, functs_res

def fitGauss(h, selection, firstDate, lastDate, predictionDate):
    functs = {}
    functs_res = {}
    for place in selection:
        functs[place] = copy.copy(ROOT.TF1("function"+place,"gaus + [3]",firstDate,predictionDate))
        functs[place].SetParameters(5.61752e+00, 20, fixSigma)
        functs[place].FixParameter(2, fixSigma)
        functs[place].FixParameter(3, 0)
        print h[place]
        print functs[place]
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        functs[place].ReleaseParameter(3)
        functs[place].SetParLimits(3,0,maxPar3)
        functs_res[place] = h[place].Fit(functs[place],"0SE","",firstDate,lastDate)
        color = colors[selection.index(place)]
        functs[place].SetLineColor(color)
    return functs, functs_res

def extendDates(dates, nextend):
    ndates = len(dates)
    for i in range(1,nextend):
    #    dates.append(dates[ndates-1]+"+"+str(i))
        newDate = "3/%d/20"%i
        if not newDate in dates: dates.append(newDate)
    return dates

def saveCSV(prediction, dates, fn_prediction, fn_prediction_error):
    f_prediction_error = open(fn_prediction_error,"w")
    f_prediction       = open(fn_prediction,"w")
    f_prediction.write( "place" )
    f_prediction_error.write( "place" )
    for date in dates:
        if date in prediction[prediction.keys()[0]]:
            f_prediction.write( ",%s"%date )
            f_prediction_error.write( ",%s"%date )
    f_prediction.write( "\n" )
    f_prediction_error.write( "\n" )
    for place in prediction:
        f_prediction.write( place )
        f_prediction_error.write( place )
        for date in dates:
            if date in prediction[place]:
                (pred, pred_err) = prediction[place][date]
                f_prediction.write( ",%.1f +/- %.1f"%(pred,pred_err) )
                f_prediction_error.write( ",%.1f"%pred_err )
        f_prediction.write( "\n" )
        f_prediction_error.write( "\n" )
    f_prediction_error.close()
    f_prediction.close()
                

def savePlot(histoConfirmed, histoRecovered, histoDeaths, function, fName, canvas):
    canvas.SetLogy()
    canvas.cd()
    canvas.SetTitle("")
    function.SetMinimum(1)
    function.SetLineColor(ROOT.kBlue)
    histoRecovered.SetLineStyle(1)
    histoDeaths.SetLineStyle(1)
    histoConfirmed.SetLineColor(ROOT.kBlue)
    histoRecovered.SetLineColor(ROOT.kRed)
    histoDeaths.SetLineColor(ROOT.kBlack)
    histoConfirmed.SetMinimum(1)
    histoConfirmed.SetMaximum(max(100, function.GetMaximum(), histoRecovered.GetMaximum(), histoConfirmed.GetMaximum(), histoDeaths.GetMaximum())*1.5)
    histoConfirmed.Draw()
    function.Draw("same")
    histoRecovered.Draw("same")
    histoDeaths.Draw("same")
    canvas.SaveAs(fName)
    print fName
