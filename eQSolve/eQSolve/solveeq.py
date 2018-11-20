'''
from PIL import Image
from pytesseract import image_to_string
image=Image.open('inspire.jpg',mode='r')
print(image_to_string(image))
'''

import re
import numpy as np
import math

def quad(eq):
	#print(eq)
	#ax2+bx+c=0
	t=eq.split('+')
	a=int(t[0][:-2])
	b=int(t[1][:-1])
	c=int(t[2][:-2])
	d = (b**2)-4*a*c
	img=''
	if(d<0):
		d=-d
		img='i'
	sol1=(-b-math.sqrt(d))/(2*a)
	sol2=(-b+math.sqrt(d))/(2*a)
	return('x1='+str(sol1)+img+'  x2='+str(sol2)+img)


def getvars(eq):
	#print(eq)
	s1=eq.split("=")
	s=s1[0].strip()
	c=float(s1[1])
	a=[]
	var=[]
	terms=s.split('+')
	for i in terms:
		#print('i:',i)
		if '-' in i:
			cnt=0
			termss=i.split('-')
			for ii in (termss):
				flag=-1
				if(cnt==0):
					cnt=1
					flag=1
				r=re.match("(\d*(\.\d*)?)([a-z]*)",ii)
				#print(ii,r.groups())
				if(r):
					v=r.groups()[2]
					if(v==''):
						c-=flag*(float(r.groups()[0]))
					else:
						if(v in var):
							j=var.index(v)
							coeff=r.groups()[0]
							if(coeff!=''):
								a[j]+=flag*(float(r.groups()[0]))
						else:
							coeff=r.groups()[0]
							if(coeff==''):
								a.append(1.0*flag)
							else:
								a.append(flag*(float(r.groups()[0])))
							var.append(v)
				
		else:
			#print(i)
			r=re.match("(\d*(\.\d*)?)([a-z]*)",i)
			#print(i,r.groups())
			if(r):
				v=r.groups()[2]
				if(v==''):
					c-=float(r.groups()[0])
				else:
					if(v in var):
						j=var.index(v)
						coeff=r.groups()[0]
						if(coeff!=''):
							a[j]+=float(r.groups()[0])
					else:
						coeff=r.groups()[0]
						if(coeff==''):
							a.append(1.0)
						else:
							a.append(float(r.groups()[0]))
						var.append(v)
	if(len(a)==1):
		if(var[0]=='x'):
			var.append('y')
			a.append(0)
		else:
			var.append('x')
			var.reverse()
			a.append(0)
			a.reverse()
	a.append(c)
	var.append('constant')
	print(a)
	print(var)
	#print('----------------------------------------')
	return(a,var)


def calcy(eq1,eq2):
	print(eq1)
	print(eq2)
		
	a1,var=getvars(eq1)
	a2,var=getvars(eq2)
	
	b = np.array([a1[-1], a2[-1]])
	a1.pop(-1)
	a2.pop(-1)
	var.pop(-1)
		
	a = np.array([a1, a2])
	x = np.linalg.solve(a, b)
	return('x='+str(x[0])+'  y='+str(x[1]))
	

#getvars('2.45y-7+r-3y=4')	
#calcy('5x-3y+2x-5x=2','4x+6y+4=12')
#calcy('y=0','x-y=-2')
#quad('1x2+4x+4=0')
#quad('5x2+2x+15=0')
