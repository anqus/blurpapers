# Blurpapers

## Creating desktop wallpapers from photo albums.

Currently, Windows offers 6 options for fitting pictures as desktop wallpapers:

* Fill
* Fit
* Stretch
* Tile
* Span
* Centre

As photos are often not the same aspect ratio as a desktop monitor, none of these options are aesthetically pleasing. The first 5 options stretch, crop or repeat sections of the photo. The final option (centre) maintains the composition, but adds black bars around the perimeter. None of these options are great, [and can make a good photo look off](readme_screens/before.png "Before"). This becomes an even bigger problem if you want to use an album with photos of varying dimensions.

This repo aims to easily convert a directory of images to a directory of [prettier desktop wallpapers](readme_screens/after.png "After"). 

This code blurs and resizes the image, before pasting the original untrasnformed image, centered on top.

It will output wallpapers to the size of the primary monitor detected.