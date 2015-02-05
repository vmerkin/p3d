import sys

####################################################################################################
def get_time_slice(bytearr,Nx,Ny,Nz,time_slice):
    from numpy import array,reshape

#            data = zeros(Nx,Ny,Nz,dtype=float)
    Npoints = Nx*Ny*Nz
    data = array(bytearr[time_slice*Npoints:(time_slice+1)*Npoints],dtype=float)
    return(data.reshape(Nz,Ny,Nx))

####################################################################################################
def read_movie_file(moviefile,Nx,Ny,Nz):
    try:
        with open(moviefile) as f: bytearr = bytearray(f.read())
        if len(bytearr) % (Nx*Ny*Nz) <> 0:
            sys.exit('Something is wrong. The number of bytes in the movie file is not divisible by Nx*Ny*Nz.')
        else:
            ntimes = len(bytearr)/(Nx*Ny*Nz)
            return(ntimes,bytearr)
    except IOError:
        print("Can't open movie file '" + moviefile+"'")

####################################################################################################
def read_param_file(paramfile):
    try:
        with open(paramfile) as pf: params = pf.readlines()

        for paramline in params:
            if paramline.startswith('#define pex '): pex = int(paramline.split()[2])
            if paramline.startswith('#define pey '): pey = int(paramline.split()[2])
            if paramline.startswith('#define pez '): pez = int(paramline.split()[2])
            if paramline.startswith('#define nx '):  nx  = int(paramline.split()[2])
            if paramline.startswith('#define ny '):  ny  = int(paramline.split()[2])
            if paramline.startswith('#define nz '):  nz  = int(paramline.split()[2])
            if paramline.startswith('#define lx '):  lx  = float(paramline.split()[2])
            if paramline.startswith('#define ly '):  ly  = float(paramline.split()[2])
            if paramline.startswith('#define lz '):  lz  = float(paramline.split()[2])

        print("Parameters read:\n Nx = %d\n Ny = %d\n Nz = %d\n lx = %.1f\n ly = %.1f\n lz = %.1f\n" % (pex*nx,pey*ny,pez*nz,lx,ly,lz) )
        return(pex*nx,pey*ny,pez*nz,lx,ly,lz)

    except IOError:
        print("Can't open parameter file '"+paramfile+"'")

####################################################################################################
def read_lims(logfile,ntimes,time_slice):
    from numpy import array
    try:
        with open(logfile) as f: lims = f.readlines()
        if len(lims) % ntimes <> 0:
            sys.exit('Something is wrong. The number of lines in the log file is not divisible by Nx*Ny*Nz.')
        else:
            return{'rho':array(lims[0+time_slice*27][:-1].split(),dtype=float),
                   'jx':array(lims[1+time_slice*27][:-1].split(),dtype=float),
                   'jy':array(lims[2+time_slice*27][:-1].split(),dtype=float),
                   'jz':array(lims[3+time_slice*27][:-1].split(),dtype=float),
                   'bx':array(lims[4+time_slice*27][:-1].split(),dtype=float),
                   'by':array(lims[5+time_slice*27][:-1].split(),dtype=float),
                   'bz':array(lims[6+time_slice*27][:-1].split(),dtype=float),
                   'ex':array(lims[7+time_slice*27][:-1].split(),dtype=float),
                   'ey':array(lims[8+time_slice*27][:-1].split(),dtype=float),
                   'ez':array(lims[9+time_slice*27][:-1].split(),dtype=float),
                   'ni':array(lims[20+time_slice*27][:-1].split(),dtype=float),
                   'ne':array(lims[10+time_slice*27][:-1].split(),dtype=float),
                   'jex':array(lims[11+time_slice*27][:-1].split(),dtype=float),
                   'jey':array(lims[12+time_slice*27][:-1].split(),dtype=float),
                   'yez':array(lims[13+time_slice*27][:-1].split(),dtype=float),
                   'pexx':array(lims[14+time_slice*27][:-1].split(),dtype=float),
                   'peyy':array(lims[15+time_slice*27][:-1].split(),dtype=float),
                   'pezz':array(lims[16+time_slice*27][:-1].split(),dtype=float),
                   'pexy':array(lims[17+time_slice*27][:-1].split(),dtype=float),
                   'peyz':array(lims[18+time_slice*27][:-1].split(),dtype=float),
                   'pexz':array(lims[19+time_slice*27][:-1].split(),dtype=float),
                   'pixx':array(lims[21+time_slice*27][:-1].split(),dtype=float),
                   'piyy':array(lims[22+time_slice*27][:-1].split(),dtype=float),
                   'pizz':array(lims[23+time_slice*27][:-1].split(),dtype=float),
                   'pixy':array(lims[24+time_slice*27][:-1].split(),dtype=float),
                   'piyz':array(lims[25+time_slice*27][:-1].split(),dtype=float),
                   'pixz':array(lims[26+time_slice*27][:-1].split(),dtype=float),
                }
    except IOError:
        print("Can't open parameter file '"+logfile+"'")
