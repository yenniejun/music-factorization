# Scale Factorization

## Basic Music Theory
In modern music theory, there are twelve chromatic (semi-tone) notes in one octave. This octave can be split evenly (that is, symmetrically), in several ways.
* Octave - an interval of 12 semi-tones. This is basically the same note, this is a 1-note scale
* Tritone - an interval of 6 semi-tones. There are 6 tritones
* Augmented - an interval of 4 semi-tones. There are 4 augmented scales
* Diminished - an interval of 3 semi-tones. There are 3 diminished scales
* Whole Tone - an interval of 2 semi-tones. There are 2 whole tone scales
* Chromatic - an interval of 1 semi-tone. There is 1 chromatic scale
* Unison - an interval of 0 semi-tones. More of a base-case scenario

## What This Project Does
I wanted to write something that "factorized"  scales into parts that could be understood with combinations of the above "symmetric" scales. For example, the scale
`A B C D E G A`
can be understood as a combination of two 3-note segements of the whole tone scale (`C D E` and `G A B`). It can also be understood as a combination of one 2-note segment of the tritone scale (`E G`) and two 2-note segments of the whole tone scale(`A B`, `C, D`).

## Tests
I have some rudimentary unit tests that tests each function. Eventually, would like to add mock and test some more scenarios.
You can run these simply with `python3 tests.py`

## Future
This is just the basic vision of what I want to achieve. Eventually I would like to add the UI element of showing how one scale can be split into different components in different ways, and of letting the user input their specified scale.