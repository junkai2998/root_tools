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
    this gives full control.
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




def DrawSinglePlotsOnDividedCanvas(arrofPlots,
              Nplots=24,cvarr=(6,4),cvsize=(4800,3200),cvname="c",
              plotrangeX=None,plotrangeY=None,drawOpt="",
              additional_codes=None,Draw=True):
    """
    this only draw the plot, with ranges and additional styling provided by the additional_codes
    also, now the code is aiming at simple plotting, so it is better if the plots are similar (or already formatted), or you have to pass additional_codes to do the formatting
        
    if you want to draw something additional such as legend, you better do it outside of the function call, like:
    
    '''arrofPlots = res_21apr.GetNvsTime
    c = Draw24calos(arrofPlots,plotrange=None,Draw=True,cvname="c",cvsize=(3600,2400),cvarr=(6,4),additional_codes=None)

    c.cd()
    lgd = r.TLegend()
    lgd.AddEntry(res_21apr.GetNvsTime[0],"t1","l")
    lgd.AddEntry(res_21apr.GetNvsTime[1],"t2","l")
    lgd.Draw()
    c.Draw()
    '''
    """
    c = r.TCanvas(cvname,cvname,*cvsize)
    c.Divide(*cvarr)

    for i in range(Nplots):
        c.cd(i+1)
        plot = arrofPlots[i]
        if (plotrangeX):
            plot.GetXaxis().SetRangeUser(*plotrangeX)
        if (plotrangeY):
            plot.GetYaxis().SetRangeUser(*plotrangeY)
        if (additional_codes):
            exec(additional_codes)
        plot.Draw(drawOpt)
    
    if (Draw):
        c.Draw()
    
    return c





def DrawDoublePlotsOnDividedCanvas(arrofPlots1,arrofPlots2,
                Nplots=24,cvarr=(6,4),cvsize=(4800,3200),cvname="c",
                plotrangeX=None,plotrangeY=None,drawOpt1="",drawOpt2="",
                additional_codes=None,Draw=True):
    """
    # codes to reproduce the original plots
    # c = r.TCanvas("c","c",3600,2400)
    # c.Divide(6,4)

    # for calonum in range(24):
    #     c.cd(calonum+1)
    #     raw_fft = res_21apr.Get_fft_raw[calonum]
    #     fit_residual_fft = res_21apr.Get_fft_res[calonum]

    #     raw_fft.GetYaxis().SetMaxDigits(3)
    #     # raw_fft.GetYaxis().SetRangeUser(0,2e5)
    #     raw_fft.GetYaxis().SetRangeUser(0, 1.05*raw_fft.GetBinContent(raw_fft.GetMaximumBin())) # GetMaximum dont work if you change the axis limits

    #     raw_fft.SetLineColorAlpha(2,0.3)
    #     raw_fft.Draw()
    #     fit_residual_fft.Draw("same")
    # c.Draw()
    """
    c = r.TCanvas(cvname,cvname,*cvsize)
    c.Divide(*cvarr)

    for i in range(Nplots):
        c.cd(i+1)
        plot1 = arrofPlots1[i]
        plot2 = arrofPlots2[i]

        if (plotrangeX):
            plot1.GetXaxis().SetRangeUser(*plotrangeX)

        if (plotrangeY):
            plot1.GetYaxis().SetRangeUser(*plotrangeY)
            
        if (additional_codes):
            exec(additional_codes)

        plot1.Draw(drawOpt1)
        plot2.Draw("same" + drawOpt2)

    if (Draw):
        c.Draw()
    
    return c


