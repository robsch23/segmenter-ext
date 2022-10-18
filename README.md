## SEGMENTER-EXT

#### The Segmenter is an extension for <a href="https://loko-ai.com/" target="_blank">LoKo-AI</a>

---
**_Abstract_**

<p>
Segmentation is the technique used to process and analyze digital images and 
allows you to divide an image into parts or regions, often based on the 
characteristics of the pixels.

There are several approaches to segmentation:
* With reference to pixels we speak of semantic segmentation: objects 
classified with the same pixel values are segmented with the same color maps

* Search for patterns in the pixels that make up an image

* and more ...
</p>

---
**_Description_**

The **Segmenter** component, in particular, is developed on two different 
kinds of segmentation, which are:

1. ### SEGMENT

This type of segmentation allows, for example, to segment documents in which it is 
not possible to find a clear pattern, so by choosing some parameters of the computer
vision Segment algorithm it is possible to obtain blocks from the document parse.

2. ### SEARCH BOX

<p>Computer vision's SearchBox algorithm is useful for searching for recurring patterns
in the picture, such as:</p>

1. [ ] Checkbox
2. [ ] Box
3. [ ] Form

