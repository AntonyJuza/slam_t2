

SET(LUA_INCLUDE_DIR
${KEENON_CROSS_DEPS_DIRS}/include
${KEENON_CROSS_DEPS_DIRS}/include/lua5.2
${KEENON_CROSS_DEPS_DIRS}/include/arm-linux-gnueabihf
)

SET(LUA_LIBRARY_DIRS
${KEENON_CROSS_DEPS_DIRS}/lib/arm-linux-gnueabihf
)

SET(LUA_LIBRARIES
liblua5.2.so
)


include_directories(${LUA_INCLUDE_DIR})
link_directories(${LUA_LIBRARY_DIRS})
