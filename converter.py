try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

tree = ET.ElementTree(file='input.txt.xml')
root = tree.getroot()
docu = root.find('document')
sents = docu.find('sentences').findall('sentence')
output  = open('input.ann', 'w')
rtypecount = 1
spanlist=[]
relationList=[]
for sent in sents:
	targetDep = 0
	tokens = 0
	sentId = 0
	sentId = str(sent.get('id'))
	tokens = sent.find('tokens').findall('token')
	for dep in sent.findall('dependencies'):
		if dep.get('type') == 'collapsed-dependencies':
			targetDep = dep
			break
	for t in tokens:
		tid = 'T'+ sentId + str(t.get('id'))
		pos = str(t.find('POS').text)
		if pos not in spanlist:
			spanlist.append(pos)
		sidx = str(t.find('CharacterOffsetBegin').text)
		eidx = str(t.find('CharacterOffsetEnd').text)
		word = str(t.find('word').text)
		output.write(tid+'\t'+pos+' '+sidx+' '+eidx+'\t'+word+'\n')
	for d in targetDep:
		rword = str(d.get('type')).replace(':','_')

		rid = 'R'+str(rtypecount)
		rtypecount+=1
		if rword not in relationList:
			relationList.append(rword)

		govidx = d.find('governor').get('idx')
		if govidx == '0':
			govidx = 1
		gov = 'T'+sentId+str(govidx)
		dpdidx = d.find('dependent').get('idx')
		if dpdidx == '0':
			govidx = 1
		dpd = 'T'+sentId+str(dpdidx)
		output.write(rid+'\t'+rword+' governor:'+gov+' dependent:'+dpd+'\n')
output.close()

conf = open('annotation.conf', 'w')
conf.write('[entities]\n')
for sp in spanlist:
	conf.write(sp+'\n')
conf.write('\n[relations]\n')
for rl in relationList:
	conf.write(rl+'\t'+'governor:<ENTITY>, dependent:<ENTITY>\n')
conf.close()
