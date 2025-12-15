# Update Summary: Enhanced UI and Signal Logic

## Changes Implemented (Comment #3655808944)

### 1. ✅ Zone Drawing on Correct Timeframes

**Implementation:**
- Added `DrawZoneOnChart()` function to create rectangle objects on charts
- Added `UpdateZoneDisplays()` to refresh zones after each scan
- Zones are drawn on appropriate timeframes:
  - **SH Zone (MTF)**: Rectangle showing fake breakout zone
    - BUY: Blue (clrDodgerBlue)
    - SELL: Red (clrCrimson)
    - High = max sweep highs, Low = swing high level
  - **RE Marker (MTF)**: Green "RE✓" text label when zone is respected
  - **BOS Zone (LTF)**: Gold (clrGold) rectangle
    - Shows HH-LL range where structure was broken
  - **PB Marker (LTF)**: Green "PB✓" text label when pullback detected

**Objects Created:**
- `ZONE_SH` - SH rectangle on MTF
- `LABEL_RE_OK` - RE validation marker on MTF
- `ZONE_BOS` - BOS rectangle on LTF  
- `LABEL_PB_OK` - PB validation marker on LTF

### 2. ✅ Timeframe Display in Checklist

**Implementation:**
- Added `lbl_tf_info` label at top of checklist (above row 0)
- Displays: `"TF: LTF=xx | MTF=xx | HTF=xx"`
- Examples:
  - M5 chart: "TF: LTF=M5 | MTF=M15 | HTF=H1"
  - H1 chart: "TF: LTF=H1 | MTF=H4 | HTF=D1"
- Updates automatically on each signal scan
- Uses small font (8pt), dark gray color

**Global Variables Added:**
```mql5
ENUM_TIMEFRAMES g_current_ltf, g_current_mtf, g_current_htf;
string g_tf_display_string;
```

### 3. ✅ Removed SL/TP/RR Preview from Checklist

**Removed Elements:**
- `SL_preview` label
- `TP1_preview`, `TP2_preview`, `TP3_preview` labels
- `RR_label` (Risk:Reward display)

**Preserved Elements (unchanged):**
- ✓ Decision row with BUY/SELL buttons
- ✓ `chk_limit` / `lbl_limit` (Limit order mode checkbox)
- ✓ `chk_3` / `lbl_3` (SL/TP preview toggle)
- ✓ `entry_btn`, `close_btn` buttons
- ✓ `status_label` (Status: Ready)
- ✓ `daily_loss_note` (Daily loss remaining)
- ✓ All symbol list/dashboard panels

**New Checklist Structure:**
```
[Timeframe Info] TF: LTF=xx | MTF=xx | HTF=xx
☑ HTF: Bias (BUY/SELL/---)
☑ MTF: SH (BUY/SELL/---)
☑ MTF: RE (BUY/SELL/---)
☑ LTF: BOS (BUY/SELL/---)
☑ LTF: PB (BUY/SELL/---)
☑ DECISION: [BUY] [SELL]
[Everything below unchanged]
```

### 4. ✅ Signal Logic Synchronized

**Dashboard and Checklist Now Use:**
- Same `RunNewSignalScan()` function
- Same timeframe mapping
- Same Bias→SH→RE→BOS→PB flow
- Same state array: `g_new_signal_state[6]`

**Integration Points:**
1. `UpdateDecisionByAlignment()` - Called by OnTimer for checklist UI
2. `ConfirmSignalWithDecisionLogic()` - Called for dashboard/auto-trade
3. Both call `RunNewSignalScan()` which populates `g_new_signal_state[]`

### 5. ✅ New SL Formula Implemented

**New Input Parameter:**
```mql5
input double InpSL_NewSignal_ATRMultiplier = 0.3;  
// (New) SL multiplier for new signal (k: 0.2-0.5, SL = SH_zone ± k*ATR_LTF)
```

**Formula:**
- **BUY**: `SL = SH_zone.low - k * ATR(14, LTF)`
- **SELL**: `SL = SH_zone.high + k * ATR(14, LTF)`

**Implementation in `CalculateTradeLevels()`:**
- Checks if new signal is active: `g_new_signal_state[5] != 0`
- Validates SH zone exists: `g_sh_zone.high > 0 && g_sh_zone.low > 0`
- Calculates SL using formula above
- Adjusts for spread if `InpAddSpreadToSL` enabled
- Validates SL is on correct side of entry price
- Sets SL type as `"NewSignal(SH)"`
- Calculates TP levels: TP1=2R, TP2=3R, TP3=10R

**Fallback Behavior:**
- If new signal not active → uses existing Kumo/Swing/ATR logic
- Maintains backward compatibility with existing trades

### 6. ✅ Detailed Debug Logging

**All functions now log when `InpEnableDebugPrints = true`:**

**[BIAS] Logs:**
```
[BIAS] Checking HTF=PERIOD_H1 for EURUSD
[BIAS] ✓ BUY bias confirmed on PERIOD_H1
[BIAS] ✗ No bias on PERIOD_H1
```

