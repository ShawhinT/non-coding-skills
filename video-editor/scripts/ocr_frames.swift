// ocr_frames — Apple Vision OCR for redaction discovery and verification.
//
// Build once (macOS, no deps):   swiftc -O ocr_frames.swift -o ocr_frames
// Line mode  (batch, cached):    ./ocr_frames <out_dir> frame1.png frame2.png ...
//     writes <out_dir>/<frame>.json = [{"t","x0","y0","x1","y1"}, ...]   (skips frames already done)
// Word mode  (one image, stdout): ./ocr_frames --words crop.png
//     prints [{"t","x0","y0","x1","y1","words":[{"t","x0","y0","x1","y1"}, ...]}, ...]
//
// Coordinates are pixels of the given image, origin top-left. Language correction is off
// so names and emails come back as seen rather than "fixed" into dictionary words.
// Word mode is most accurate on a 3× upscaled crop of one line (see references/redaction.md).
import Foundation
import Vision
import AppKit

func recognize(_ cg: CGImage) -> [VNRecognizedTextObservation] {
  let req = VNRecognizeTextRequest()
  req.recognitionLevel = .accurate
  req.usesLanguageCorrection = false
  try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
  return req.results ?? []
}
func load(_ path: String) -> CGImage? {
  guard let img = NSImage(contentsOf: URL(fileURLWithPath: path)) else { return nil }
  return img.cgImage(forProposedRect: nil, context: nil, hints: nil)
}
func px(_ b: CGRect, _ W: Double, _ H: Double) -> [String: Any] {
  ["x0": Int(b.minX * W), "y0": Int((1 - b.maxY) * H), "x1": Int(b.maxX * W), "y1": Int((1 - b.minY) * H)]
}

let args = CommandLine.arguments
if args.count >= 3 && args[1] == "--words" {
  guard let cg = load(args[2]) else { print("[]"); exit(0) }
  let W = Double(cg.width), H = Double(cg.height)
  var arr: [[String: Any]] = []
  for o in recognize(cg) {
    guard let c = o.topCandidates(1).first else { continue }
    var line = px(o.boundingBox, W, H); line["t"] = c.string
    var words: [[String: Any]] = []
    let s = c.string
    s.enumerateSubstrings(in: s.startIndex..<s.endIndex, options: .byWords) { sub, r, _, _ in
      if let sub = sub, let bo = try? c.boundingBox(for: r) {
        var w = px(bo.boundingBox, W, H); w["t"] = sub; words.append(w)
      }
    }
    line["words"] = words
    arr.append(line)
  }
  print(String(data: try! JSONSerialization.data(withJSONObject: arr), encoding: .utf8)!)
  exit(0)
}

guard args.count >= 3 else {
  FileHandle.standardError.write("usage: ocr_frames <out_dir> img...  |  ocr_frames --words img\n".data(using: .utf8)!)
  exit(1)
}
let outDir = args[1]
for path in args.dropFirst(2) {
  let url = URL(fileURLWithPath: path)
  let outPath = outDir + "/" + url.deletingPathExtension().lastPathComponent + ".json"
  if FileManager.default.fileExists(atPath: outPath) { continue }
  guard let cg = load(path) else { continue }
  let W = Double(cg.width), H = Double(cg.height)
  var arr: [[String: Any]] = []
  for o in recognize(cg) {
    guard let c = o.topCandidates(1).first else { continue }
    var d = px(o.boundingBox, W, H); d["t"] = c.string
    arr.append(d)
  }
  try! JSONSerialization.data(withJSONObject: arr).write(to: URL(fileURLWithPath: outPath))
}
