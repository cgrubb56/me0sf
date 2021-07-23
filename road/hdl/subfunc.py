#Functions used in multiple files
import numpy as np
import math


class hi_lo_t:
    def __init__(self,hi,lo):
        self.hi=hi
        self.lo=lo

class patdef_t:
    def __init__(self, id, ly0, ly1, ly2, ly3, ly4, ly5):
        self.id=id
        self.ly0=ly0
        self.ly1=ly1
        self.ly2=ly2
        self.ly3=ly3
        self.ly4=ly4
        self.ly5=ly5

def mirror_patdef(pat,id):
    ly0_h=pat.ly0.lo*(-1)
    ly0_l=pat.ly0.hi*(-1)
    ly1_h=pat.ly1.lo*(-1)
    ly1_l=pat.ly1.hi*(-1)
    ly2_h=pat.ly2.lo*(-1)
    ly2_l=pat.ly2.hi*(-1)
    ly3_h=pat.ly3.lo*(-1)
    ly3_l=pat.ly3.hi*(-1)
    ly4_h=pat.ly4.lo*(-1)
    ly4_l=pat.ly4.hi*(-1)
    ly5_h=pat.ly5.lo*(-1)
    ly5_l=pat.ly5.hi*(-1)
    ly0=hi_lo_t(ly0_h,ly0_l)
    ly1=hi_lo_t(ly1_h,ly1_l)
    ly2=hi_lo_t(ly2_h,ly2_l)
    ly3=hi_lo_t(ly3_h,ly3_l)
    ly4=hi_lo_t(ly4_h,ly4_l)
    ly5=hi_lo_t(ly5_h,ly5_l)
    result=patdef_t(id,ly0,ly1,ly2,ly3,ly4,ly5)
    return result

def count_ones(int_ones):
        n_ones=0
        iterable=bin(int_ones)[2:]
        for i in range(len(iterable)):
            if iterable[i]=='1':
                n_ones=n_ones+1
        return n_ones;

def set_bit(index,num1=0,MAX_SPAN=37):
    r_index=(MAX_SPAN-index)-1
    num2=1<<r_index
    final_v=num1|num2
    return final_v

def clear_bit(num,index,MAX_SPAN=37):
    index=MAX_SPAN-index-1
    bit = 1 & (num>>index)
    return (num ^ (bit << index))

def ones_bit_mask(num):
    o_mask=0
    iterable_data=bin(num)[2:]
    for m in range(len(iterable_data)):
        mask_1=1<<m
        o_mask=o_mask|mask_1
    return o_mask

def get_ly_mask(ly_pat,MAX_SPAN=37):
        m_vec=[]
        center=round(MAX_SPAN/2)
        a_lo=ly_pat.ly0.lo+center
        a_hi=ly_pat.ly0.hi+center
        b_lo=ly_pat.ly1.lo+center
        b_hi=ly_pat.ly1.hi+center
        c_lo=ly_pat.ly2.lo+center
        c_hi=ly_pat.ly2.hi+center
        d_lo=ly_pat.ly3.lo+center
        d_hi=ly_pat.ly3.hi+center
        e_lo=ly_pat.ly4.lo+center
        e_hi=ly_pat.ly4.hi+center
        f_lo=ly_pat.ly5.lo+center
        f_hi=ly_pat.ly5.hi+center
        m_vals=[[a_lo,a_hi],[b_lo,b_hi],[c_lo,c_hi],[d_lo,d_hi],[e_lo,e_hi],[f_lo,f_hi]]
        for i in range(len(m_vals)):
            index=MAX_SPAN-m_vals[i][0]-1
            holder=0
            while (index!=MAX_SPAN-m_vals[i][1]-2):
                val=1<<index
                holder=holder|val
                index-=1
            m_vec.append(holder)
        return m_vec







def get_lc_id(patlist,ly0_x,ly1_x,ly2_x,ly3_x,ly4_x,ly5_x,MAX_SPAN=37):
        len_patlist=len(patlist)
        corr_pat_id=np.zeros(len_patlist)
        pats_m=[]
        for w in range(len_patlist):
            pats_m.append(get_ly_mask(patlist[w]))
        ly0_a=np.zeros(MAX_SPAN)
        ly1_a=np.zeros(MAX_SPAN)
        ly2_a=np.zeros(MAX_SPAN)
        ly3_a=np.zeros(MAX_SPAN)
        ly4_a=np.zeros(MAX_SPAN)
        ly5_a=np.zeros(MAX_SPAN)
        lc_vec_x=np.zeros(len_patlist)
        lc_id_vec=[]
        for v in range(len_patlist):
            for h in range(MAX_SPAN):
                ly0_a[h]=pats_m[v][0][h]*ly0_x[h]
                ly1_a[h]=pats_m[v][1][h]*ly1_x[h]
                ly2_a[h]=pats_m[v][2][h]*ly2_x[h]
                ly3_a[h]=pats_m[v][3][h]*ly3_x[h]
                ly4_a[h]=pats_m[v][4][h]*ly4_x[h]
                ly5_a[h]=pats_m[v][5][h]*ly5_x[h]
            ly0_ones=count_ones(ly0_a)
            ly1_ones=count_ones(ly1_a)
            ly2_ones=count_ones(ly2_a)
            ly3_ones=count_ones(ly3_a)
            ly4_ones=count_ones(ly4_a)
            ly5_ones=count_ones(ly5_a)
            if (ly0_ones>=1):
                ly0_h=1
            else:
                ly0_h=0
            if (ly1_ones>=1):
                ly1_h=1
            else:
                ly1_h=0
            if (ly2_ones>=1):
                ly2_h=1
            else:
                ly2_h=0
            if (ly3_ones>=1):
                ly3_h=1
            else:
                ly3_h=0
            if (ly4_ones>=1):
                ly4_h=1
            else:
                ly4_h=0
            if (ly5_ones>=1):
                ly5_h=1
            else:
                ly5_h=0
            lc_vec_x[v]=ly0_h+ly1_h+ly2_h+ly3_h+ly4_h+ly5_h

        for i in range(len(patlist)):
                    corr_pat_id[i]=patlist[i].id
        for p in range(len_patlist):
                    lc_id_vec.append([lc_vec_x[p],corr_pat_id[p]])

        return lc_id_vec
