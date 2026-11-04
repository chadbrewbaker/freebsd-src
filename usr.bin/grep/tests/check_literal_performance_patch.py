"""Enumerate short ASCII records; preserve complete output, not just totals."""
import itertools,os,subprocess
from pathlib import Path
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('baseline',type=Path)
parser.add_argument('candidate',type=Path)
args=parser.parse_args()
binaries=[str(args.baseline.resolve()),str(args.candidate.resolve())]
words=[b''.join(t) for n in range(7) for t in itertools.product([b'a',b'b',b'_',b' '],repeat=n)]
data=b'\n'.join(words)+b'\nababa aba\n'+ 'élan aé éa a\n'.encode()
checks=0
for pattern in ['a','b','aa','ab','aba','a b','_']:
 for flags in [['-Fw'],['-Fwv'],['-Fwc'],['-Fwx'],['-Fwxv'],['-Fwo']]:
  outputs=[]
  for binary in binaries:
   p=subprocess.run([binary,*flags,'-e',pattern],input=data,capture_output=True,env=dict(os.environ,LC_ALL='C'))
   outputs.append((p.returncode,p.stdout,p.stderr))
  assert outputs[0]==outputs[1],(pattern,flags)
  checks+=1
print(f'{len(words)} enumerated records, {checks} command pairs: exact output/status agreement.')

import itertools,os,subprocess
from pathlib import Path

inputs=[b'a\0b a\naba\na',b'\xff a\n\xc3a\na\n',b'\n\na a\n',('é a aé éa\n'*3).encode(),b'x'*131071+b'a\n']
flags=[['-Fa'],['-Fac'],['-Fawc'],['-Fawo'],['-Faz'],['-Fax'],['-Favn'],['-Fa','--color=always'],['-Fai'],['-Fa','-e','ab']]
n=0
for data,f,loc in itertools.product(inputs,flags,['C','en_US.UTF-8']):
 outs=[]
 for binary in binaries:
  p=subprocess.run([binary,*f,'-e','a'],input=data,capture_output=True,timeout=10,env=dict(os.environ,LC_ALL=loc))
  outs.append((p.returncode,p.stdout,p.stderr))
 assert outs[0]==outs[1],(data[:40],f,loc,outs)
 n+=1
print(n,'binary/text, locale, output, multiple-pattern and boundary-size checks passed')
