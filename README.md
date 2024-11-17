# plotly_map

## Description:
Demo use of plotly mapping capabilities using "offline" resources.  On NGGN, plotly will access topojson files hosted by plotly; which clearly does not work when using on an air-gapped network.

Files are held resident in the '/assets' folder.  

Mapping scripts work with deals-tornado and do not require other packages.  

Dash provides server for dashboard/display--http://localhost:<port number specified in script run>