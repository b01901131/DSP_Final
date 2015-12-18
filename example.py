from features import mfcc
from features import logfbank
import scipy.io.wavfile as wav

(rate,sig) = wav.read("output.wav")
mfcc_feat = mfcc(sig,rate)
fbank_feat = logfbank(sig,rate)

print mfcc_feat[50]#[1:3,:]
