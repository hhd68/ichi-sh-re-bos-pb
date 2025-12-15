# New UI Layout - Visual Reference

## Before vs After

### BEFORE (Old Checklist)
```
┌────────────────────────────────┐
│ □ HTF TF Align (---)           │
│ □ LTF TK Cross (---)           │
│ □ LTF ADX > 22.0 (---)         │
│ □ LTF RSI < 30 or > 70 (---)   │
│ □ DECISION:  [BUY] [SELL]      │
│                                 │
│ □ LIMIT order mode              │
│ □ Show SL/TP preview            │
│                                 │
│ SL: 1.08450                     │  ← REMOVED
│ TP1: 1.08650                    │  ← REMOVED
│ TP2: 1.08750                    │  ← REMOVED
│ TP3: 1.09200                    │  ← REMOVED
│ R:R = 1:6                       │  ← REMOVED
│                                 │
│ [  ENTRY  ] [ CLOSE ALL ]       │
│ Status: Ready                   │
│ Daily loss: $xxx                │
└────────────────────────────────┘
```

### AFTER (New Checklist)
```
┌────────────────────────────────┐
│ TF: LTF=M5 | MTF=M15 | HTF=H1  │  ← NEW!
│                                 │
│ □ HTF: Bias (BUY)               │  ← NEW!
│ □ MTF: SH (BUY)                 │  ← NEW!
│ □ MTF: RE (BUY)                 │  ← NEW!
│ □ LTF: BOS (BUY)                │  ← NEW!
│ □ LTF: PB (BUY)                 │  ← NEW!
│ □ DECISION:  [BUY] [SELL]       │  ← KEPT
│                                 │
│ □ LIMIT order mode              │  ← KEPT
│ □ Show SL/TP preview            │  ← KEPT
│                                 │
│ [  ENTRY  ] [ CLOSE ALL ]       │  ← KEPT
│ Status: Ready                   │  ← KEPT
│ Daily loss: $xxx                │  ← KEPT
└────────────────────────────────┘
```

## Zone Visualization on Charts

### MTF Chart (e.g., M15)
```
Price
  ↑
  │     ┌──────────────┐ ← ZONE_SH (Blue/Red)
  │     │  SH Zone     │   High = max sweep highs
  │     │              │   Low = swing high level
  │     │   RE✓        │ ← LABEL_RE_OK (Green)
  │     └──────────────┘
  │          ╱╲
  │         ╱  ╲  Fake breakout
  │        ╱    ╲
  │       ╱      ╲
  │      ╱        ╲
  │     ╱          ╲ Return
  │    ╱            ╲
  └────────────────────→ Time
```

### LTF Chart (e.g., M5)
```
Price
  ↑
  │     Break of Structure
  │           ↓
  │     ┌──────────┐ ← ZONE_BOS (Gold)
  │     │ BOS Zone │   High = HH from bars 2-6
  │     │          │   Low = LL from bars 2-6
  │     │   PB✓    │ ← LABEL_PB_OK (Green)
  │     └──────────┘
  │         ↓
  │      Pullback retests zone
  └────────────────────→ Time
```

## SL Calculation Visualization

### BUY Signal
```
Price
  ↑
  │
  │   Entry ────────────o
  │                     │
  │   SH Zone High ─────┤
  │   SH Zone Low ──────┤
  │                     │ k * ATR_LTF
  │   SL ───────────────x ← SL = SH_low - k*ATR
  │
  └────────────────────────→ Time

Formula: SL = 1.08500 - (0.3 × 0.00167) = 1.08449
```

### SELL Signal
```
Price
  ↑
  │
  │   SL ───────────────x ← SL = SH_high + k*ATR
  │                     │ k * ATR_LTF
  │   SH Zone High ─────┤
  │   SH Zone Low ──────┤
  │                     │
  │   Entry ────────────o
  │
  └────────────────────────→ Time

Formula: SL = 1.08750 + (0.3 × 0.00167) = 1.08801
```

## Debug Log Flow Example

