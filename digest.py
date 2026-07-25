import os


# I resolved the problematic part by manually commenting it out in the original file.


# bound
#
# ad08
# x: 0 to 7
# y: -4 to 12
#
# ad16
# x: 0 to 15
# y: -4 to 12

#while True:
#    os.system('clear')


def handle_file(pth):
    print(f'Handle {pth}...')
    pth_src = './neodgm/bitmap_font/'+pth
    pth_dst = './digest/'+pth.replace('.ex','')
    with open(pth_src, 'r') as f:
        d = f.readlines()
    dat = []
    out_buf = ''
    name = ''
    for line in d:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('bmp_glyph'):
            a,b,c = line.split(' ')
            name = b
        elif line.startswith('advance'):
            _, ad = line.split(' ')
            if ad == 'aw':
                name = ''
                continue
            ad = int(ad)
        elif line.startswith('bounds'):
            line = line.replace(',','').replace('..', ' ')
            _, x1, x2, y1, y2 = line.split(' ')
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
        elif line[0] == '0' or line[0] == '1':
            dat.append(line)
        elif line.startswith('end'):
            if name != '':
                #print(name)
                out_buf = out_buf + name + '\n' + bitmap(f'{pth}.{name}',ad,x1,x2,y1,y2,dat) + '\n\n\n'
            dat = []
            name = ''
    
    with open(pth_dst, 'w') as f:
        f.write(out_buf)
    print('Done.')
  

def bitmap(nm,ad,x1,x2,y1,y2,dat):
    #print(ad,x1,x2,y1,y2)
    #ad = int(input('ad: '))
    #x1 = int(input('x1: '))
    #x2 = int(input('x2: '))
    #y1 = int(input('y1: '))
    #y2 = int(input('y2: '))

    #print('data:')
    #d = []
    #for y in range(y1,y2):
    #    d.append(input().strip())

    d = dat
    #print(dat)
    res = []
    res = res + ['.'*ad for i in range(12)]
    res = res + [','*ad for i in range(4)]

    if ad < x2 - x1:
        ad = x2 - x1 + 1
        print(f'[   ad changed    ] {nm:60s}')

    if len(d[0]) != (x2 - x1):
        offset = len(d[0])
        x1 = (ad - offset) // 2
        x2 = x1 + offset
        print(f'[ x range changed ] {nm}')


    for y in range(y1, y2):
        for x in range(x1, x2):
            yy = y - y1
            xx = x - x1
            ry = 12 - y2 + yy
            rx = x
            #print(' ', yy)
            if d[yy][xx] == '1':
                res[ry] = res[ry][:rx] + '#' + res[ry][rx+1:]
    return '\n'.join(res)

    #print('\n'.join(res))
    #input('Press any key to continue.')



for pth in [nm for nm in os.listdir('./neodgm/bitmap_font') if nm.endswith('.ex')]:
    handle_file(pth)
for pth in [nm for nm in os.listdir('./neodgm/bitmap_font/components') if nm.endswith('.ex')]:
    handle_file('components/'+pth)
for pth in [nm for nm in os.listdir('./neodgm/bitmap_font/programming_ligatures') if nm.endswith('.ex')]:
    handle_file('programming_ligatures/' + pth)
