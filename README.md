# PCA4CD - PCA for change detection #

The PCA4CD is a Qgis plugin to build the change detection layer using the principal components method. Designed mainly with the goal of:

1. generate or load the principal components (PCA)
2. and build the change detection layer based on the dimensionality reduction properties.

## Documentation

Home page documentation: [https://smbyc.bitbucket.io/qgisplugins/pca4cd](https://smbyc.bitbucket.io/qgisplugins/pca4cd)

## Installation

The plugin can be installed using the QGIS Plugin Manager, go into Qgis to `Plugins` menu and `Manage and install plugins`, in `All` section search for `PCA4CD`.

The plugin will be available in the `Plugins` menu and `Plugins toolbar`.

### Additional Python packages

PCA4CD requires additional Python packages to function, that are generally not part of QGIS's Python. These are:

* Python-Dask
* PyQtGraph

The way for have that: First way (recommended and automatic) is that the plugin (when is installing or updating) will be installed into a separate folder specific to PCA4CD and will not influence any existing Python installation. Second, install it in your system python installation first before install the plugin, but depends of the operating system to work.

## Source code

The official version control system repository of the plugin:
[https://github.com/SMByC/PCA4CD](https://github.com/SMByC/PCA4CD)

The home plugin in plugins.qgis.org: [http://plugins.qgis.org/plugins/PCA4CD/](http://plugins.qgis.org/plugins/PCA4CD/)

## Issue Tracker

Issues, ideas and enhancements: [https://github.com/SMByC/PCA4CD/issues](https://github.com/SMByC/PCA4CD/issues)

## About us

PCA4CD was developing, designed and implemented by the Group of Forest and Carbon Monitoring System (SMByC), operated by the Institute of Hydrology, Meteorology and Environmental Studies (IDEAM) - Colombia.

Author and developer: *Xavier Corredor Ll.*  
Theoretical support, tester and product verification: SMByC-PDI group

### Contact

Xavier Corredor Ll.: *xcorredorl (a) ideam.gov.co*  
SMByC: *smbyc (a) ideam.gov.co*

## License

PCA4CD is a free/libre software and is licensed under the GNU General Public License.