**[SH] Logs:**
```
[SH] Checking MTF=PERIOD_M15, direction=BUY
[SH] ✓ BUY SH found: High=1.08750, Low=1.08500
```

**[RE] Logs:**
```
[RE] Checking MTF=PERIOD_M15, direction=BUY, zone Low=1.08500 High=1.08750
[RE] ✗ BUY RE failed: close[2]=1.08450 < zone.low=1.08500
```

**[BOS] Logs:**
```
[BOS] Checking LTF=PERIOD_M5, direction=BUY
```

**[PB] Logs:**
```
[PB] Checking LTF=PERIOD_M5, direction=BUY, BOS zone Low=1.08300 High=1.08550
```

**[SCAN] Logs:**
```
[SCAN] Starting signal scan for EURUSD: LTF=M5, MTF=M15, HTF=H1
[SCAN] ✓✓✓ ALL CHECKS PASSED! Final decision: BUY
```

**[ZONE] Logs:**
```
[ZONE] Drew ZONE_SH: High=1.08750, Low=1.08500 on TF=PERIOD_M15
```

**[SL] Logs:**
```
[SL] ✓ NEW SIGNAL SL: SL=1.08450 (SH_zone=1.08500-1.08750, k=0.30, ATR=0.00167), TP1=1.08784, R=0.00134
```

## Testing Checklist

### Visual Verification
- [ ] Compile EA in MetaEditor (F7)
- [ ] Attach to chart
- [ ] Verify timeframe info appears at top of checklist
- [ ] Check 6 rows display correctly (HTF:Bias, MTF:SH, MTF:RE, LTF:BOS, LTF:PB, DECISION)
- [ ] Confirm SL/TP/RR labels removed from checklist

### Zone Drawing
- [ ] Wait for/trigger a signal
- [ ] Verify SH zone appears on MTF chart (blue for BUY, red for SELL)
- [ ] Check BOS zone appears on LTF chart (gold)
- [ ] Confirm RE marker ("RE✓") appears when validated
- [ ] Confirm PB marker ("PB✓") appears when validated

### SL Calculation
- [ ] Enable debug prints: `InpEnableDebugPrints = true`
- [ ] Check logs show `[SL] ✓ NEW SIGNAL SL` when signal fires
- [ ] Verify SL distance from SH zone = k * ATR
- [ ] Adjust `InpSL_NewSignal_ATRMultiplier` (try 0.2, 0.3, 0.5)
- [ ] Confirm SL adjusts accordingly

### Signal Flow
- [ ] Enable debug prints
- [ ] Watch Expert log for [BIAS], [SH], [RE], [BOS], [PB] messages
- [ ] Verify scan stops at first failure
- [ ] Check [SCAN] logs show full flow when all pass

## Configuration

### Recommended Settings for Testing
```
InpEnableDebugPrints = true           // Enable detailed logging
InpSL_NewSignal_ATRMultiplier = 0.3   // k value (0.2-0.5)
```

### To Disable Zone Drawing
Set zones not to display by commenting out `UpdateZoneDisplays()` call in `RunNewSignalScan()`.

### To Revert to Old SL Logic
Set `InpSL_NewSignal_ATRMultiplier = 0` or comment out new SL section in `CalculateTradeLevels()`.

## Technical Notes

### Timeframe Mapping
| Chart TF | LTF (Chart) | MTF (Medium) | HTF (High) |
|----------|-------------|--------------|------------|
| M1       | M1          | M5           | M15        |
| M5       | M5          | M15          | H1         |
| M15      | M15         | H1           | H4         |
| H1       | H1          | H4           | D1         |
| H4       | H4          | D1           | W1         |
| D1       | D1          | W1           | MN1        |

### SL Calculation Priority
1. **NEW SIGNAL** (if active): Uses SH zone ± k*ATR
2. Kumo-based SL (with TP balance check)
3. Swing-based SL (with TP balance check)
4. Pure ATR-based SL (fallback)

### Zone Object Names
- `ZONE_SH` - Swing High zone rectangle
- `ZONE_BOS` - Break of Structure zone rectangle
- `LABEL_RE_OK` - Retest validation marker
- `LABEL_PB_OK` - Pullback validation marker
- `lbl_tf_info` - Timeframe display label

## Known Issues / Limitations

1. **Zone Persistence**: Zones are redrawn on each scan. Previous zones are cleared.
2. **Multi-Symbol**: Zones only drawn on current chart symbol.
3. **Historical**: Zones not drawn for past signals, only current/future.
4. **SL Formula**: Only applies to new entries after signal fires. Existing positions use original SL.

## Future Enhancements

Possible improvements for consideration:
- Option to persist historical zones
- Multi-chart zone display
- Zone alerts/notifications
- Adjustable zone colors
- Zone transparency settings

---

**Implementation Date**: 2025-12-15  
**Commit**: 6de2c1d  
**Files Modified**: HHD68_ICHIMOKU_v5.7-(MT5)adx,rsi.mq5  
**Status**: ✅ Complete and Ready for Testing
