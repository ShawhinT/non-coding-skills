#!/usr/bin/env python3
"""Recreated-slides layout: spine = camera (audio; picture hidden underneath),
lane 1 = full-frame slides track, lane 2 = rounded camera inset (alpha clip).
Both overlays are rendered on the raw-camera timeline starting at TRACK_T0
(render_slides_track.py prints it), so overlay_source_time = camera_source_time - TRACK_T0.
See references/recreated-slides.md.

Usage: make_slides_inset_fcpxml.py edl.json --slides slides_track.mp4 \
    --inset camera_inset.mov --track-t0 599.9994 -o edit.fcpxml --project-name NAME \
    [--inset-x 801 --inset-y 336 --inset-scale 0.3333]
"""
import argparse, json, os, subprocess
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote
from xml.dom import minidom

def probe(p):
    s = json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height,r_frame_rate","-of","json",p],capture_output=True,text=True,check=True).stdout)["streams"][0]
    n,d = (int(x) for x in s["r_frame_rate"].split("/"))
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p]).decode())
    return {"w":int(s["width"]),"h":int(s["height"]),"num":n,"den":d,"dur":dur}

ap = argparse.ArgumentParser()
ap.add_argument("edl"); ap.add_argument("--slides",required=True); ap.add_argument("--inset",required=True)
ap.add_argument("--track-t0",type=float,required=True); ap.add_argument("-o",required=True); ap.add_argument("--project-name",required=True)
ap.add_argument("--inset-scale",type=float,default=1/3)   # relative to FCP 'fit' conform (720->1080 tall)
# inset position in pixels on a 1080p canvas, center origin, +y up
ap.add_argument("--inset-x",type=float,default=801); ap.add_argument("--inset-y",type=float,default=336)
a = ap.parse_args()
SEQ_H = 1080   # sequence is 1920x1080; inset px args are on this canvas

edl = json.load(open(a.edl)); cam_file = edl["source_file"]; segs = edl["segments"]
cam, sld, ins = probe(cam_file), probe(a.slides), probe(a.inset)
fd = Fraction(cam["den"], cam["num"])
def q(t):  # seconds -> frame-aligned rational string
    f = round(Fraction(t).limit_denominator(10**9)/fd)*fd; return f"{f.numerator}/{f.denominator}s"
url = lambda p: "file://"+quote(os.path.abspath(p), safe="/:")
fdur = f"{cam['den']}/{cam['num']}s"

root = ET.Element("fcpxml", version="1.11"); res = ET.SubElement(root,"resources")
ET.SubElement(res,"format",id="r1",name="FFVideoFormat1080p2997",width="1920",height="1080",frameDuration=fdur)
for fid,m in (("f_cam",cam),("f_sld",sld),("f_ins",ins)):
    ET.SubElement(res,"format",id=fid,width=str(m["w"]),height=str(m["h"]),frameDuration=fdur)
def asset(id_,path,fmt,m,audio):
    kw = dict(hasAudio="1",audioSources="1",audioChannels="2",audioRate="48000") if audio else dict(hasAudio="0")
    el = ET.SubElement(res,"asset",id=id_,name=Path(path).stem,start="0s",duration=q(m["dur"]),format=fmt,hasVideo="1",videoSources="1",**kw)
    ET.SubElement(el,"media-rep",kind="original-media",src=url(path))
asset("r_cam",cam_file,"f_cam",cam,True); asset("r_sld",a.slides,"f_sld",sld,False); asset("r_ins",a.inset,"f_ins",ins,False)

ev = ET.SubElement(ET.SubElement(root,"library"),"event",name=a.project_name)
proj = ET.SubElement(ev,"project",name=a.project_name)
seq = ET.SubElement(proj,"sequence",format="r1",tcStart="0s",tcFormat="NDF",audioLayout="stereo",audioRate="48k")
spine = ET.SubElement(seq,"spine")
off = Fraction(0)
for i,s in enumerate(segs):
    nfr = round(Fraction(s["end"]-s["start"]).limit_denominator(10**9)/fd); dur = nfr*fd
    ds = f"{dur.numerator}/{dur.denominator}s"
    clip = ET.SubElement(spine,"asset-clip",ref="r_cam",name=f"Seg {i+1}",offset=(f"{off.numerator}/{off.denominator}s" if off else "0s"),
                         start=q(s["start"]),duration=ds,tcFormat="NDF")
    o_in = s["start"]-a.track_t0
    assert 0 <= o_in and o_in+float(dur) <= min(sld["dur"],ins["dur"])+0.05, (i,s)
    ET.SubElement(clip,"asset-clip",ref="r_sld",lane="1",name="Slides",offset=q(s["start"]),start=q(o_in),duration=ds)
    ic = ET.SubElement(clip,"asset-clip",ref="r_ins",lane="2",name="Camera inset",offset=q(s["start"]),start=q(o_in),duration=ds)
    # FCPXML position units = % of frame height (1080px -> 100), not pixels
    ET.SubElement(ic,"adjust-transform",position=f"{a.inset_x*100/SEQ_H:.4f} {a.inset_y*100/SEQ_H:.4f}",scale=f"{a.inset_scale:.4f} {a.inset_scale:.4f}")
    off += dur
seq.set("duration",f"{off.numerator}/{off.denominator}s")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n'+ET.tostring(root,encoding="unicode")
pretty = "\n".join(l for l in minidom.parseString(xml).toprettyxml(indent="  ").split("\n") if l.strip())
pretty = pretty.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>',1)
Path(a.o).write_text(pretty+"\n")
print(json.dumps({"fcpxml":a.o,"n_clips":len(segs),"timeline_min":round(float(off)/60,2)}))
