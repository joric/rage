import sys
import struct


filename = 'RAGE_2.txt'
#filename = 'HT10SE.txt'

filename = sys.argv[1] if len(sys.argv)>1 else filename


def interval(a):
    out = []
    begin = a[0]
    for i in range(1, len(a)):
        if a[i-1]+1 != a[i] and a[i-1]!=a[i]:
            out.append( ( begin, a[i-1] ) )
            begin = a[i]

    out.append( (begin, a[len(a)-1]) )
    return out

f = open(filename).read().splitlines()
f = f[f.index('frame_data') + 2:]

frames = []
ints = []

for s in f:
    r = [int(x) for x in s.split(' ')]
    ints.append( [ struct.unpack( ">I", bytearray( r[i*4:i*4+4] ) )[0] for i in range(4) ] )
    frames.append(r[:14])

    #if len(frames)==256: break

size = 16

while len(frames)%size!=0:
    frames.append(frames[len(frames)-1])
    ints.append(ints[len(ints)-1])

total = 0
rows = 14

d = {}

for row in range(rows):

    for i in range(len(frames)//size):
        ofs = i*size

        f = frames[ofs:ofs+size]

        v = tuple([x[row] for x in f])

        if not v in d:
            d[v] = {}


        if not row in d[v]:
            d[v][row] = []

        d[v][row].append(i)


#for k,v in d.items(): print(''.join(['%02x' % x for x in k]), v)

print('#define FRAMES %d' % len(frames))
print('#define LOOP_FRAME %d' % 512)
print('#define CHUNKS %d' % len(d))
print('#define CHUNK_SIZE %d' % size)

print('ivec4 get_reg(int r, int i) {')

default_key = tuple([0]*size)
if (default_key) in d: del d[default_key]

for k,v in d.items():
    out = []
    for r,idx in v.items():
        cond = []
        for a,b in interval(idx):
            cond.append ( ('(i>=%d && i<=%d)' % (a, b)) if a!=b else ('i==%d' % (a)) )
        out.append( '(r==%d && (%s))'  % (r, ' || '.join(cond)) )

    ii = [ struct.unpack( ">I", bytearray( k[i*4:i*4+4] ) )[0] for i in range(size//4) ]

    val = '0'
    if size==16:
        val = 'ivec4(%s)' % ','.join('0x%08x' % x for x in ii)
    if size==4:
        val = '0x%08x' % ii[0]

    print('    if (%s) return %s;' % (' || '.join(out), val) )


print('    return ivec4(0);')
print('}')

s1 = len(frames)*rows

s2 = len(d)*size

print('intervals:', len(frames)//size)
print('full frames:', len(frames))
print('unique frames:', len(d))
print('compression: %d/%d (%.2f%%)' % (s2,s1, s2*100/s1))





