a = 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/83860227.jpg'

b = a.replace(u'/', u' ').split()
b = b[-1].replace(u'.', u' ').split()
c = b[0]

print(c)