import tensorflow as tf
import pandas as pd
import numpy
import tensorflow as tf 
import json
import shutil
import numpy as np

class DTI:
	
	def __init__(self):
		self.model=tf.keras.models.load_model("DTI/models-082.h5")
		self.outs=[]

		with open("DTI/voc_DTI_D.json", 'r') as f:
			self.voc=json.load(f)


		with open("DTI/voc_DTI_Target.json", 'r') as f:
			self.voc_t=json.load(f)

	def encode(self, row):
		r2=row
		for i in range(len(row)):
			if row[i] in self.voc.keys():
					try:
						r2[i]=self.voc[row[i]]
					except:
						r2[i]=0
			else:
					r2[i]=0
		return r2

	def encode_t(self, row):
		r2=row
		for i in range(len(row)):
			try:
				r2[i]=self.voc_t[row[i]]
			except:
				r2[i]=0
		return r2

	
	def one_hot_d(self, x):
		x3d=np.zeros((x.shape[0], x.shape[1], len(self.voc)+1))
		for i in range(x.shape[0]):
			for j in range(x.shape[1]):
				x3d[i][j][x[i][j]]=1
		
		return x3d

	def one_hot_t(self, x):
		x3d=np.zeros((x.shape[0], x.shape[1], len(self.voc_t)+1))
		for i in range(x.shape[0]):
			for j in range(x.shape[1]):
				x3d[i][j][x[i][j]]=1
		
		return x3d


	def pred(self, d, t):
		d=list(d)
		d=self.encode(d)
		d=np.expand_dims(d, axis=0)
		d=tf.keras.preprocessing.sequence.pad_sequences(d, 90)
		d=d.reshape(d.shape[0], d.shape[1], 1)
		#d=one_hot_d(d)


		t=list(t)
		t=self.encode_t(t)
		t=np.expand_dims(t, axis=0)
		t=tf.keras.preprocessing.sequence.pad_sequences(t, 1300)
		t=t.reshape(t.shape[0], t.shape[1], 1)
		#t=one_hot_t(t)

		pre=self.model.predict([d, t])
		p=np.argmax(pre, axis=-1)
		return p, pre 

	def calculate(self, target):
		shutil.copy("Tox/output/output.txt", "DTI/input/input.txt")
		t=target
		with open("DTI/input/input.txt", "r") as f:
			mols=f.read()

		mols=mols.split("\n")

		op=[]
		for mol in mols:
			p, pre = self.pred(mol, t)
			if p[0]==1:
				if len(mol)>0:
					op.append(mol)
					print("Found "+mol+str(len(mol)))
				else:
					print("None Mol")

		if len(op)>0:
			self.outs=self.outs+op
		with open("DTI/output/out.txt", "a") as f:
			
			if len(op)>0:
				f.write("\n".join(op))
				f.write("\n")
				
		print("Done, found "+str(len(op))+" molecules out of "+str(len(mols)) )
		
#dti=DTI()
#dti.calculate("ATMG")
