#! /usr/bin/env python


SLICE = 0
vars  = 'bx','by','bz'
param_file = 'param_particls01'
file_number = 40
centered = 'point' # or 'cell'
####################################################################################################

import sys
if centered.lower()<>'cell' and centered.lower()<>'point': 
    sys.exit("Grid centered-ness must be either 'cell' or 'point'!")

log_file   = 'movie.log.%003d' % file_number

import p3d
from numpy import linspace,hstack

Nx,Ny,Nz,lx,ly,lz = p3d.read_param_file(param_file)

sliced_v=[]
for var in vars:
    movie_file = 'movie.%s.%003d' % (var,file_number)
    ntimes,bytedata = p3d.read_movie_file(movie_file,Nx,Ny,Nz)
    lims = p3d.read_lims(log_file,ntimes,SLICE)
    sliced = p3d.get_time_slice(bytedata,Nx,Ny,Nz,SLICE)
# note scaling
    sliced = lims[var][0]+sliced/255.*( lims[var][1]-lims[var][0] )

    sliced_v.append(sliced)

# coordinates
x = linspace(-lx/2,lx/2,Nx+1)
y = linspace(-ly/2,ly/2,Ny+1)
z = linspace(-lz/2,lz/2,Nz+1)

# cell centers
xmid = 0.5*(x[1:]+x[:-1])
ymid = 0.5*(y[1:]+y[:-1])
zmid = 0.5*(z[1:]+z[:-1])


### VTK STUFF ###

import vtk

xpoints=vtk.vtkFloatArray()
ypoints=vtk.vtkFloatArray()
zpoints=vtk.vtkFloatArray()

xpoints.SetNumberOfComponents(1)
ypoints.SetNumberOfComponents(1)
zpoints.SetNumberOfComponents(1)

grid=vtk.vtkRectilinearGrid()

if centered=='point':
    xpoints.SetNumberOfTuples(Nx)
    for i in xrange(Nx): xpoints.SetTuple1(i,xmid[i])

    ypoints.SetNumberOfTuples(Ny)
    for i in xrange(Ny): ypoints.SetTuple1(i,ymid[i])

    zpoints.SetNumberOfTuples(Nz)
    for i in xrange(Nz): zpoints.SetTuple1(i,zmid[i])

    # Grid vertices are the centers of the cells of the original grid
    grid.SetDimensions(Nx,Ny,Nz)

else:
    xpoints.SetNumberOfTuples(Nx+1)
    for i in xrange(Nx+1): xpoints.SetTuple1(i,x[i])

    ypoints.SetNumberOfTuples(Ny+1)
    for i in xrange(Ny+1): ypoints.SetTuple1(i,y[i])

    zpoints.SetNumberOfTuples(Nz+1)
    for i in xrange(Nz+1): zpoints.SetTuple1(i,z[i])

    # Grid vertices are the vertices of the cells of the original grid
    grid.SetDimensions(Nx+1,Ny+1,Nz+1)

    
grid.SetXCoordinates(xpoints)
grid.SetYCoordinates(ypoints)
grid.SetZCoordinates(zpoints)

vtkVar=vtk.vtkFloatArray()
vtkVar.SetNumberOfComponents(3)
vtkVar.SetNumberOfTuples(Nx*Ny*Nz)

for i in xrange(Nx):
    for j in xrange(Ny):
        for k in xrange(Nz):
            offset = k*Nx*Ny+j*Nx+i
            vtkVar.InsertTuple3(offset,sliced_v[0][k,j,i],sliced_v[1][k,j,i],sliced_v[2][k,j,i])

vtkVar.SetName(''.join(vars))
if centered=='point':
    grid.GetPointData().AddArray(vtkVar)
else:
    grid.GetCellData().AddArray(vtkVar)


#grid.GetPointData().SetScalars(vtkVar)


#grid = vtk.vtkStructuredGrid()
#sg = vtk.vtkXMLStructuredGridWriter()

# WRITING FILES
import os,os.path

outdir = movie_file.split('.')[0]+'.'+movie_file.split('.')[2]+'.vtk'
if not os.path.exists(outdir): os.mkdir(outdir)
if not os.path.exists(outdir+'/'+centered+'_centered'): 
    os.mkdir(outdir+'/'+centered+'_centered')

outvardir = outdir + '/'+centered+'_centered/'+''.join(vars)
if not os.path.exists(outvardir): os.mkdir(outvardir)
outfile    = outvardir+'/'+movie_file.split('.')[0]+'.'+''.join(vars)+'.'+movie_file.split('.')[2]+'.vtk'

sg=vtk.vtkXMLPRectilinearGridWriter()
sg.SetFileName(outfile)
sg.SetInput(grid)
sg.SetDataModeToBinary()
sg.Write()
