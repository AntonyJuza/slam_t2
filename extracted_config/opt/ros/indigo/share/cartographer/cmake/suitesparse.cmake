

SET(SUITESPARSE_INCLUDE_DIRS
${KEENON_CROSS_DEPS_DIRS}/include/suitesparse	
)

SET(SUITESPARSE_LIBRARY_DIRS 
${KEENON_CROSS_DEPS_DIRS}/lib
)

SET(SUITESPARSE_LIBRARIES
amd
btf 
camd 
ccolamd 
cholmod 
colamd 
cxsparse 
klu 
umfpack 
spqr
)

include_directories(${SUITESPARSE_INCLUDE_DIRS})
link_directories(${SUITESPARSE_LIBRARY_DIRS})
