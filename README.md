# Interactive Design System for Textile Graphic Pattern Generation in Vector format
This repository contains code and materials for the paper _Interactive Design System for Textile Graphic Pattern Generation in Vector format_, contributed by Hong QU, Honghong He, K. P. Chau, and P. Y. Mok*. All rights reserved by authors.

-----
## Introduction
This study proposes an intelligent system for interactive vector pattern generation to address the labor-intensive process of creating scalable and production-ready patterns in the fashion and textile industries. The system integrates an Interactive Genetic Algorithm (IGA) for layout generation and a colorization mechanism guided by reference images, enabling users to produce editable and aesthetically pleasing patterns efficiently. It also recommends Pantone TPX codes to streamline production workflows. Experimental results demonstrate the system’s ability to generate high-quality vector patterns in under a second, meeting industry standards for usability, efficiency, and human aesthetics. A survey with fashion professionals confirmed its practicality and potential for design support. While the system depends on high-quality reference images, future improvements will focus on enhancing pattern diversity and accessibility for non-expert users. This study offers a practical tool for automated vector pattern design, contributing to the advancement of computer-aided design in the fashion industry.

![The method pipeline.](assets/framework.png)

## Application demo
Moreover, we provide an interactive tool that allowsusers to efficiently extract and manipulate editable design elements with just a few clicks. The tool enables users to adjust the similarity threshold, which determines the number of extracted editable design elements.

Below, we demonstrate the results generated with different threshold values:

<p align="center">
  <img src="assets/thhre_1.gif" alt="Demo: Set threshold to 0.55" style="height: 260px; margin-right: 10px;" />
  <img src="assets/thhre_4.gif" alt="Demo: Set threshold to 0.85" style="height: 260px;" />
</p>


## Installation
- Install [Potrace](https://potrace.sourceforge.net/). Follow its official manual.
- Please see the _requirements.txt_
  
