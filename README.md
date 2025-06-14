# Raspi-Baby-Mobile

A Raspberry Pi–powered system that brings interactivity to a baby mobile.

![](./doc/baby_yaw_mobile_rotation.svg)

It visually detects yaw movement of the head and translates it to a proportional rotation of a visual display.

## Background

Young infants quickly learn that their own actions can make things happen around them - a phenomenon known as **response-contingent learning**.

In [Rovee-Collier’s (1969)](https://www.sciencedirect.com/science/article/abs/pii/0022096569900253)
classic experiment,
babies as young as two months had one leg connected to an overhead mobile via a ribbon.
Whenever the infant kicked that leg, the mobile moved.
Even at this early age,
infants learned the contingency between their action and the mobile’s motion.

Building on this idea, [Watson and Ramey (1972)](https://psycnet.apa.org/record/1973-28652-001)
placed two-month-old babies on pressure-sensitive pillows wired to a rotating array of colored shapes.
The infants quickly adjusted their posture to keep the display turning,
again demonstrating an emerging sense of agency.

Crucially, contingent feedback elicited longer looking times as well as clear signs of positive affect such as smiling, cooing, and vocalizing.
In contrast, identical but non-contingent movements held little interest.
