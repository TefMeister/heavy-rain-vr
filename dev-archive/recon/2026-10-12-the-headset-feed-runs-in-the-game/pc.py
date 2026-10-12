"""Global image shift by phase correlation. usage: pc.py ref.png a.png b.png ..."""
import sys, numpy as np
from PIL import Image
g=lambda f:np.asarray(Image.open(f).convert('L')).astype(float)
a=g(sys.argv[1]); w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
A=np.fft.fft2((a-a.mean())*w)
for f in sys.argv[2:]:
    b=g(f); B=np.fft.fft2((b-b.mean())*w)
    R=np.conj(A)*B; R/=np.abs(R)+1e-9; r=np.real(np.fft.ifft2(R))
    dy,dx=np.unravel_index(r.argmax(),r.shape)
    if dy>a.shape[0]//2: dy-=a.shape[0]
    if dx>a.shape[1]//2: dx-=a.shape[1]
    print(f, 'dx',dx,'dy',dy,'peak',round(r.max(),3),'mean diff',round(abs(a-b).mean(),2))
