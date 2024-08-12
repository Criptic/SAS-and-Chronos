# SAS-and-Chronos

This repository serves as a companion piece to SAS Community Library article.

It demontrates a deployment strategy for the Chronos model family developed by Amazon Science - which you can find here: https://github.com/amazon-science/chronos-forecasting.

**Citation:**
```
@article{ansari2024chronos,
  author  = {Ansari, Abdul Fatir and Stella, Lorenzo and Turkmen, Caner and Zhang, Xiyuan and Mercado, Pedro and Shen, Huibin and Shchur, Oleksandr and Rangapuram, Syama Syndar and Pineda Arango, Sebastian and Kapoor, Shubham and Zschiegner, Jasper and Maddix, Danielle C. and Wang, Hao and Mahoney, Michael W. and Torkkola, Kari and Gordon Wilson, Andrew and Bohlke-Schneider, Michael and Wang, Yuyang},
  title   = {Chronos: Learning the Language of Time Series},
  journal = {arXiv preprint arXiv:2403.07815},
  year    = {2024}
}
```

## Deployment

Check the chronos-deploy.yaml on a sample deployment yaml for kubernetes, note that variables are marked as _${name}_ within the file.