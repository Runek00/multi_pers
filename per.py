"""
Program finds the lowest number in given range
with largest miltiplicative persistance
for example:
	35[3*5]->15[1*5]->5:2
	679[7*7*9]->378[3*7*8]->168[1*6*8]->48[4*8]->32[3*2]->6:5
"""

from multiprocessing import Queue, Process
import time

def per(num):
	if len(num) == 1:
		return 0
	tab = [int(i) for i in num]
	out = 1
	for j in tab:
		out *= j
	return 1 + per(str(out))

def tabsProc(q, x, y):
	for n in range(x, y):
		tab = [int(i) for i in str(n)]
		dont = False
		if tab[0] == 1:
			dont = True
		else:
			for s in range (1, len(tab)):
				if tab[s] == 1 or tab[s] == 0 or tab[s] < tab[s-1] or tab[s]*tab[s-1] <= 10:
					dont = True
					break
			if dont == False:
				q.put(n)

def msftabs(q, intab):
	outn = 0
	out = 0
	for n in intab:
		x = per(str(n))
		if x > out or (x == out and n < outn):
			out = x
			outn = n
	outer = (outn, out)
	q.put(outer)

def lengthsummer(ar):
	out = 0
	for i in ar:
		out += len(i)
	return out

def checkout(cur, cand):
	if cur[1] < cand[1] or (cur[1] == cand[1] and cand[0] < cur[0]):
		return cand
	else:
		return cur

if __name__ == '__main__':
	t0 = time.time()
	tr = 7 #number of processess
	minnum = 1#26666666
	maxnum = 3778889000
	if minnum > maxnum:
		print('Range is the other way around')
	else:
		queue = Queue()
		freds = []
		tabs = []
		r = int((maxnum-minnum)/tr)+1
		for x in range(0, tr):
			tabs.append([])
			# for y in range(minnum+r*x, minnum+r*(x+1)):
			# 	tabs[x].append(y)
			p = Process(target = tabsProc, args = (queue, minnum+r*x, minnum+r*(x+1)))
			freds.append(p)
			p.start()
		cnt = 0
		wait = True
		while wait == True:
			wait = False
			for p in freds:
				if p.is_alive():
					wait = True
			if not queue.empty():
				wait = True
				tabs[cnt%tr].append(queue.get())
				cnt += 1
		for p in freds:
			p.join()
		print('phase 1 completed with cnt = ' + str(cnt))
		print('tabs length sum = ' + str(lengthsummer(tabs)))
		print('time so far: ' + str(time.time()-t0))
		freds = []
		for x in range (0, tr):
			p = Process(target = msftabs, args = (queue, tabs[x]))
			freds.append(p)
			p.start()
		out = (0, 0)
		wait = True
		while wait == True:
			wait = False
			if not queue.empty():
				wait = True
				out = checkout(out, queue.get())
				continue
			for p in freds:
				if p.is_alive():
					wait = True
		for p in freds:
			p.join()
		print(out)
		print('finishing time: ' + str(time.time()-t0))