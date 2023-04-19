'''
to reload:
import importlib
importlib.reload(ToolsCollection) 
'''

import ROOT as r

def cut_th1d(hist,start_bin,last_bin,hist_name="histo_cut"):
    """
    written for root 6.24
    6.26 also work ?
    
    start_bin = 1
    last_bin = hist.GetNbinsX()
    
    cut the original th1d with selected range
    th1d is defined as N, xlow, xup, with:
        index 0 is underflow
        index 1 as the index of its first bin
        index N is the last bin
        index N+1 is the overflow
    
    xlow is the lower limit, which is also the low edge of the first (1) bin
    xup  is the upper limit, which is also the up edge of the last (N) bin, also the low edge of the overflow (n+1) bin
    """

    bin_width = hist.GetBinWidth(1)
    nbins_ori = hist.GetNbinsX()
    nbins_new = last_bin - start_bin + 1
    xlow_new = (start_bin - 1) * bin_width
    xup_new =  last_bin * bin_width
    
    title_new = "{};{};{}".format(hist.GetTitle(),hist.GetXaxis().GetTitle(),hist.GetYaxis().GetTitle())
    hist_cut = r.TH1D(hist_name, title_new, nbins_new, xlow_new, xup_new)

    print("original: nbsins, xlow, xup, xwidth: ",nbins_ori,hist.GetBinLowEdge(1),hist.GetBinLowEdge(nbins_ori+1),hist.GetBinWidth(1))
    print("cut: nbins, xlow, xup, xwidth : ",nbins_new,hist_cut.GetBinLowEdge(1),hist_cut.GetBinLowEdge(nbins_new+1),hist.GetBinWidth(1))

    hist_cut.SetMarkerStyle(hist.GetMarkerStyle())
    hist_cut.SetMarkerSize(hist.GetMarkerSize())
    hist_cut.SetMarkerColor(hist.GetMarkerColor())
    hist_cut.SetLineStyle(hist.GetLineStyle())
    hist_cut.SetLineColor(hist.GetLineColor())
    hist_cut.SetLineWidth(hist.GetLineWidth())

    for i in range(last_bin+1)[start_bin:]:
        # debug with h1 = r.TH1D("h1","h1;x;y",10,0,20)
#         print("{}-th bin of the original histo, {}-th bin of the new histo".format(i,i-start_bin+1))
#         print(hist.GetBinCenter(i),hist_cut.GetBinCenter(i-start_bin+1)) 

        val = hist.GetBinContent(i)
        err = hist.GetBinError(i)

        hist_cut.SetBinContent(i-start_bin+1, val)
        hist_cut.SetBinError(i-start_bin+1, err)
    
    return hist_cut



def fft(hist,fftname="default_fft_name",given_title="FFT",fstart=0.01):
    bin_width = hist.GetBinWidth(1)
    print(bin_width)
    
    title = "{} ;f [MHz]; FFT Magnitude [arb.]".format(given_title)
    
    fft_hist = r.TH1D(fftname, title, hist.GetNbinsX(), 0, 1.0/bin_width)
    hist.FFT(fft_hist, "MAG")
    fft_hist.GetXaxis().SetRangeUser(fstart,fft_hist.GetXaxis().GetXmax()/2) # 0.08 to get rid of the DC component
    return fft_hist



def fft2(hist,fftname="default_fft_name",given_title="FFT",fstart=0.01,fft_option="MAG"):
    """
    from ROOT: https://root.cern.ch/doc/master/classTH1.html#a69321e3106e4a26db3fef4d126d835ff
    option on what to return
    "RE" - returns a histogram of the real part of the output
    "IM" - returns a histogram of the imaginary part of the output
    "MAG"- returns a histogram of the magnitude of the output
    "PH" - returns a histogram of the phase of the output

    option of transform type
    "R2C" - real to complex transforms - default
    "R2HC" - real to halfcomplex (special format of storing output data, results the same as for R2C)
    "DHT" - discrete Hartley transform real to real transforms (sine and cosine):
    "R2R_0", "R2R_1", "R2R_2", "R2R_3" - discrete cosine transforms of types I-IV
    "R2R_4", "R2R_5", "R2R_6", "R2R_7" - discrete sine transforms of types I-IV To specify the type of each dimension of a 2-dimensional real to real transform, use options of form "R2R_XX", for example, "R2R_02" for a transform, which is of type "R2R_0" in 1st dimension and "R2R_2" in the 2nd.
    """
    bin_width = hist.GetBinWidth(1)
    print(bin_width)
    
    if(fft_option=="MAG"):yaxis_label = "Magnitude [arb.]"
    elif(fft_option=="RE"):yaxis_label = "Real component [arb.]"
    elif(fft_option=="IM"):yaxis_label = "Imaginary component [arb.]"
    elif(fft_option=="PH"):yaxis_label = "Phase [rad]"
    else:
        print("invalid option, using Magnitude instead")
        yaxis_label = "Magnitude [arb.]"

    title = "{} ;f [MHz]; FFT {}".format(given_title,yaxis_label)
    
    fft_hist = r.TH1D(fftname, title, hist.GetNbinsX(), 0, 1.0/bin_width)
    hist.FFT(fft_hist, fft_option)
    fft_hist.GetXaxis().SetRangeUser(fstart,fft_hist.GetXaxis().GetXmax()/2) # 0.08 to get rid of the DC component
    return fft_hist


