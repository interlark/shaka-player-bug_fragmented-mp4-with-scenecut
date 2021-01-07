## How to reproduce the bug:
1) Encode video stream with scenecut parameter (you can run build_demo.py or use already built one)
2) Open the stream with Firefox browser and Shaka player (you can open 3 demo links shown below)
![Image of Links](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/links.png)
3) Play video and seek through given places by clicking links shown below, you'll notice video glitches (on Windows) or video freezing while audo is playing (on Linux)
![Image of Seeks](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/seeks.png)

## Zoom in
Let's see some places closer on example of BBB.

![Image of Zoom in Legend](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_legend.png)

### Point 176.17
#### With scenecut
![Image of Zoom in 1-S](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_1_scenecut.png)
#### Without scenecut
![Image of Zoom in 1-NS](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_1_no-scenecut.png)

### Point 322.21
#### With scenecut
![Image of Zoom in 1-S](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_2_scenecut.png)
#### Without scenecut
![Image of Zoom in 1-NS](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_2_no-scenecut.png)

### Point 270.38
#### With scenecut
![Image of Zoom in 1-S](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_3_scenecut.png)
#### Without scenecut
![Image of Zoom in 1-NS](https://raw.githubusercontent.com/interlark/shaka-player-bug_fragmented-mp4-with-scenecut/master/images/an_3_no-scenecut.png)

## Conclusion
Somehow Shaka player skips I-frames what make a decoder missing back references for next frames which cause visual glitches on Windows (when decoder tries to rebuild B\P frames) and freezes on Linux (when decoders just wait for another I\IDR frames)

## Demo
Check the demo on https://interlark.github.io/shaka-player-bug_fragmented-mp4-with-scenecut with Firefox browser.

## Screencast
https://youtu.be/P_aWcyjM8bM
