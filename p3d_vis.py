#! /usr/bin/env python


SLICE = 0
var   = 'ez'
param_file = 'param_particls01'
movie_file = 'movie.ez.015'
log_file   = 'movie.log.015'

xmin,xmax  = -20,2.5
ymin,ymax  = -5,5
zmin,zmax  = -2,2
####################################################################################################
import p3d
from numpy import linspace,hstack,meshgrid
from matplotlib import pyplot as pl
from matplotlib import cm


Nx,Ny,Nz,lx,ly,lz = p3d.read_param_file(param_file)
ntimes,bytedata = p3d.read_movie_file(movie_file,Nx,Ny,Nz)
lims = p3d.read_lims(log_file,ntimes,SLICE)
sliced = p3d.get_time_slice(bytedata,Nx,Ny,Nz,SLICE)
# note scaling
sliced = lims[var][0]+sliced/255.*( lims[var][1]-lims[var][0] )

# coordinates
x = linspace(-lx/2,lx/2,Nx)
y = linspace(-ly/2,ly/2,Ny)
z = linspace(-lz/2,lz/2,Nz)

# pad coords
xmid = 0.5*(x[1:]+x[:-1])
xmid = hstack( (2*xmid[0]-xmid[1],xmid,2*xmid[-1]-xmid[-2]) )

ymid = 0.5*(y[1:]+y[:-1])
ymid = hstack( (2*ymid[0]-ymid[1],ymid,2*ymid[-1]-ymid[-2]) )

zmid = 0.5*(z[1:]+z[:-1])
zmid = hstack( (2*zmid[0]-zmid[1],zmid,2*zmid[-1]-zmid[-2]) )

########### PAY ATTENTION HERE, WANT TO MOVE THIS TO THE TOP AND ASK USER FOR WHICH SLICE TO MAKE ###########
xind = (x<=xmax)&(x>=xmin)
yind = (y<=ymax)&(y>=ymin)
I,J  = meshgrid(xind,yind)
zind = 64
vmin = sliced[zind][I&J].min()
vmax = sliced[zind][I&J].max()
vmax = max( (abs(vmin),abs(vmax) ) )
vmin = -vmax
##############################################################################################################

ax = pl.subplot(111,aspect='equal')
p  = pl.pcolormesh(xmid,ymid,sliced[zind,:,:],vmin=vmin,vmax=vmax,cmap=cm.RdBu_r)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)
ax.set_title('min= %.1f, max= %.1f' % (vmin,vmax))
pl.colorbar(p,ax=ax).set_label(var)
pl.show()

