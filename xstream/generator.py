#!/usr/bin/env python
# -*- coding: utf-8 -*-

# #########################################################################
# Copyright (c) 2016, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2016. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################


__author__ = "Doga Gursoy"
__contact__ = "dgursoy@aps.anl.gov"
__copyright__ = "Copyright (c) 2016, UChicago Argonne, LLC."
__license__ = "BSD-3"
__version__ = "0.1.0"
__status__ = "Development"
__docformat__ = "restructuredtext en"
__all__ = []


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import numpy as np

logger = logging.getLogger(__name__)


def project(x0, y0, x1, y1, obj):
	""" Project single x-ray beam.
	"""

    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
    sx, sy = obj.shape

    # grid frame (gx, gy)
    gx = np.arange(0, sx + 1)
    gy = np.arange(0, sy + 1)

    # avoid upper-right boundary errors
    if (x1 - x0) == 0:
        x0 += 1e-6
    if (y1 - y0) == 0:
        y0 += 1e-6

    # vector lengths (ax, ay)
    ax = (gx - x0) / (x1 - x0)
    ay = (gy - y0) / (y1 - y0)

    # edges of alpha (a0, a1)
    ax0 = min(ax[0], ax[-1])
    ax1 = max(ax[0], ax[-1])
    ay0 = min(ay[0], ay[-1])
    ay1 = max(ay[0], ay[-1])
    a0 = max(max(ax0, ay0), 0)
    a1 = min(min(ax1, ay1), 1)

    # sorted alpha vector
    cx = (ax >= a0) & (ax <= a1)
    cy = (ay >= a0) & (ay <= a1)
    alpha = np.sort(np.r_[ax[cx], ay[cy]])

    # lengths
    xv = x0 + alpha * (x1 - x0)
    yv = y0 + alpha * (y1 - y0)
    lx = np.ediff1d(xv)
    ly = np.ediff1d(yv)
    dist = np.sqrt(lx**2 + ly**2)
    ind = dist != 0

    # indexing
    mid = alpha[:-1] + np.ediff1d(alpha) / 2.
    xm = x0 + mid * (x1 - x0)
    ym = y0 + mid * (y1 - y0)
    ix = np.floor(xm).astype('int')
    iy = np.floor(ym).astype('int')

    # projection
    return np.dot(dist[ind], obj[ix[ind], iy[ind]])
