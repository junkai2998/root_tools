#ifndef TOOLSCOLLECTION_H
#define TOOLSCOLLECTION_H

#include <iostream>

using namespace std;

TH1D* cut_th1d(TH1D* hist, int start_bin, int last_bin, string hist_name="histo_cut"){
    /*
    written for root 6.24
    6.26 also work ?

    start_bin = 1
    last_bin = hist.GetNbinsX()

    cut the original th1d with selected (bin) range
    th1d is defined as N, xlow, xup, with:
        index 0 is underflow
        index 1 as the index of its first bin
        index N is the last bin
        index N+1 is the overflow
    
    xlow is the lower limit, which is also the low edge of the first (1) bin
    xup  is the upper limit, which is also the up edge of the last (N) bin, also the low edge of the overflow (n+1) bin
    */

    int nbins_ori = hist->GetNbinsX();
    int nbins_new = last_bin - start_bin + 1;
    double bin_width = hist->GetBinWidth(1);
    double xlow_new = (start_bin - 1) * bin_width;
    double xup_new =  last_bin * bin_width;
    
    TString title_new = Form("%s;%s;%s", hist->GetTitle(), hist->GetXaxis()->GetTitle(), hist->GetYaxis()->GetTitle());
    TH1D* hist_cut = new TH1D(hist_name.c_str(), title_new.Data(), nbins_new, xlow_new, xup_new);

    cout << "original: nbsins, xlow, xup, xwidth: ";
	cout << " " << nbins_ori<< " " << hist->GetBinLowEdge(1)<< " " ;
	cout << hist->GetBinLowEdge(nbins_ori+1)<< " " << hist->GetBinWidth(1) << endl;

    cout << "cut: nbins, xlow, xup, xwidth : "<< " ";
	cout << nbins_new<< " " << hist_cut->GetBinLowEdge(1)<< " " ;
	cout << hist_cut->GetBinLowEdge(nbins_new+1)<< " " << hist->GetBinWidth(1) << endl;

    hist_cut->SetMarkerStyle(hist->GetMarkerStyle());
    hist_cut->SetMarkerSize(hist->GetMarkerSize());
    hist_cut->SetMarkerColor(hist->GetMarkerColor());
    hist_cut->SetLineStyle(hist->GetLineStyle());
    hist_cut->SetLineColor(hist->GetLineColor());
    hist_cut->SetLineWidth(hist->GetLineWidth());

	 for (int i=start_bin; i<(last_bin+1);i++){
		hist_cut->SetBinContent(i-start_bin+1, hist->GetBinContent(i));
        hist_cut->SetBinError(i-start_bin+1, hist->GetBinError(i));

	//   debug with TH1D* h1 = new TH1D("h1","h1;x;y",10,0,20);
    //   for (int i=0; i<10;i++){h1->SetBinContent(i+1,2*i+1);};
// 		cout << Form("%d-th bin of the original histo, %d-th bin of the new histo",i,i-start_bin+1) << endl;
// 		cout << hist->GetBinCenter(i) << " " << hist_cut->GetBinCenter(i-start_bin+1)  << endl;
	};

    return hist_cut;
}



TH1D* fft(TH1D* hist, string fftname="default_fft_name", string given_title="FFT", double fstart=0.01){
    double bin_width = hist->GetBinWidth(1);
    cout << bin_width << endl;
    
    TString title = Form("%s ;f [MHz]; FFT Magnitude [arb.]",given_title.c_str());
    
    TH1D* fft_hist = new TH1D(fftname.c_str(), title.Data(), hist->GetNbinsX(), 0, 1.0/bin_width);
    hist->FFT(fft_hist, "MAG");
    fft_hist->GetXaxis()->SetRangeUser(fstart,fft_hist->GetXaxis()->GetXmax()/2); // fstart to get rid of the DC component
    return fft_hist;
}


TH1D* fft2(TH1D* hist, string fftname="default_fft_name", string given_title="FFT", double fstart=0.01,string fft_option="MAG"){
    /*
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
    */
    double bin_width = hist->GetBinWidth(1);
//     cout << bin_width << endl;
    
    string yaxis_label;
    if(strcmp(fft_option.c_str(),"MAG")==0){yaxis_label = "Magnitude [arb.]";}
    else if(strcmp(fft_option.c_str(),"RE")==0){yaxis_label = "Real Component [arb.]";}
    else if(strcmp(fft_option.c_str(),"IM")==0){yaxis_label = "Imaginary Component [arb.]";}
    else if(strcmp(fft_option.c_str(),"PH")==0){yaxis_label = "Phase [rad]";}
    else{
        cout << "invalid option, using Magnitude instead" << endl;
        fft_option="MAG";
        yaxis_label = "Magnitude [arb.]";
        };
    TString title = Form("%s ;f [MHz]; FFT %s",given_title.c_str(),yaxis_label.c_str());
    
    TH1D* fft_hist = new TH1D(fftname.c_str(), title.Data(), hist->GetNbinsX(), 0, 1.0/bin_width);
    hist->FFT(fft_hist, fft_option.c_str());
    fft_hist->GetXaxis()->SetRangeUser(fstart,fft_hist->GetXaxis()->GetXmax()/2); // fstart to get rid of the DC component
    return fft_hist;
}




void identify_hist_peaks3(TH1D* hist,int maxpositions=3, double resolution=1.0,
                          double sigma=2.0, string option="", double threshold=0.1,
                          bool draw=false, bool addToHist=false,
                          string unit="MHz",int decimal_places=2,
                          int color=2,int markerstyle=23,double textsize=0.04){

    TSpectrum * peak_finder = new TSpectrum(maxpositions, resolution); // (int maxpositions, double resolution = 1)
    int npeaks = peak_finder->Search(hist,sigma,option.c_str(),threshold); // int TSpectrum::Search(const TH1* hist, double sigma = 2, const char* option = "", double threshold = 0.050000000000000003)
    cout << "found " << npeaks << " peak(s) in the range." << endl;
    TPolyMarker* pm = (TPolyMarker*) hist->FindObject("TPolyMarker");
    pm->SetMarkerStyle(markerstyle);
    pm->SetMarkerColor(color);

    if(addToHist){hist->GetListOfFunctions()->Add(pm->Clone()); };
    if(draw){pm->Draw(); };
     // caveat: if not draw, the TPoly will resides in the ListOfFunction of that histo.
     //         if draw, the TPoly need to be attached to the ListOfFunction, in order to be drawn

    // int npeaks = pm->GetN();
    for (int pk=0; pk<npeaks;pk++){
        //cout << pm->GetX()[pk] << endl;
        //TString formatted_text = Form("%.*f %s", decimal_places, pm->GetX()[pk],unit.c_str());
        TLatex* text = new TLatex(pm->GetX()[pk]*1.05, pm->GetY()[pk]*0.9, Form("%.*f %s", decimal_places, pm->GetX()[pk],unit.c_str()));
        text->SetTextColor(color);
        text->SetTextSize(textsize);
        if(draw){text->DrawClone(); };
        if(addToHist){hist->GetListOfFunctions()->Add(text); };
    };
}
#endif