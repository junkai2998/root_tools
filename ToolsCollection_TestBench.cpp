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