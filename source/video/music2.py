import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
import wave

SR = 44100
DUR = 27.9
N = int(SR * DUR)
rng = np.random.default_rng(11)

# three buses: melodic (gets sidechain pumping), drums, fx
MEL = np.zeros((2, N)); DRM = np.zeros((2, N)); FX = np.zeros((2, N))
SC = np.ones(N)  # sidechain gain curve driven by the kick

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def add(bus, sig, t0, g=1.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= N or t0 < 0: return
    s = sig[: N - i] * g
    bus[0, i:i+len(s)] += s * np.sqrt(0.5*(1-pan)); bus[1, i:i+len(s)] += s * np.sqrt(0.5*(1+pan))

# ---------- tempo grid: 150 BPM, beat 0 is the first flash at 8.4 s ----------
BEAT = 0.4; G0 = 8.4
def T(beat): return G0 + beat * BEAT          # beat may be fractional / negative

# ---------- instruments ----------
def square_like(f, t, bright=6):
    s = np.zeros_like(t)
    for k in range(1, 2*bright, 2): s += np.sin(2*np.pi*f*k*t) / k
    return s
def pluck(m, dur=0.22, vel=1.0, bright=2500):
    n = int((dur + 0.3) * SR); t = np.arange(n)/SR; f = hz(m)
    s = square_like(f, t, 5) * 0.6 + np.sin(2*np.pi*2*f*t) * 0.3
    s = lp(s, bright)
    e = (1 - np.exp(-t/0.002)) * np.exp(-t/max(0.08, dur*0.5))
    return s * e * vel * 0.16
def lead(m, dur, vel=1.0):
    n = int((dur + 0.25) * SR); t = np.arange(n)/SR
    # cute "blip": slides up a semitone into the note, light vibrato after
    pitch = hz(m) * 2 ** ((-1*np.exp(-t/0.025) + 0.012*np.sin(2*np.pi*6*t)*np.clip(t/0.25-0.4, 0, 1)) / 12)
    ph = 2*np.pi*np.cumsum(pitch)/SR
    s = np.sin(ph) * 0.7 + np.sin(2*ph) * 0.25 + np.sin(3*ph) * 0.12
    e = (1 - np.exp(-t/0.004)) * np.exp(-t/0.6) * np.clip((dur + 0.25 - t)/0.25, 0, 1)
    return s * e * vel * 0.20
def bell(m, vel=1.0, d=0.9):
    n = int(2.0 * SR); t = np.arange(n)/SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.3) + 0.25*np.sin(2*np.pi*4.02*f*t)*np.exp(-t/0.12)
    return s * (1 - np.exp(-t/0.001)) * np.exp(-t/d) * vel * 0.12
def chord_pad(ms, dur, vel=1.0, cutoff=3200):
    n = int((dur + 0.3) * SR); t = np.arange(n)/SR; s = np.zeros(n)
    for m in ms:
        for det in (-0.12, -0.04, 0.05, 0.13):
            f = hz(m + det); ph = rng.random()*6.28
            for k in range(1, 8): s += np.sin(2*np.pi*f*k*t + ph*k) / k
    s = lp(s, cutoff)
    e = np.clip(t/0.01, 0, 1) * np.clip((dur + 0.3 - t)/0.3, 0, 1)
    return s * e * vel * 0.0042
def bass(m, dur, vel=1.0):
    n = int((dur + 0.05) * SR); t = np.arange(n)/SR; f = hz(m)
    s = np.sin(2*np.pi*f*t) + 0.35*lp(square_like(f, t, 4), 900)
    e = np.clip(t/0.004, 0, 1) * np.clip((dur + 0.05 - t)/0.05, 0, 1) * np.exp(-t/0.5)
    return s * e * vel * 0.30
def kick(vel=1.0):
    n = int(0.35*SR); t = np.arange(n)/SR
    f = 50 + 130*np.exp(-t/0.03)
    s = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.13)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t/0.004) * 0.3
    return (s + click) * vel * 0.85
def clap(vel=1.0):
    n = int(0.3*SR); t = np.arange(n)/SR; s = np.zeros(n)
    for k, d in enumerate((0, 0.009, 0.018)):
        i = int(d*SR); nz = rng.standard_normal(n - i)
        s[i:] += nz * np.exp(-np.arange(n-i)/SR/(0.012 if k < 2 else 0.11))
    s = sosfilt(butter(2, [900, 7000], 'band', fs=SR, output='sos'), s)
    return s * vel * 0.38
def hat(vel=1.0):
    n = int(0.07*SR); t = np.arange(n)/SR
    return hp(rng.standard_normal(n), 8000) * np.exp(-t/0.02) * vel * 0.16
