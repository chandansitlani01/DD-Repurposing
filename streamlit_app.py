import threading
from DTI.dti_pred import DTI

import streamlit as st
import time
import shutil
import datetime

from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Draw import MolsToGridImage
import os

import pandas as pd





st.set_page_config(page_title="Drug Discovery", layout="wide", page_icon="logo.png")


    
st.title("Drug Repurposing")
d=pd.read_csv("antiviral_drugs.tab", delimiter="\t")
drugs=d["SMILES"].values


target=st.text_input("Enter Target Sequence")
dti=DTI()
affinities=[]
i=0


use=st.checkbox("Use Own Drugs File", help="Create a .tab file with a SMILES column")


if use:
    uploaded_file = st.file_uploader("Choose a csv file")
    if uploaded_file is not None:
        d = pd.read_csv(uploaded_file, delimiter="\t")
        drugs=d["SMILES"].values

st.warning("Dont make any action on the page after run until the program is complete else progress may get discarded.")

if st.button("Run"):
        
        
        progress=st.progress(0)
        for drug in drugs:
            p, affinity=dti.pred(drug, target)
            a=round(affinity[0][1], 3)
            affinities.append(a)
            print(i, "done")
            progress.progress((i+1)/len(d))
            i+=1
        
        print(affinities)
        progress.empty()
        data=d.copy()
        data["Affinity"]=affinities
        data["Affinity"]=data["Affinity"].map(lambda x:round(x, 3))
        data=data.sort_values("Affinity", ascending=False)
        data["SMILES"]=data["SMILES"].map(lambda x: x if len(x)<70 else x[0:70]+"...")
        data["Effect"]=data["Affinity"].map(lambda x:"Very Effective" if x >0.9 else "Effective" if x>0.8 else "Not Efective")
        print(data)
        st.text(" ")
        st.text(" ")
        # data=data.reset_index(drop=True)
        st.table(data)
        print()
        print()
        
        
    
    
    
    


    
    
        st.warning("Please Download the file using the Download Button else it can be deleted as soon as any other action is taken on the page")
        
        