def identify_hist_peaks(hist,addToHist=False,setting=(3,1,2,0.1)):
    """
    note: this can only be used during drawing of the hist
    """
    peak_finder = r.TSpectrum(setting[0],setting[1])
    peak_finder.Search(hist,setting[2],"",setting[3])
    pm = hist.FindObject("TPolyMarker");
    
    if(addToHist):
        hist.GetListOfFunctions().Add(pm.Clone())
    pm.Draw()

    for pk in range(pm.GetN()):
        text = r.TLatex(pm.GetX()[pk]*1.05,pm.GetY()[pk]*0.9,"{:.02f} MHz".format(pm.GetX()[pk]));
        text.SetTextColor(2)
        text.SetTextSize(0.04)
        text.DrawClone();
        if(addToHist):
            hist.GetListOfFunctions().Add(text)


def identify_hist_peaks2(hist,setting=(3,1,2,0.1),draw=False,addToHist=False,decimal_places=2,unit="MHz",color=2,markerstyle=23,textsize=0.04):
    """
    new feature test
    note: this can only be used during drawing of the hist
    Tspectrum find peak only scan the peak in the set range of the histogram
    """
    peak_finder = r.TSpectrum(setting[0],setting[1])
    npeaks = peak_finder.Search(hist,setting[2],"",setting[3])
    print("found {} peaks".format(npeaks))
    pm = hist.FindObject("TPolyMarker");
    pm.SetMarkerColor(color)
    pm.SetMarkerStyle(markerstyle)

    if(addToHist):
        hist.GetListOfFunctions().Add(pm.Clone())
    if(draw):
        pm.Draw() 
     # caveat: if not draw, the TPoly will resides in the ListOfFunction of that histo.
     #         if draw, the TPoly need to be attached to the ListOfFunction, in order to be drawn

    for pk in range(pm.GetN()):
        text = r.TLatex(pm.GetX()[pk]*1.05,pm.GetY()[pk]*0.9,"{:.0{}f} {}".format(pm.GetX()[pk],decimal_places,unit));
        text.SetTextColor(color)
        text.SetTextSize(textsize)
        if(draw):
            text.DrawClone();
        if(addToHist):
            hist.GetListOfFunctions().Add(text)


def identify_hist_peaks3(hist, maxpositions=3, resolution = 1.0, sigma = 2.0, option = "", threshold = 0.1, draw=False, addToHist=False, decimal_places=2, unit="MHz", color=2, markerstyle=23, textsize=0.04):
    """
    this gives full control. ROOT version still buggy ! in ../test.h, ../test.ipynb
    note: this can only be used during drawing of the hist
    Tspectrum find peak only scan the peak in the set range of the histogram
    """
    peak_finder = r.TSpectrum(maxpositions, resolution)
    npeaks = peak_finder.Search(hist,sigma, option, threshold)
    print("found {} peaks".format(npeaks))
    pm = hist.FindObject("TPolyMarker");
    pm.SetMarkerColor(color)
    pm.SetMarkerStyle(markerstyle)

    if(addToHist):
        hist.GetListOfFunctions().Add(pm.Clone())
    if(draw):
        pm.Draw() 
     # caveat: if not draw, the TPoly will resides in the ListOfFunction of that histo.
     #         if draw, the TPoly need to be attached to the ListOfFunction, in order to be drawn

    for pk in range(pm.GetN()):
        text = r.TLatex(pm.GetX()[pk]*1.05,pm.GetY()[pk]*0.9,"{:.0{}f} {}".format(pm.GetX()[pk],decimal_places,unit));
        text.SetTextColor(color)
        text.SetTextSize(textsize)
        if(draw):
            text.DrawClone();
        if(addToHist):
            hist.GetListOfFunctions().Add(text)