def snap(vel=1.0):
    n = int(0.12*SR); t = np.arange(n)/SR
    return sosfilt(butter(2, [1500, 5000], 'band', fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t/0.03) * vel * 0.3
def bloop(up=True, vel=1.0):
    n = int(0.22*SR); t = np.arange(n)/SR
    f = (500 + 900*(t/0.22)) if up else (1300 - 900*(t/0.22))
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t/0.08) * vel * 0.2
def riser(dur, vel=1.0):
    n = int(dur*SR); t = np.arange(n)/SR
    nz = rng.standard_normal(n); out = np.zeros(n); seg = int(0.04*SR)
    for i in range(0, n, seg):
        fc = 600 + 9000*(i/n)**2
        b = sosfilt(butter(2, [fc*0.7, min(fc*1.4, 19000)], 'band', fs=SR, output='sos'), nz[i:i+seg+500])
        out[i:i+seg] += b[:len(out[i:i+seg])]
    tone = np.sin(2*np.pi*np.cumsum(300*2**(2.5*t/dur))/SR) * 0.12
    return (out*0.5 + tone) * (t/dur)**2 * vel * 0.5
def crash(vel=1.0):
    n = int(1.8*SR); t = np.arange(n)/SR
    return hp(rng.standard_normal(n), 5000) * np.exp(-t/0.6) * vel * 0.14
def sub_drop(vel=1.0):
    n = int(1.0*SR); t = np.arange(n)/SR
    return np.sin(2*np.pi*np.cumsum(30 + 60*np.exp(-t/0.15))/SR) * np.exp(-t/0.45) * vel * 0.5

# ---------- harmony: C major, | F | G | Em | Am |, one chord per bar (4 beats) ----------
PROG = [([65, 69, 72, 76], 41), ([67, 71, 74, 77], 43), ([64, 67, 71, 74], 40), ([69, 72, 76, 79], 45)]
def chord_at(beat): return PROG[int(np.floor(beat / 4)) % 4]

# hook: 2 bars = 8 beats, (beat offset, midi, length in beats); C pentatonic, bouncy
HOOK = [(0, 76, .5), (.5, 79, .5), (1, 81, .5), (1.5, 79, .5), (2.5, 76, .5), (3, 74, .5), (3.5, 72, .5),
        (4, 74, .5), (4.5, 76, .5), (5, 79, 1), (6, 76, .5), (6.5, 74, .5), (7, 72, 1)]
HOOK_B = [(0, 81, .5), (.5, 84, .5), (1, 81, .5), (1.5, 79, .5), (2.5, 76, .5), (3, 79, .5), (3.5, 81, .5),
          (4, 84, .5), (4.5, 86, .5), (5, 84, 1), (6, 81, .5), (6.5, 79, .5), (7, 84, 1)]

def sidechain(beat, depth=0.6):
    i = int(T(beat)*SR); n = int(0.36*SR); t = np.arange(n)/SR
    g = 1 - depth*np.exp(-t/0.09)
    j = min(N, i+n)
    if i < N: SC[i:j] = np.minimum(SC[i:j], g[:j-i])

def section(b0, b1, kick_on=True, claps=True, hats=True, hook=None, plucks=True, bass_on=True, pad=True, half=False, bright=2800):
    for b in np.arange(b0, b1):
        t = T(b); notes, root = chord_at(b); pos = b % 4
        if kick_on and (not half or pos in (0,)) :
            add(DRM, kick(1.0 if pos == 0 else 0.85), t); sidechain(b)
        if claps and pos in (1, 3): add(DRM, clap(0.9), t, 1.0, 0.05)
        if half and claps and pos == 2: add(DRM, clap(0.9), t)
        if hats:
            add(DRM, hat(0.9), t + BEAT/2, 1.0, 0.35); add(DRM, hat(0.45), t, 1.0, -0.3)
        if pos == 0 and pad: add(MEL, chord_pad(notes, 4*BEAT - 0.05, 1.0, bright), t)
        if bass_on:
            for e8 in range(2):
                m = root if (e8 == 0 or pos % 2 == 0) else root + 12
                add(MEL, bass(m, BEAT/2 - 0.03, 0.9 if e8 == 0 else 0.7), t + e8*BEAT/2)
        if plucks:  # bouncy arpeggio in eighths
            arp = notes + [notes[1] + 12]
            for e8 in range(2):
                k = int((b * 2 + e8)) % len(arp)
                add(MEL, pluck(arp[k] + 12, 0.18, 0.75 if e8 else 0.9, bright), t + e8*BEAT/2, 1.0, (-0.4, 0.4)[e8])
    if hook is not None:
        for start in np.arange(b0, b1, 8):
            for off, m, ln in hook:
                if start + off < b1: add(MEL, lead(m, ln*BEAT*0.9, 1.0), T(start + off), 1.0, 0.0)

