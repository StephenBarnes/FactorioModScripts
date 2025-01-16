#!/bin/bash

# Given some GIMP xcf files, creates PNGs of them scaled to 64x64 with 4 mipmaps.

for f in "$@"; do
  base="${f%.xcf}"
  out="${base}.png"

  gimp -i \
       -b "(begin
            (define (xcf2png-batch in-file out-file)
              (let* (
                 (image (car (gimp-file-load RUN-NONINTERACTIVE in-file in-file)))
                 ;; merge all visible layers
                 (merged (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE)))
                 (w (car (gimp-image-width image)))
                 (h (car (gimp-image-height image)))
                 (factor (/ 64.0 (max w h)))
                 (neww (round (* w factor)))
                 (newh (round (* h factor))))
                (gimp-image-scale image neww newh)
                (gimp-image-resize image 64 64 0 0)
                (gimp-layer-set-offsets merged
                                        (round (/ (- 64 neww) 2))
                                        (round (/ (- 64 newh) 2)))
                (file-png-save
                  RUN-NONINTERACTIVE
                  image
                  merged
                  out-file
                  out-file
                  0  ; interlace
                  9  ; compression
                  0  ; bkgd
                  0  ; gamma
                  0  ; save layer offset
                  0  ; save color values from transparent pixels
                  0)
                (gimp-image-delete image)))
            (xcf2png-batch \"$f\" \"$out\")
          )" \
       -b "(gimp-quit 0)"

  # Now do your mipmaps:
  convert "$out" -resize 64x64  "${base}-mipmap-1.png"
  convert "$out" -resize 32x32  "${base}-mipmap-2.png"
  convert "$out" -resize 16x16  "${base}-mipmap-3.png"
  convert "$out" -resize 8x8    "${base}-mipmap-4.png"
  convert -background transparent \
          "${base}-mipmap-1.png" \
          "${base}-mipmap-2.png" \
          "${base}-mipmap-3.png" \
          "${base}-mipmap-4.png" +append "${base}-mipmaps.png"
  rm "${base}-mipmap-"?.png
  rm "${base}.png"
  mv "${base}-mipmaps.png" "${base}.png"

done
