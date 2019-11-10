# RAGE

PSG player for Shadertoy. AY register data from RAGE by X-Trade (RAGE_2.pt2 by LAV).

Still unfinished, needs better data compression and proper envelopes for the bass line.


## HTML5 version

* https://joric.github.io/rage (uses [ayumi-js](https://github.com/alexanderk23/ayumi-js))

## Shadertoy version

* https://www.shadertoy.com/view/ltKcWz (warning - slow preloading, see Sound tab for details)

### How it works

Shadertoy uses a large pregenerated texture to play the sound (every sample is a pixel,
the texture is about 5 minutes total). AY data is essentially an AY register dump (PSG).
Every streaming multiprocessor in glsl needs to parse the AY data according to the timestamp, so
I tried to compress that data, but LZ or LZ4 has backreferences and RLE was too large so I ended
with a simple branching in the GLSL code (still needs a little bit of optimizing).

## References

* https://github.com/true-grue/ayumi
* https://github.com/alexanderk23/ayumi-js
* https://www.shadertoy.com/view/ltKcWz
