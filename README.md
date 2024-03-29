# RAGE

PSG player for Shadertoy. AY register data from RAGE by X-Trade (RAGE_2.pt2 by LAV).

Still unfinished, needs better data compression and proper envelopes for the bass line.


## HTML5 version

* https://joric.github.io/rage (uses [ayumi-js](https://github.com/alexanderk23/ayumi-js))

## Shadertoy version

* https://www.shadertoy.com/view/ltKcWz (warning - slow preloading, see Sound tab for details)

The graphic shader is essentially one line of GLSL:

```GLSL
void mainImage(out vec4 O, vec2 U) {
    U += U - iResolution.xy;
    O = vec4(int(iTime - atan(U.y, U.x) * 8. / 6.28 + 8.) / ivec4(2, 4, 1, 1) % 2);
}
```

The sound shader is a little bit more complicated.

### How it works

Shadertoy uses a large pregenerated texture to play the sound (every sample is a pixel,
the texture is about 5 minutes total). AY data is essentially an AY register dump (PSG).
Every streaming multiprocessor in glsl needs to parse the AY data according to the timestamp, so
I tried to compress that data, but LZ or LZ4 has backreferences and RLE was too large so I ended
with a simple branching in the GLSL code (still needs a little bit of optimizing).

### HLSL

Just for fun, the same shader for MPC-HC (sadly, it's video only, doesn't work for audio), add that to pre-resize:

```hlsl
#define clock (p0[3])
float4 p0 : register(c0);

float4 main(float2 tex: TEXCOORD0): COLOR {
	float2 U = tex * p0.xy;
	U += U - p0.xy;
	return int(clock - atan2(U.x, U.y) * 8. / 6.28 + 8.) / int4(2, 4, 1, 1) % 2;
}
```

## References

* https://github.com/true-grue/ayumi
* https://github.com/alexanderk23/ayumi-js
* https://www.shadertoy.com/view/ltKcWz