### Successful Signal Scan
```
[SCAN] Starting signal scan for EURUSD: LTF=M5, MTF=M15, HTF=H1

[BIAS] Checking HTF=PERIOD_H1 for EURUSD
[BIAS] ✓ BUY bias confirmed on PERIOD_H1

[SH] Checking MTF=PERIOD_M15, direction=BUY
[SH] ✓ BUY SH found: High=1.08750, Low=1.08500

[RE] Checking MTF=PERIOD_M15, direction=BUY, zone Low=1.08500 High=1.08750
[RE] ✓ BUY RE validated

[BOS] Checking LTF=PERIOD_M5, direction=BUY
[BOS] ✓ BUY BOS confirmed: Close[1]=1.08600 > HH=1.08550

[PB] Checking LTF=PERIOD_M5, direction=BUY, BOS zone Low=1.08300 High=1.08550
[PB] ✓ BUY PB detected

[ZONE] Drew ZONE_SH: High=1.08750, Low=1.08500 on TF=PERIOD_M15
[ZONE] Drew ZONE_BOS: High=1.08550, Low=1.08300 on TF=PERIOD_M5

[SCAN] ✓✓✓ ALL CHECKS PASSED! Final decision: BUY

[SL] ✓ NEW SIGNAL SL: SL=1.08449 (SH_zone=1.08500-1.08750, k=0.30, ATR=0.00167), TP1=1.08784, R=0.00134
```

### Failed Signal Scan (Stops at RE)
```
[SCAN] Starting signal scan for GBPUSD: LTF=M5, MTF=M15, HTF=H1

[BIAS] Checking HTF=PERIOD_H1 for GBPUSD
[BIAS] ✓ BUY bias confirmed on PERIOD_H1

[SH] Checking MTF=PERIOD_M15, direction=BUY
[SH] ✓ BUY SH found: High=1.25800, Low=1.25600

[RE] Checking MTF=PERIOD_M15, direction=BUY, zone Low=1.25600 High=1.25800
[RE] ✗ BUY RE failed: close[2]=1.25550 < zone.low=1.25600

→ Scan stopped, no signal generated
```

## Color Coding Reference

| Element        | BUY Color       | SELL Color      | Neutral     |
|----------------|-----------------|-----------------|-------------|
| Checklist text | Green (clrGreen)| Red (clrRed)    | Gray        |
| SH Zone        | Blue (clrDodgerBlue) | Red (clrCrimson) | -      |
| BOS Zone       | Gold (clrGold)  | Gold (clrGold)  | -           |
| RE/PB Markers  | Green (clrLime) | Green (clrLime) | -           |
| TF Info        | -               | -               | Dark Gray   |

## Input Parameters

### New Parameter
```mql5
input double InpSL_NewSignal_ATRMultiplier = 0.3;
// (New) SL multiplier for new signal (k: 0.2-0.5)
// SL = SH_zone ± k*ATR_LTF

Range: 0.2 to 0.5
- 0.2 = Tighter SL (higher risk of stop out)
- 0.3 = Balanced (recommended)
- 0.5 = Wider SL (more room, lower R:R)
```

### Existing Parameters (Still Used)
```mql5
input bool InpEnableDebugPrints = true;
// BẬT/TẮT: In log chi tiết để debug

Recommendation: 
- true during testing to see full flow
- false in production to reduce log spam
```

## Quick Test Procedure

1. **Compile**
   ```
   MetaEditor → Open .mq5 → Press F7
   ```

2. **Attach to Chart**
   ```
   MT5 → M5 chart → Drag EA from Navigator
   ```

3. **Enable Debug**
   ```
   EA Settings → InpEnableDebugPrints = true → OK
   ```

4. **Watch for Signal**
   ```
   Checklist UI updates automatically
   Zones appear when conditions met
   Expert log shows detailed flow
   ```

5. **Verify**
   - [ ] TF info shows at top
   - [ ] 6 rows display (Bias, SH, RE, BOS, PB, DECISION)
   - [ ] No SL/TP/RR labels in checklist
   - [ ] Zones appear on charts when signal active
   - [ ] Debug logs show in Expert tab
   - [ ] SL uses new formula when signal fires

---

**Visual Reference Created**: 2025-12-15  
**All enhancements implemented**: Commit 47f1d36
