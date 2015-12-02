# Blender to Poppy Torso Synchronizer

## What is it ?
This project enable an animator to animate a robot in Blender (here the Poppy Torso) and see directly the motion rendered on the real robot.

## Installing

#### Create a directory for the project and enter it:
```shell
mkdir BlenderPoppy
cd BlenderPoppy
```

#### Download and extract Blender 2.74:

```shell
wget http://ftp.halifax.rwth-aachen.de/blender/release/Blender2.74/blender-2.74-linux-glibc211-x86_64.tar.bz2
tar xf blender-2.74-linux-glibc211-x86_64.tar.bz2
rm blender-2.74-linux-glibc211-x86_64.tar.bz2
mv blender-2.74-linux-glibc211-x86_64 ./Blender274
```

#### Install virtualenv from Ubuntu repositories:

```shell
sudo apt-get install python-virtualenv
```

#### Create a virtual environment at the root of the BlenderPoppy repository, then activate it

```shell
virtualenv -p /usr/bin/python3.4 virtualenv
source ./virtualenv/bin/activate
```

#### Install BLAS and LAPACK libraries and Fortran compiler from Ubuntu repositories (needed to compile scipy, a pypot dependency):

```shell
sudo apt-get install libblas-dev liblapack-dev gfortran
pip install pypot
pip install zmq
```
