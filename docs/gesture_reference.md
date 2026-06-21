# Gesture & Configuration Reference

## Hand Landmarks

The system tracks 21 landmarks per hand using MediaPipe. Each landmark is identified by an index (0–20).

![Hand Landmarks](../assets/images/hand_landmarks.png)

The gesture engine relies on six key landmarks:

| Landmark | Index | Role in System | Marker Color |
|---|---|---|---|
| Thumb Tip | 4 | Move mode trigger (paired with index PIP) | Green |
| Index Finger PIP | 6 | Move mode trigger (paired with thumb tip) | Green |
| Index Finger Tip | 8 | Right click trigger, drag anchor | Red |
| Middle Finger Tip | 12 | Left click trigger, drag anchor | Red |
| Ring Finger Tip | 16 | Scroll mode trigger | Blue |
| Pinky Tip | 20 | Screenshot trigger, action guard | Pink |

## Gesture Guide

### Move Pointer
- **How**: Bring THUMB_TIP (4) and INDEX_FINGER_PIP (6) together (the two green dots). Point your index finger in the direction you want the cursor to move.
- **Visual cue**: Two green dots merge; display shows "Move Pointer" in green.

### Right Click
- **How**: Put INDEX_FINGER_TIP (8) down then up. Works just like a physical mouse — can double click by tapping quickly.
- **Visual cue**: Display shows "Right Click" in red.

### Left Click
- **How**: Put MIDDLE_FINGER_TIP (12) down then up to perform a left click.
- **Visual cue**: Display shows "Left Click" in red.

### Scroll Mode
Enter scroll mode by closing RING_FINGER_TIP (16) down:

- **Scroll Down**: With ring finger (16) down, put INDEX_FINGER_TIP (8) down.
- **Scroll Up**: With ring finger (16) down, put MIDDLE_FINGER_TIP (12) down (index finger up).
- **Visual cue**: Display shows "Scroll Up" or "Scroll Down" in blue.

### Drag & Drop
- **How**: Pinch INDEX_FINGER_TIP (8) and MIDDLE_FINGER_TIP (12) together sideways — like pinching between the two tips. Move your hand to drag. Separate the tips apart to drop.
- **Visual cue**: Display shows "Drag and Drop" in red.

### Screenshot
- **How**: Close all fingers into a fist (all landmarks down), then open your hand. The screenshot is captured on the fist-close, and the flag resets when you open.
- **Saved to**: `Screenshots/screenshot_DDMMYYYY_HHMMSS.png`

## Configuration Reference

All parameters are defined in `src/config.py`:

| Parameter | Default | Description |
|---|---|---|
| `WIN_W` | 640 | Camera capture window width (px) |
| `WIN_H` | 512 | Camera capture window height (px) |
| `CAM_ID` | 0 | Camera device index |
| `SINGLE_MONITOR` | True | Restrict cursor to a single monitor |
| `MONITOR_NUMBER` | 1 | Which monitor to target (1-indexed) |
| `SMOOTH_FACT` | 1 | Cursor smoothing factor (higher = faster response, more jitter) |
| `DEAD_ZONE` | 10 | Minimum pixel movement required to update cursor position |
| `BOUND_R` | 120 | Screen boundary reduction (px) — reduces usable camera area to prevent edge jitter |
| `CLICK_WAIT_TIME` | 0.3 | Cooldown between consecutive clicks (seconds) |
| `ACTION_DURATION` | 0.2 | Time to keep action label displayed (seconds) |
| `SCROLL_LINES` | 1 | Number of lines to scroll per gesture |
| `MARKER_RADIUS` | 5 | Radius of landmark markers on the display (px) |
| `DETECT_CONF` | 0.7 | MediaPipe hand detection confidence threshold |
| `TRACK_CONF` | 0.7 | MediaPipe hand tracking confidence threshold |
