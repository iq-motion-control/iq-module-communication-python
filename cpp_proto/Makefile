# make file made by RAPHAEL VAN HOFFELEN, inspired by JOB VRANISH
 #https://spin.atomicobject.com/2016/08/26/makefile-c-projects/


TARGET_EXEC ?= run

BUILD_DIR ?= ./build
SRC_DIRS ?= ./src
INC ?= ./inc

SRCS := $(shell find $(SRC_DIRS) -name *.cpp -or -name *.c -or -name *.s)
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(INC) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))
CC = g++
CXX = g++
DEBUG = -g
C_INC_FLAGS ?= $(INC_FLAGS) -MMD -MP
CFLAGS = -Wall  -std=c++11  $(DEBUG)
CXXFLAGS = -Wall  -std=c++11  $(DEBUG)

$(TARGET_EXEC): $(OBJS)
	$(CC) $(OBJS) -o $@ $(LDFLAGS)


# c source
$(BUILD_DIR)/%.c.o: %.c
	$(MKDIR_P) $(dir $@)
	$(CC) $(C_INC_FLAGS) $(CFLAGS) -c $< -o $@

# c++ source
$(BUILD_DIR)/%.cpp.o: %.cpp
	$(MKDIR_P) $(dir $@)
	$(CXX) $(C_INC_FLAGS) $(CXXFLAGS) -c $< -o $@ 



.PHONY: clean

clean:
	$(RM) $(TARGET_EXEC) $(OBJS) $(DEPS) -r $(BUILD_DIR)

-include $(DEPS)

MKDIR_P ?= mkdir -p