import pandas as pd
from lxml import objectify, etree
import datetime

path = r'C:\Users\mattk\Documents\Projects\Import_XML\Raw_XML2\Swaptions_results_2018-01-31.xml'
path_out =r'C:\Users\mattk\Documents\Projects\Import_XML\Out_csv2\Swaptions_results.txt' 

parser =etree.XMLParser(remove_blank_text = True)
tree = etree.parse(path,parser)
root = tree.getroot()


for elem in root.getiterator():
    if not hasattr(elem.tag, 'find'): continue
    i = elem.tag.find('}')
    if i >= 0:
        elem.tag = elem.tag[i+1:]
objectify.deannotate(root, cleanup_namespaces=True)

dfcols = ['ValueDate','ClientForward','ClientImpliedVolatility','ClientPrice','ConsensusForward','ImpliedConsensusVolatility','ConsensusPrice','ExerciseDate','OptionType','StandardDeviationPrice','StrikeRelative','Tenor','Exp']
df = pd.DataFrame(columns = dfcols)


def datedif(a):
    dif = a
    if dif<= 38:
        return '1m'
    elif dif <= 75:
        return '2m'
    elif dif <= 100:
        return '3m'
    elif dif <= 200:
        return '6m'
    elif dif <= 300:
        return '9m'
    elif dif <= 400:
        return '1y'
    elif dif <= 600:
        return '18m'
    elif dif <= 800:
        return '2y'
    elif dif <= 1200:
        return '3y'
    elif dif <= 1600:
        return '4y'
    elif dif <= 1900:
        return '5y'
    elif dif <= 2700:
        return '7y'
    elif dif <= 3800:
        return '10y'
    elif dif <= 4500:
        return '12y'
    elif dif <= 6000:
        return '15y'
    elif dif <= 8000:
        return '20y'
    elif dif <= 10000:
        return '25y'
    elif dif <= 12000:
        return '30y'
    else:
        return 'other'

def getvalue(node):
    return node.text if node is not None else node

for node in root[7][3:]:
    hfwd  = node.find('ClientForward')
    hivol  = node.find('ClientImpliedVolatility')
    hpx = node.find('ClientPrice')
    cfwd  = node.find('ConsensusForward')
    civol  = node.find('ImpliedConsensusVolatility')
    cpx = node.find('ConsensusPrice')
    exp = node.find('ExerciseDate')
    opt_type = node.find('OptionType')
    stdev = node.find('StandardDeviationPrice')
    strike = node.find('StrikeRelative')
    tenor = node.find('Tenor')
    v = datetime.datetime.strptime(root[1].text,"%Y-%m-%d").date()
    x = datetime.datetime.strptime(getvalue(exp),"%Y-%m-%d").date()
    df = df.append( pd.Series([v,getvalue(hfwd), getvalue(hivol), getvalue(hpx),getvalue(cfwd),getvalue(civol),getvalue(cpx),x,getvalue(opt_type),getvalue(stdev),getvalue(strike),getvalue(tenor),datedif((x-v).days)], index = dfcols), ignore_index=True)


df.to_csv(path_out,index = False)
print(df.Exp.unique())

