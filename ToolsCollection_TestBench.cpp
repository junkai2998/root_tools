#include <iostream>
#include <string>
#include "ToolsCollection.h"

using namespace std;

void ToolsCollection_TestBench(){
        cout << "welcome to the test bench" << endl;
        //testcut(2,8);
}

void testcut(int start, int last){
        cout << "zzz" << endl;
        TH1D* h1 = new TH1D("h1","h1;x;y",10,0,20);
        h1->SetLineColor(2);
        for (int i=0; i<10;i++){h1->SetBinContent(i+1,2*i+1);};
        TH1D* h1_cut = cut_th1d(h1, start, last,"histozzzzz_cut");

        TCanvas* c = new TCanvas("c","c",800,600);
        c->Divide(2,1);
        c->cd(1)->SetGrid();
        h1->Draw("hist");
        c->cd(2)->SetGrid();
        h1_cut->Draw("hist");
        c->Draw();
}


void testfft(){
        TF1* func = new TF1("func","1+0.5*cos(6*x+1.5)",0,20);
        TH1D* h1 = new TH1D("h1","h1;t;y",100,0,20);
        h1->SetLineColor(2);
        h1->FillRandom("func",10000); // also can: func->GetRandom(); // then fill
        TH1D* hfft = fft(h1,"new_fft","title for fft",0.01);

        TCanvas* c = new TCanvas("c","c",800,600);
        c->Divide(2,1);
        c->cd(1)->SetGrid();
        h1->Draw("hist");
        c->cd(2)->SetGrid();
        hfft->Draw("hist");
        c->Draw();

}


void testFindPeaks(){
    
int npts = 4000;

TF1* func = new TF1("func","1 + 0.5*cos(14.48*x + 0)",0,npts*0.1492); 
func->SetNpx(npts*2);

TH1D* hist = new TH1D("hist","hist",npts,0,npts*0.1492);
    
int N = 100000;
for(int i=0;i<N;i++){
    double t = func->GetRandom();
    hist->Fill(t);
    //hist_bin2.Fill(t);
    //hist_bin4.Fill(t);
    };

// 	hist->FillRandom("func",N);
    

TCanvas c = TCanvas("cc","c",400,400);
TH1D* hist_fft = fft(hist,"fft_name","FFT",0.01); // without new fft(...), because you already have new TH1D in that function !

// this work
hist_fft->Draw();
int maxpositions=3;
double resolution=1.0;
double sigma=2.0;
string option="";
double threshold=0.1;
bool draw=true;
bool addToHist=false;
int decimal_places=1;
string unit="GHz";
identify_hist_peaks3(hist_fft,maxpositions,resolution,sigma,option,threshold,draw,addToHist,unit,decimal_places);


// void identify_hist_peaks3(TH1D* hist,int maxpositions=3, double resolution=1.0,
//                           double sigma=2.0, string option="", double threshold=0.1,
//                           bool draw=false, bool addToHist=false,
//                           string unit="MHz",int decimal_places=2,
//                           int color=2,int markerstyle=23,double textsize=0.04){

c.Draw();
c.Print("testFindPeaks.png");
}
