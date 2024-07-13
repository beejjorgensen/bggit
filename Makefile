PACKAGE=bggit
BGBSPD_BUILD_DIR?=../bgbspd

WEB_IMAGES=$(wildcard src/*.svg src/*.png)

include $(BGBSPD_BUILD_DIR)/main.make