def DrawMultiplePlotsOnDividedCanvas(Plots,
                Nplots=6,cvarr=(3,2),cvsize=(2400,1600),cvname="c",
                plotrangeX=None,plotrangeY=None,drawOpt="",
                additional_codes=None,Draw=True):
    
    """
    # Plots = [[divided],[], plotsOnSameAxes]
    # [[a1,a2,a3],[b1,b2,b3],[c1,c2,c3],[d1,d2,d3]]
    # a,b,c,d are Nplots different variables; 1,2,3 are different dataset
    """
    c = r.TCanvas(cvname,cvname,*cvsize)
    c.Divide(*cvarr)

    for i in range(Nplots):
        c.cd(i+1)
        arrofPlots = Plots[i]
        plot1 = arrofPlots[0]

        if (plotrangeX):
            plot1.GetXaxis().SetRangeUser(*plotrangeX)

        if (plotrangeY):
            plot1.GetYaxis().SetRangeUser(*plotrangeY)
            
        if (additional_codes):
            exec(additional_codes)

        plot1.Draw("AP"+ drawOpt)        
        for plot in arrofPlots[1:]:
            plot.Draw("same P" + drawOpt)

    if (Draw):
        c.Draw()
    
    return c


def DrawMultiplePlotsOnDividedCanvas2(Plots,
                Nplots=6,cvarr=(3,2),cvsize=(2400,1600),cvname="c",
                plotrangeX=None,plotrangeY=None,drawOpt="",
                additional_codes=None,Draw=True):
    """
    # Plots = [[plotsOnSameAxes],[], divided]
    # [[a1,b1,c1,d1],[a2,b2,c2,d2],[a3,b3,c3,d3]]
    # a,b,c,d are Nplots different variables; 1,2,3 are Ndata different dataset
    """
    c = r.TCanvas(cvname,cvname,*cvsize)
    c.Divide(*cvarr)
    
    Ndata = len(Plots)

    for i in range(Nplots):
        c.cd(i+1)
        plot1 = Plots[0][i]

        if (plotrangeX):
            plot1.GetXaxis().SetRangeUser(*plotrangeX)

        if (plotrangeY):
            plot1.GetYaxis().SetRangeUser(*plotrangeY)
            
        if (additional_codes):
            exec(additional_codes)

        plot1.Draw("AP"+ drawOpt)        
        for j in range(1,Ndata):
            plotj = plot1 = Plots[j][i]
            plotj.Draw("same P" + drawOpt)

    if (Draw):
        c.Draw()
    
    return c


def TransposePyArray(arr):
    Ni = len(arr)
    Nj = len(arr[0])

    lengtsOfSubs = [len(sub_arr) for sub_arr in arr]
    # lengtsOfSubs

    IsAllSameLength = True # assume they are the same 
    for i in range(len(lengtsOfSubs)-1):
        IsAllSameLength = IsAllSameLength  & (lengtsOfSubs[i]==lengtsOfSubs[i+1])
    assert(IsAllSameLength)

    ArrNew = []
    for j in range(Nj):
        SubArrNew = []
        for i in range(Ni):
            SubArrNew.append(arr[i][j])
        ArrNew.append(SubArrNew)

    return ArrNew


