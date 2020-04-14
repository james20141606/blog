# 4.6
##continue trainig last week’s model

<img src="1.png" alt="drawing" style="width:400px;"/>

the loss decreases slowly, 60k iterations are enough for training DDSP autoencoder using SHTOOKA dataset.

---
correlation and stoi:

<img src="2.png" alt="drawing" style="width:400px;"/>

<img src="2_0.png" alt="drawing" style="width:400px;"/>

---
## latent feature extracted using DDSP ECoG encoder

<img src="3.png" alt="drawing" style="width:600px;"/>

---

## check again DDSP autoencoder’s restore operation

previously, the autoencoder has some problem to restore the weights, so modify some codes and change to the latest DDSP version, retrain two autoencoders (with z or without z)
the results are correct now

https://drive.google.com/open?id=1vDq2Qi-ArOvI7ahPBCB3oetGLoxViAwy
https://drive.google.com/open?id=11M0PU_5c5MlLDeVj7C8QzW0jfUgNJEda 

---
## add simple RNN to f0 and loudness encoding

and add similar strategy to loudness encoder did not improve the result (make it a little worse)
(1000,2,2,128)->reduce mean:(1000,128) ->GRU->(1000,256)->softplus and sum:(1000,1)

the author said that a simple RNN might be useful to f0 and loudness encoding *(You can also train small autoregressive models like a simple RNN, since the signal is much simpler than an audio waveform. )*
I tested it but did not work well. (**Might need more training**)

<img src="4.png" alt="drawing" style="width:300px;"/>

---

correlation and stoi:

<img src="5.png" alt="drawing" style="width:400px;"/>

<img src="5_0.png" alt="drawing" style="width:400px;"/>



---
## latent feature extracted using DDSP ECoG encoder

<img src="6.png" alt="drawing" style="width:500px;"/>

f0 feature is weird, it seems that RNN suppresses nearly all signals.

---

## allow multi gpu training
add multi gpu training codes to speed up the training a little bit (not very useful, maybe gradient transfer between different gpu is also time consuming)

---

## mask out reproduction period signal

original ECoG signal

<img src="7.png" alt="drawing" style="width:600px;"/>

<img src="8.png" alt="drawing" style="width:600px;"/>
---

## set signals outside perception region to be zero

<img src="9.png" alt="drawing" style="width:600px;"/>

<img src="10.png" alt="drawing" style="width:600px;"/>

maybe we should make it smoother at boundary?

---

## one sample example

<img src="11.png" alt="drawing" style="width:300px;"/>

---

## performance

<img src="14.png" alt="drawing" style="width:600px;"/>

(need more training? 
Training is slow, one day only 10,000 steps. Just fix entire model restore problem)

---

## mask out data training
(not use z latent, not use RNN in encoder)
- correlation is very poor

<img src="27.png" alt="drawing" style="width:400px;"/><img src="28.png" alt="drawing" style="width:250px;"/>

- reconstructed audio is weird


<img src="29.png" alt="drawing" style="width:400px;"/>  

---
<audio controls>
<source src="audio/gt.wav" type="audio/wav">
</audio>  

<audio controls>
<source src="audio/z_0_rnn_0.wav" 
type="audio/wav">
</audio>


---
## extracting latent feature from new ecog data using trained DDSP ecog autoencoder
 
<img src="30.png" alt="drawing" style="width:300px;"/><img src="13.png" alt="drawing" style="width:300px;"/>

- features from ecog encoder have some problems: loudness seems ok, but f0 might need more variation in silent period.
 

 
---
## other experiments using mask out data
- Similar bad results:
    - use z, not use RNN in encoder
    - use z, use RNN in encoder
- better result:
    - not use z, use RNN in encoder
(but the audio does not make sense, and it is not better than original ECoG data, not use z, not use RNN experiment)

<img src="19.png" alt="drawing" style="width:500px;"/>

<audio controls>
<source src="audio/gt.wav" type="audio/wav">
</audio>  

<audio controls>
<source src="audio/z_0_rnn_1.wav" 
type="audio/wav">
</audio>       
 
---
<img src="20.png" alt="drawing" style="width:400px;"/>

<img src="21.png" alt="drawing" style="width:400px;"/>

---
## extracted features comparison
<img src="22.png" alt="drawing" style="width:320px;"/><img src="13.png" alt="drawing" style="width:360px;"/>

- It seems the RNN encoder suppresses nearly all signals.
- But loudness features extraction seems really **good** if we use RNN encoder on mask out data.
- F0 features need more variance.

---
 
## TODO
- [ ] more training epochs for mask out data and RNN encoder
    - [ ] resume training using both encoder and decoder(still have to manually assign weights)
- [ ] other mask out strategy?
- [ ] analyze CREPEPRETRAINED embedding loss, why is it always 0
- [ ] how to better encode f0



---
## use z, add rnn, mask out


<img src="23.png" alt="drawing" style="width:500px;"/>    

<audio controls>
<source src="audio/gt.wav" type="audio/wav">
</audio>  

<audio controls>
<source src="audio/z_1_rnn_1.wav" 
type="audio/wav">
</audio>   
 
---
<img src="24.png" alt="drawing" style="width:400px;"/>

<img src="25.png" alt="drawing" style="width:400px;"/>

---
## extracted features comparison
<img src="26.png" alt="drawing" style="width:320px;"/><img src="13.png" alt="drawing" style="width:360px;"/>
---
## use z, not use rnn, mask out


<img src="15.png" alt="drawing" style="width:500px;"/>   

<audio controls>
<source src="audio/gt.wav" type="audio/wav">
</audio>  

<audio controls>
<source src="audio/z_1_rnn_0.wav" 
type="audio/wav">
</audio>    
 
---
<img src="16.png" alt="drawing" style="width:400px;"/>

<img src="17.png" alt="drawing" style="width:400px;"/>

---
## extracted features comparison
<img src="18.png" alt="drawing" style="width:320px;"/><img src="13.png" alt="drawing" style="width:360px;"/>


