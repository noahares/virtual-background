# Virtual Background

Create a virtual background to spice up your online meetings.

Only works on Linux!

## Setup

Install
* opencv
* v4l2loopback-dkms

```
sudo modprobe -r v4l2loopback
sudo modprobe v4l2loopback devices=1 video_nr=20 card_label="v4l2loopback" exclusive_caps=1

pip install --user virtualenv
python -m venv
source venv/bin/activate
pip install -r requirements.txt

cd bodypix/
npm install
```

## Execute

First start node with `node bodypix/app.js` then start python with `python virtual_background.py`.

## Acknowledgment

Based on [this article](https://elder.dev/posts/open-source-virtual-background/)