# ---------- arrangement (beats relative to 8.4 s; 1 beat = 0.4 s) ----------
# 0.0 to 2.6 s (beats -21 to -14.5): dark scene, a music box playing the hook softly, muffled
for off, m, ln in [h for h in HOOK if h[0] < 6.5]:
    tb = -21 + off
    add(MEL, bell(m + 12, 0.55, 0.7), T(tb), 1.0, 0.2)
add(MEL, chord_pad([60, 64, 67, 72], 2.6, 0.45, 900), 0.0)
add(FX, riser(0.9, 0.6), 1.7)
add(FX, bloop(True, 0.8), 2.5)

# 2.6 s: colour arrives, light bouncy groove (typing), from the "and" of beat -14.5
add(FX, crash(0.6), T(-14.5)); add(MEL, chord_pad(PROG[0][0], 1.4, 1.0, 3000), T(-14.5))
section(-14, -6, kick_on=True, half=True, claps=True, hats=True, plucks=True, bass_on=True, pad=True, bright=2600)
# 5.2 s onward (beat -8): "Finding something calm", the beat kicks in and builds
section(-6, 0, kick_on=True, claps=True, hats=True, plucks=True, bass_on=True, pad=True, bright=2600)
for k in range(8):   # snare/clap roll into the drop
    add(DRM, snap(0.4 + 0.08*k), T(-2 + k*0.25))
add(FX, riser(1.6, 1.0), T(-4))

# 8.4 s DROP: showreel, full chorus with the hook
add(FX, crash(1.0), T(0)); add(FX, sub_drop(1.0), T(0)); add(FX, bloop(True), T(0), 0.8, 0.3)
section(0, 8, hook=HOOK, bright=3200)
# 11.6 s: darker scene, half-time bounce, hook B on bells
add(FX, crash(0.6), T(8)); add(FX, bloop(False, 0.7), T(8))
section(8, 16, half=True, hats=True, plucks=True, bright=2200)
for off, m, ln in HOOK_B: add(MEL, bell(m, 0.8, 0.6), T(8 + off), 1.0, -0.2)
# 14.8 s: bright again, full chorus with the higher hook
add(FX, crash(1.0), T(16)); add(FX, sub_drop(0.7), T(16))
section(16, 24, hook=HOOK_B, bright=3400)
add(FX, riser(1.0, 0.8), T(21.5))
# 18.0 s flash: the mood card, lighter verse while stress turns to calm
add(FX, crash(0.9), T(24)); add(FX, bloop(True), T(24), 0.9)
section(24, 34, kick_on=True, claps=True, hats=False, plucks=True, bass_on=True, pad=True, bright=2600)
for off, m, ln in HOOK: add(MEL, bell(m + 12, 0.5, 0.6), T(26 + off), 1.0, 0.25)
add(FX, riser(1.2, 0.8), T(33))
# 22.8 s end card "ta-da": big chord, sparkle run, then a soft bouncy outro that fades
add(FX, crash(1.0), T(36)); add(FX, sub_drop(0.8), T(36))
add(MEL, chord_pad([60, 64, 67, 72, 76], 2.5, 1.4, 4000), T(36))
for k, m in enumerate([72, 76, 79, 84, 88, 91, 96]):
    add(MEL, bell(m, 0.9 - 0.06*k, 1.2), T(36) + k*0.06, 1.0, -0.6 + k*0.2)
section(38, 48, kick_on=False, claps=False, hats=True, plucks=True, bass_on=False, pad=False, bright=2400)
for off, m, ln in HOOK[:7]: add(MEL, bell(m + 12, 0.45, 0.8), T(40 + off), 1.0, 0.2)
add(MEL, chord_pad([60, 64, 67, 72], 3.6, 0.8, 2500), T(42))

# ---------- mix ----------
MEL *= SC
def reverb(x, secs=1.6, decay=0.45, mix=0.25):
    n = int(secs*SR); t = np.arange(n)/SR
    out = []
    for ch in range(2):
        ir = lp(rng.standard_normal(n) * np.exp(-t/decay), 6000)
        w = fftconvolve(x[ch], ir)[:N]; out.append(w)
    w = np.stack(out); w /= np.max(np.abs(w)) + 1e-9
    return w * mix * np.max(np.abs(x))
mel = MEL + reverb(MEL, mix=0.35)
fx = FX + reverb(FX, mix=0.3)
out = mel * 1.0 + DRM * 0.9 + fx * 0.8
out = np.stack([hp(c, 30) for c in out])
tt = np.arange(N)/SR
out *= np.clip(tt/0.05, 0, 1) * np.clip((DUR - tt)/2.2, 0, 1)
out /= np.max(np.abs(out)) + 1e-9
out = np.tanh(out * 1.25) / np.tanh(1.25)                 # glue / loudness
out *= 0.89 / np.max(np.abs(out))
pcm = (out.T * 32767).astype(np.int16)
with wave.open('/home/claude/vid2/ending-music2.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok')
