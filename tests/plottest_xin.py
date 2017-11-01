import numpy as np
import matplotlib.pyplot as plt
import astropy.io.ascii as ascii


data = ascii.read('test.dat')
pyout = ascii.read('test.pyout')
# idlout = ascii.read('test.idlout')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(data['x'], data['y'], c='k')
ax.errorbar(data['x'], data['y'], xerr=data['xsig'], yerr=data['ysig'], ls=' ', c='k')

# Fix the plot boundaries and then plot the true line
xlim = ax.get_xlim()
ax.set_xlim(xlim)
ylim = ax.get_ylim()
ax.set_ylim(ylim)
truex = np.array(xlim)
truey = 4.0 + 3.0*truex
ax.plot(truex, truey, c='k', lw=2)

# Plot samples of the regression line
# samplex = truex
# for i in xrange(0, len(pyout), len(pyout)/50):
#     sampley = pyout[i]['alpha'] + pyout[i]['beta'] * samplex
#     ax.plot(samplex, sampley, c='b', alpha=0.1)

#<<160928>> plot 1-sigma confidence region! TODO: can encapsulate this into a subroutine!
newx = np.linspace(xlim[0], xlim[1], 50)    # NOTE: nelem of newx cannot be small!
allsampley = newx.copy()
for ii in xrange(len(pyout)):
    allsampley = np.vstack((allsampley, np.polyval([pyout[ii]['beta'], pyout[ii]['alpha']], newx)))
    # allsampley = np.vstack((allsampley, np.polyval([pyout[ii]['beta'], pyout[ii]['alpha']], newx)
    #                         +np.random.normal(loc=0., scale=pyout[ii]['sigsqr'])))
    # NOTE: after adding the int scatter, uncert on slope/intercept becomes vague
allsampley = np.delete(allsampley, 0, 0)
y_1sigma = np.percentile(allsampley, [16,84], axis=0)
y_low = y_1sigma[0,:]
y_up  = y_1sigma[1,:]
ax.fill_between(newx, y_low, y_up, alpha=0.3, facecolor='grey', edgecolor='grey', linewidth=0.0)

# for i in xrange(0, len(pyout), len(pyout)/50):
#     sampley = idlout[i]['alpha'] + idlout[i]['beta'] * samplex
#     ax.plot(samplex, sampley, c='r', alpha=0.1)

plt.show()