def plot_diff(gr_sims,gr_data_fit,legends = ("gm2ringsim","Data Fit"),diff_ranges = (-11,11),legend_pos = (0.1, 0.77, 0.4, 0.90)):
    parname = gr_data_fit.GetTitle().split(" ")[0]
    # legends = ("gm2ringsim","Data Fit")
    # gr_sims = N0_vs_calo_gm2ringsim
    # gr_data_fit = N0_vs_calo
    # legend_pos = (0.1, 0.77, 0.4, 0.90)
    # diff_ranges = (-11,11)

    '''
    make sure you give appropriate title to the 'gr_data_fit', it will be the title of the plot
    
    make sure you have your parameter name in the title of the 'gr_data_fit'
    put in front, separated by a space.
    but as it will be the small plot's title and get obstructed by the another plot, so it is ok
    
    note: this does not take care of the error propagation
    '''


    gr_rel_diff = r.TGraphErrors()
    title = '{} difference ({} - {}) for Run {}'.format(parname,legends[0],legends[1],ds_name)
    gr_rel_diff.SetTitle(title)
    gr_rel_diff.SetMarkerStyle(23)
    gr_rel_diff.SetMarkerColor(4)
    gr_rel_diff.GetXaxis().SetTitle('Calo Number')
    gr_rel_diff.GetYaxis().SetTitle('relative difference [%]')

    for calo_num in range(24):
        data_fit_val = gr_data_fit.GetPointY(calo_num)
        sims_val = gr_sims.GetPointY(calo_num)

        diff_abs = sims_val - data_fit_val
        diff_rel = diff_abs/data_fit_val*100 # percent

        gr_rel_diff.SetPoint(gr_rel_diff.GetN(),calo_num+1,diff_rel)


    r.gStyle.SetTitleX(0.2)
    r.gStyle.SetTitleW(0.6)
    r.gStyle.SetTitleH(0.06)
    c = r.TCanvas("c","c",800,600) 

    # draw the bottom first
    p2 = r.TPad("p2", "", 0, 0, 1, 0.275);
    # p2.SetFillColor(3)
    p2.SetGrid(1,0);
    p2.Draw();
    p2.cd();
    p2.SetBottomMargin(0.2)
    p2.GetListOfPrimitives().Add(gr_rel_diff)
    gr_rel_diff.Draw('APE')
    gr_rel_diff.GetXaxis().SetRangeUser(0,24.5)
    gr_rel_diff.GetXaxis().SetLabelSize(0.1);
    gr_rel_diff.GetXaxis().SetTitleSize(0.1);
    # title = '#frac{{{0} - {1}}}{{{1}}}  [%]'.format(legends[0],legends[1])
    gr_rel_diff.GetYaxis().SetTitle('#frac{Sim - Fit}{Fit}  [%]   ')
    gr_rel_diff.GetYaxis().SetRangeUser(*diff_ranges)
    gr_rel_diff.GetYaxis().SetLabelSize(0.08);
    gr_rel_diff.GetYaxis().SetTitleSize(0.08);
    gr_rel_diff.GetYaxis().SetTitleOffset(0.4)
    gr_rel_diff.GetYaxis().SetMaxDigits(2)
    # r.gStyle.SetOptTitle(1)
    


    # N0_rel_diff.SetTitle(0)
    line = r.TLine(0,0,24.5,0) # x1, y1, x2, y2
    line.SetLineStyle(9)
    line.SetLineWidth(2)
    line.SetLineColor(1)
    line.Draw()
    gr_rel_diff.GetListOfFunctions().Add(line)


    c.cd() # go back to the largest canvas and make another pad
    # draw the upper pad later, used to cover up the bottom title
    p1 = r.TPad("p1", "", 0, 0.25, 1, 1); #  xlow, ylow, xup, yup
    p1.SetGrid();
    # p1.SetFillColor(2)
    p1.Draw();
    p1.SetBottomMargin(0.01)
    p1.cd();
    gr_data_fit.Draw('APE')
    gr_sims.Draw('PE')
    gr_data_fit.GetXaxis().SetRangeUser(0,24.5)
    gr_data_fit.GetXaxis().SetLabelOffset(999);
    gr_data_fit.GetXaxis().SetLabelSize(0);
    gr_data_fit.GetXaxis().SetTitleSize(0);
    gr_data_fit.GetYaxis().SetMaxDigits(2);

    leg = r.TLegend(*legend_pos);
    leg.SetFillColor(r.gPad.GetFillColor());
    # leg.SetTextAlign(22);
    leg.AddEntry(gr_sims, legends[0], "P");
    leg.AddEntry(gr_data_fit,legends[1], "P");
    leg.Draw();

    p1.GetListOfPrimitives().Add(leg)


    # c.cd();
    c.Draw()
    return c #,gr_rel_diff
    # c.Print("N0_vs_calo_fit_vs_gm2ringsim_run{}_{}_method.png".format(ds_name,ana_method))