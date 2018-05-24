# Forced alignment

This repository allows for quick deployment of forced alignment algorithms. Currently, the only supported algorithm is [FAVE-align](https://github.com/JoFrhwld/FAVE/tree/master/FAVE-align).

## HTK

Please note that the forced alignment algorithms make use of the [Hidden Markov Model Toolkit (HTK)](http://htk.eng.cam.ac.uk/). HTK is made available free of charge and can be downloaded from the website mentioned above. However it may not be redistributed, and you must register at the website.

That being said, we do not explicitly redistribute the HTK source code here, but make use of a [Docker Hub image](https://hub.docker.com/r/armariya/htk-ubuntu/) that contains the source code. 