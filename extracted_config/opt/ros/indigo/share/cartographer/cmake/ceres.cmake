

SET(CERES_INCLUDE_DIRS
${KEENON_CROSS_DEPS_DIRS}/local/include/ceres
)

SET(CERES_LIBRARY_DIRS
${KEENON_CROSS_DEPS_DIRS}/lib
)

SET(CERES_LIBRARIES
    libceres.a
)

include_directories(${CERES_INCLUDE_DIRS})
link_directories(${CERES_LIBRARY_DIRS})

