#Matplotlib display for different levels of hardware design
# from matplotlib.lines import _LineStyle
import matplotlib.pyplot as plt
from subfunc import*
from pat_unit_beh import process_pat
from datadev import datadev
import random
from linear_reg_table import*


def get_mypattern(pat_id:int, patlist:'List[patdef_t]') -> patdef_t:
    assert type(pat_id) == int, "pat_id input must be an integer"
    assert (
        type(patlist) == list
    ), "patlist input must be a list of patdef_t class values"
    assert (
        type(patlist[0]) == patdef_t
    ), "each value in patlist input must be of the class patdef_t"
    assert (
        type(patlist[0].ly0) == hi_lo_t
    ), "each patlist layer must be of the class hi_lo_t"
    assert type(patlist[0].id) == int, "each patlist id must be an integer"
    for i in range(len(patlist)):
        if patlist[i].id == pat_id:
            mypattern = patlist[i]
    return mypattern

def best_fit(x_data, y_data):
    """takes in x_data and y_data to determine the values necessary for linear regression; uses linear least squares method"""
    # eliminate data values that correlate to no hits within the mask of a layer
    # elimination_indices = []
    # for i in range(len(y_data)):
    #     if y_data[i] == None:
    #         elimination_indices.append(i)
    # elimination_vals = []
    # for j in range(len(elimination_indices)):
    #     elimination_vals.append(x_data[elimination_indices[j]])
    # x_data = set(x_data)
    # elimination_vals = set(elimination_vals)
    # x_data = x_data - elimination_vals
    # x_data = list(x_data)
    # y_data = [n for n in y_data if n != None]
    sum_x = 0
    sum_y = 0
    for i in range(len(x_data)):
        sum_x = sum_x + x_data[i]
        sum_y = sum_y + y_data[i]
    n = len(x_data)
    xy_list = []
    x_sq_list = []
    for k in range(len(x_data)):
        xy_list.append(x_data[k] * y_data[k])
        x_sq_list.append(x_data[k] ** 2)
    sum_xy = sum(xy_list)
    sum_x_sq = sum(x_sq_list)
    denominator = n * sum_x_sq - sum_x ** 2
    if denominator == 0:
        denominator = 1
    slope = (n * sum_xy - (sum_x * sum_y)) / denominator
    b = (sum_y - slope * sum_x) / n
    y_fit = []
    for j in range(len(y_data)):
        y_fit.append(slope * x_data[j] + b)
    slope = round(slope, 8)
    b = round(b, 8)
    int(slope)
    int(b)
    for i in range(len(y_fit)):
        y_fit[i]=int(y_fit[i])

    return slope, b, y_fit

def strip2mask(ly_pat, strip):
        """takes in a given layer pattern and returns a list of integer bit masks for each layer"""
        assert type(ly_pat)==patdef_t,"ly_pat input must be defined in the patdef_t class"
        assert type(ly_pat.ly0)==hi_lo_t,"each layer of ly_pat must be of the class hi_lo_t"
        assert type(ly_pat.id)==int,"ly_pat's id must be an integer"
        assert type(MAX_SPAN)==int,"MAX_SPAN input must be an integer"
        m_vec = []
        # generate indices of the high bits for each layer based on the provided hi and lo values from the pattern definition
        a_lo = ly_pat.ly0.lo + strip
        a_hi = ly_pat.ly0.hi + strip
        b_lo = ly_pat.ly1.lo + strip
        b_hi = ly_pat.ly1.hi + strip
        c_lo = ly_pat.ly2.lo + strip
        c_hi = ly_pat.ly2.hi + strip
        d_lo = ly_pat.ly3.lo + strip
        d_hi = ly_pat.ly3.hi + strip
        e_lo = ly_pat.ly4.lo + strip
        e_hi = ly_pat.ly4.hi + strip
        f_lo = ly_pat.ly5.lo + strip
        f_hi = ly_pat.ly5.hi + strip
        m_vals = [
            [a_lo, a_hi],
            [b_lo, b_hi],
            [c_lo, c_hi],
            [d_lo, d_hi],
            [e_lo, e_hi],
            [f_lo, f_hi],
        ]
        # use the high and low indices to determine where the high bits must go for each layer
        for i in range(len(m_vals)):
            holder = 0
            # keep setting high bits from the low index to the high index; leave all else as low bits
            for index in range(m_vals[i][0], m_vals[i][1] + 1):
                val = 1 << index
                holder = holder | val
            m_vec.append(holder)
        return m_vec

def filter_hits(hits,pat_id,patlist,MAX_SPAN=37):
    '''Takes a list of hit data and a pattern ID to filter hits to only exists within patterns'''
    ly_pat=get_mypattern(pat_id=pat_id,patlist=patlist)
    m_vec=get_ly_mask(ly_pat=ly_pat,MAX_SPAN=MAX_SPAN)
    hits_out=[]
    for i in range(len(hits)):
        # print(bin(hits[i])[2:].zfill(MAX_SPAN))
        # print('\n')
        # print(bin(m_vec[i])[2:].zfill(MAX_SPAN))
        # print('\n')
        hits_out.append(hits[i]&m_vec[i])
        # print(bin(hits_out[i])[2:].zfill(MAX_SPAN))
        # print('\n')
    return hits_out

def int2_xy(int_vec,width):
    binary_vec=[]
    for t in range(len(int_vec)):
        binary_vec.append(bin(int_vec[t])[2:].zfill(width))
    # print(binary_vec)
    total_x=[]
    total_y=[]
    for j in range(len(binary_vec)):
        x=[]
        y=[]
        for k in range(len(binary_vec[j])):
            if (binary_vec[j][k]=='1'):
                x.append(k)
                y.append(j)
        total_x.append(x)
        total_y.append(y)
    return total_x,total_y


def plotting_disp(patlist=patlist,hits=None,fits=None,pats_found=None,width=192):
    #notes for Chloe:
    #hits come in as a list of 6 integers
    #fits should come in as a m and a b --> might have to have info
    #on what vals we also used to create these; centroid info o/w fits not gonna work
    #fits = [[m,b,[centroids_x]]]
    #pat found should come in as a pat id and strip; must orient this on the strip given
    #use the read of patlist from firmware and getmypattern function to configure this
    #order of operations --> get the pattern get drawn first in cyan 'c' with a markersize=10
    #then throw on the hits with black o's 'ko'
    #then connect the dots with black lines--> fits come last
    if pats_found is not None:
        for a in range(len(pats_found)):
            pattern=get_mypattern(pat_id=pats_found[a][0],patlist=patlist)
            m_vec=strip2mask(ly_pat=pattern,strip=pats_found[a][1])
            # print(m_vec)
            [x_pat,y_pat]=int2_xy(int_vec=m_vec,width=width)
            for b in range(len(x_pat)):
                plt.plot(x_pat[b],y_pat[b],'cs',markersize=10)
    if hits is not None:
        [hits_x,hits_y]=int2_xy(hits,width)
        for l in range(len(hits_x)):
            plt.plot(hits_x[l],hits_y[l],'ko')
    if fits is not None:
       for z in range(len(fits)):
            y_fits=[]
            for a in range(len(fits[z][2])):
                # print('m is %.2f'%fits[z][0])
                # print('x is %d'%fits[z][2][a])
                # print('b is %d'%fits[z][1])
                if (fits[z][2][a]==0):
                    y_fits.append(0)
                else:
                    y_fits.append(fits[z][0]*fits[z][2][a]+float(fits[z][1]))
            # for v in range(len(y_fits)):
        #     print('x_fits is %d long'%len(fits[z][2]))
        #     print('y_fits is %d long'%len(y_fits))
        #     print('x is '+str(fits[z][2]))
        #     print('y_fits is ' +str(y_fits))
            x_vals=fits[z][2]
            # print('x_vals is '+str(x_vals))
            # print('y_fits is '+str(y_fits))
            # print(len(x_vals))
            # print(len(y_fits))
            for v in range(len(fits[z][2])):
                if (v==len(fits[z][2])):
                   break
                if (x_vals[v]==0):
                    x_vals.pop(v)
                    y_fits.pop(v)
                    v-=1
            # print('x_vals is '+str(x_vals))
            # print('y_fits is '+str(y_fits))
            # print(len(x_vals))
            # print(len(y_fits))
            plt.plot(x_vals,y_fits,'k-')
            m=round(fits[z][0],4)
            b=round(fits[z][1],4)
            fits_string='y'+'='+str(m)+'x'+'+'+str(b)
            plt.legend([fits_string])
    plt.show()

#testing with pat_unit.vhd
random.seed(56)
for i in range(20):
    MAX_SPAN=37
    [ly0_x,ly1_x,ly2_x,ly3_x,ly4_x,ly5_x]=datadev(MAX_SPAN=MAX_SPAN)
    [pat_id, ly_c]=process_pat(patlist=patlist,ly0_x=ly0_x,ly1_x=ly1_x,ly2_x=ly2_x,ly3_x=ly3_x,ly4_x=ly4_x,ly5_x=ly5_x,MAX_SPAN=MAX_SPAN)
    # print('pat_id is %d'%pat_id)
    hits=[ly0_x,ly1_x,ly2_x,ly3_x,ly4_x,ly5_x]
    strip=MAX_SPAN//2
    pats_found=[[pat_id,strip]]
    centroids=[]
    hits_2=filter_hits(hits=hits,pat_id=pat_id,patlist=patlist,MAX_SPAN=MAX_SPAN)
    for k in range(len(hits_2)):
        centroids.append(general_findcentroid(data=hits_2[k],width=MAX_SPAN))
    y_list=[0,1,2,3,4,5]
    [slope, b, y_fit]=best_fit(x_data=centroids, y_data=y_list) #NOTE: y_list is not used, we just use it here
    #since I didn't wanna modify an existing function for a testing phase
    # b=[0,1,2,3,4,5]
    fits=[[slope,b,centroids]]
    plotting_disp(patlist=patlist,hits=hits,fits=fits,pats_found=pats_found,width=37)
