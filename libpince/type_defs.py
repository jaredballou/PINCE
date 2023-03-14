# -*- coding: utf-8 -*-
"""
Copyright (C) 2016-2017 Korcan Karaokçu <korcankaraokcu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# IMPORTANT: Any constant involving only PINCE.py should be declared in PINCE.py

import collections.abc
import queue
import sys


class CONST_TIME:
    GDB_INPUT_SLEEP = sys.float_info.min


class PATHS:
    GDB_PATH = "/bin/gdb"


class IPC_PATHS:
    # Use SysUtils.get_PINCE_IPC_directory()
    PINCE_IPC_PATH = "/dev/shm/PINCE-connection/"
    # Use SysUtils.get_IPC_from_PINCE_file()
    IPC_FROM_PINCE_PATH = "/from_PINCE_file"
    IPC_TO_PINCE_PATH = "/to_PINCE_file"  # Use SysUtils.get_IPC_to_PINCE_file()


class USER_PATHS:
    # Use SysUtils.get_user_path() to make use of these

    CONFIG_PATH = ".config/"
    ROOT_PATH = CONFIG_PATH + "PINCE/PINCE_USER_FILES/"
    TRACE_INSTRUCTIONS_PATH = ROOT_PATH + "TraceInstructions/"
    CHEAT_TABLES_PATH = ROOT_PATH + "CheatTables/"
    GDBINIT_PATH = ROOT_PATH + "gdbinit"
    GDBINIT_AA_PATH = ROOT_PATH + "gdbinit_after_attach"
    PINCEINIT_PATH = ROOT_PATH + "pinceinit.py"
    PINCEINIT_AA_PATH = ROOT_PATH + "pinceinit_after_attach.py"

    @staticmethod
    def get_init_directories():
        return USER_PATHS.ROOT_PATH, USER_PATHS.TRACE_INSTRUCTIONS_PATH, USER_PATHS.CHEAT_TABLES_PATH

    @staticmethod
    def get_init_files():
        return USER_PATHS.GDBINIT_PATH, USER_PATHS.GDBINIT_AA_PATH, USER_PATHS.PINCEINIT_PATH, \
            USER_PATHS.PINCEINIT_AA_PATH


class INFERIOR_STATUS:
    INFERIOR_RUNNING = 1
    INFERIOR_STOPPED = 2


class INFERIOR_ARCH:
    ARCH_32 = 1
    ARCH_64 = 2


class INJECTION_METHOD:
    SIMPLE_DLOPEN_CALL = 1
    ADVANCED_INJECTION = 2


class BREAKPOINT_TYPE:
    HARDWARE_BP = 1
    SOFTWARE_BP = 2


class WATCHPOINT_TYPE:
    WRITE_ONLY = 1
    READ_ONLY = 2
    BOTH = 3


class BREAKPOINT_ON_HIT:
    BREAK = 1
    FIND_CODE = 2
    FIND_ADDR = 3
    TRACE = 4


class BREAKPOINT_MODIFY:
    CONDITION = 1
    ENABLE = 2
    DISABLE = 3
    ENABLE_ONCE = 4
    ENABLE_COUNT = 5
    ENABLE_DELETE = 6


class STEP_MODE:
    SINGLE_STEP = 1
    STEP_OVER = 2


class TRACE_STATUS:
    STATUS_IDLE = 1
    STATUS_TRACING = 2
    STATUS_CANCELED = 3
    STATUS_PROCESSING = 4
    STATUS_FINISHED = 5


class STOP_REASON:
    PAUSE = 1
    DEBUG = 2


class ATTACH_RESULT:
    ATTACH_SELF = 1
    ATTACH_SUCCESSFUL = 2
    PROCESS_NOT_VALID = 3
    ALREADY_DEBUGGING = 4
    ALREADY_TRACED = 5
    PERM_DENIED = 6


class TOGGLE_ATTACH:
    ATTACHED = 1
    DETACHED = 2


class REGISTERS:
    GENERAL_32 = ["eax", "ebx", "ecx", "edx",
                  "esi", "edi", "ebp", "esp", "eip"]
    GENERAL_64 = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "rip", "r8", "r9", "r10", "r11", "r12",
                  "r13", "r14", "r15"]
    SEGMENT = ["cs", "ss", "ds", "es", "fs", "gs"]
    FLAG = ["cf", "pf", "af", "zf", "sf", "tf", "if", "df", "of"]

    class FLOAT:
        ST = ["st" + str(i) for i in range(8)]
        XMM = ["xmm" + str(i) for i in range(8)]


class FREEZE_TYPE:
    DEFAULT = 0
    INCREMENT = 1
    DECREMENT = 2


class VALUE_REPR:
    UNSIGNED = 0
    SIGNED = 1
    HEX = 2


class VALUE_INDEX:
    # Beginning of the integer indexes, new integer indexes should be added between 0 and 3
    INDEX_INT8 = 0
    INDEX_INT16 = 1
    INDEX_INT32 = 2
    INDEX_INT64 = 3
    # Ending of the integer indexes

    INDEX_FLOAT32 = 4
    INDEX_FLOAT64 = 5

    # Beginning of the string indexes, new string indexes should be added between 6 and 9
    INDEX_STRING_ASCII = 6
    INDEX_STRING_UTF8 = 7
    INDEX_STRING_UTF16 = 8
    INDEX_STRING_UTF32 = 9
    # Ending of the string indexes

    INDEX_AOB = 10  # Array of Bytes

    INDEX_STRUCT = 11
    INDEX_LOOKUP_TABLE = 12

    @staticmethod
    def is_integer(value_index):
        return VALUE_INDEX.INDEX_INT8 <= value_index <= VALUE_INDEX.INDEX_INT64

    @staticmethod
    def is_string(value_index):
        return VALUE_INDEX.INDEX_STRING_ASCII <= value_index <= VALUE_INDEX.INDEX_STRING_UTF32

    @staticmethod
    def has_length(value_index):
        return VALUE_INDEX.INDEX_STRING_ASCII <= value_index <= VALUE_INDEX.INDEX_STRING_UTF32 or \
            value_index == VALUE_INDEX.INDEX_AOB


class SCAN_INDEX:
    INDEX_INT_ANY = 0
    INDEX_INT8 = 1
    INDEX_INT16 = 2
    INDEX_INT32 = 3
    INDEX_INT64 = 4
    INDEX_FLOAT_ANY = 5
    INDEX_FLOAT32 = 6
    INDEX_FLOAT64 = 7
    INDEX_ANY = 8
    INDEX_STRING = 9
    INDEX_AOB = 10  # Array of Bytes
    INDEX_STRUCT = 11
    INDEX_LOOKUP_TABLE = 12


on_hit_to_text_dict = {
    BREAKPOINT_ON_HIT.BREAK: "Break",
    BREAKPOINT_ON_HIT.FIND_CODE: "Find Code",
    BREAKPOINT_ON_HIT.FIND_ADDR: "Find Address",
    BREAKPOINT_ON_HIT.TRACE: "Trace"
}

# Represents the texts at indexes in the address table
index_to_text_dict = collections.OrderedDict([
    (VALUE_INDEX.INDEX_INT8, "Int8"),
    (VALUE_INDEX.INDEX_INT16, "Int16"),
    (VALUE_INDEX.INDEX_INT32, "Int32"),
    (VALUE_INDEX.INDEX_INT64, "Int64"),
    (VALUE_INDEX.INDEX_FLOAT32, "Float32"),
    (VALUE_INDEX.INDEX_FLOAT64, "Float64"),
    (VALUE_INDEX.INDEX_STRING_ASCII, "String_ASCII"),
    (VALUE_INDEX.INDEX_STRING_UTF8, "String_UTF8"),
    (VALUE_INDEX.INDEX_STRING_UTF16, "String_UTF16"),
    (VALUE_INDEX.INDEX_STRING_UTF32, "String_UTF32"),
    (VALUE_INDEX.INDEX_AOB, "Array of Bytes"),
    (VALUE_INDEX.INDEX_STRUCT, "Struct"),
    (VALUE_INDEX.INDEX_LOOKUP_TABLE, "Lookup Table")
])

text_to_index_dict = collections.OrderedDict()
for key in index_to_text_dict:
    text_to_index_dict[index_to_text_dict[key]] = key

scanmem_result_to_index_dict = collections.OrderedDict([
    ("I8", VALUE_INDEX.INDEX_INT8),
    ("I8u", VALUE_INDEX.INDEX_INT8),
    ("I8s", VALUE_INDEX.INDEX_INT8),
    ("I16", VALUE_INDEX.INDEX_INT16),
    ("I16u", VALUE_INDEX.INDEX_INT16),
    ("I16s", VALUE_INDEX.INDEX_INT16),
    ("I32", VALUE_INDEX.INDEX_INT32),
    ("I32u", VALUE_INDEX.INDEX_INT32),
    ("I32s", VALUE_INDEX.INDEX_INT32),
    ("I64", VALUE_INDEX.INDEX_INT64),
    ("I64u", VALUE_INDEX.INDEX_INT64),
    ("I64s", VALUE_INDEX.INDEX_INT64),
    ("F32", VALUE_INDEX.INDEX_FLOAT32),
    ("F64", VALUE_INDEX.INDEX_FLOAT64),
    ("string", VALUE_INDEX.INDEX_STRING_UTF8),
    ("bytearray", VALUE_INDEX.INDEX_AOB),
])

# Represents the texts at indexes in scan combobox
scan_index_to_text_dict = collections.OrderedDict([
    (SCAN_INDEX.INDEX_INT_ANY, "Int(any)"),
    (SCAN_INDEX.INDEX_INT8, "Int8"),
    (SCAN_INDEX.INDEX_INT16, "Int16"),
    (SCAN_INDEX.INDEX_INT32, "Int32"),
    (SCAN_INDEX.INDEX_INT64, "Int64"),
    (SCAN_INDEX.INDEX_FLOAT_ANY, "Float(any)"),
    (SCAN_INDEX.INDEX_FLOAT32, "Float32"),
    (SCAN_INDEX.INDEX_FLOAT64, "Float64"),
    (SCAN_INDEX.INDEX_ANY, "Any(int, float)"),
    (SCAN_INDEX.INDEX_STRING, "String"),
    (SCAN_INDEX.INDEX_AOB, "Array of Bytes"),
    (SCAN_INDEX.INDEX_STRUCT, "Struct"),
    (SCAN_INDEX.INDEX_LOOKUP_TABLE, "Lookup Table")
])

# Used in scan_data_type option of scanmem
scan_index_to_scanmem_dict = collections.OrderedDict([
    (SCAN_INDEX.INDEX_INT_ANY, "int"),
    (SCAN_INDEX.INDEX_INT8, "int8"),
    (SCAN_INDEX.INDEX_INT16, "int16"),
    (SCAN_INDEX.INDEX_INT32, "int32"),
    (SCAN_INDEX.INDEX_INT64, "int64"),
    (SCAN_INDEX.INDEX_FLOAT_ANY, "float"),
    (SCAN_INDEX.INDEX_FLOAT32, "float32"),
    (SCAN_INDEX.INDEX_FLOAT64, "float64"),
    (SCAN_INDEX.INDEX_ANY, "number"),
    (SCAN_INDEX.INDEX_STRING, "string"),
    (SCAN_INDEX.INDEX_AOB, "bytearray")
])


class SCAN_TYPE:
    EXACT = 0
    INCREASED = 1
    INCREASED_BY = 2
    DECREASED = 3
    DECREASED_BY = 4
    LESS = 5
    MORE = 6
    BETWEEN = 7
    CHANGED = 8
    UNCHANGED = 9
    UNKNOWN = 10


# Represents the texts at indexes in combobox
scan_type_to_text_dict = collections.OrderedDict([
    (SCAN_TYPE.EXACT, "Exact Scan"),
    (SCAN_TYPE.INCREASED, "Increased"),
    (SCAN_TYPE.INCREASED_BY, "Increased by"),
    (SCAN_TYPE.DECREASED, "Decreased"),
    (SCAN_TYPE.DECREASED_BY, "Decreased by"),
    (SCAN_TYPE.LESS, "Less Than"),
    (SCAN_TYPE.MORE, "More Than"),
    (SCAN_TYPE.BETWEEN, "Between"),
    (SCAN_TYPE.CHANGED, "Changed"),
    (SCAN_TYPE.UNCHANGED, "Unchanged"),
    (SCAN_TYPE.UNKNOWN, "Unknown Value")
])


class SCAN_MODE:
    NEW = 0
    ONGOING = 1


class SCAN_SCOPE:
    BASIC = 1
    NORMAL = 2
    FULL_RW = 3
    FULL = 4


scan_scope_to_text_dict = collections.OrderedDict([
    (SCAN_SCOPE.BASIC, "Basic"),
    (SCAN_SCOPE.NORMAL, "Normal"),
    (SCAN_SCOPE.FULL_RW, "Read+Write"),
    (SCAN_SCOPE.FULL, "Full")
])

string_index_to_encoding_dict = {
    VALUE_INDEX.INDEX_STRING_UTF8: ["utf-8", "surrogateescape"],
    VALUE_INDEX.INDEX_STRING_UTF16: ["utf-16", "replace"],
    VALUE_INDEX.INDEX_STRING_UTF32: ["utf-32", "replace"],
    VALUE_INDEX.INDEX_STRING_ASCII: ["ascii", "replace"],
}

string_index_to_multiplier_dict = {
    VALUE_INDEX.INDEX_STRING_UTF8: 2,
    VALUE_INDEX.INDEX_STRING_UTF16: 4,
    VALUE_INDEX.INDEX_STRING_UTF32: 8,
}

# first value is the length and the second one is the type
# Check ScriptUtils for an exemplary usage
index_to_valuetype_dict = {
    VALUE_INDEX.INDEX_INT8: [1, "B"],
    VALUE_INDEX.INDEX_INT16: [2, "H"],
    VALUE_INDEX.INDEX_INT32: [4, "I"],
    VALUE_INDEX.INDEX_INT64: [8, "Q"],
    VALUE_INDEX.INDEX_FLOAT32: [4, "f"],
    VALUE_INDEX.INDEX_FLOAT64: [8, "d"],
    VALUE_INDEX.INDEX_STRING_ASCII: [None, None],
    VALUE_INDEX.INDEX_STRING_UTF8: [None, None],
    VALUE_INDEX.INDEX_STRING_UTF16: [None, None],
    VALUE_INDEX.INDEX_STRING_UTF32: [None, None],
    VALUE_INDEX.INDEX_AOB: [None, None],
    VALUE_INDEX.INDEX_STRUCT: [None, None],
    VALUE_INDEX.INDEX_LOOKUP_TABLE: [None, None]
}

# Check ScriptUtils for an exemplary usage
index_to_struct_pack_dict = {
    VALUE_INDEX.INDEX_INT8: "B",
    VALUE_INDEX.INDEX_INT16: "H",
    VALUE_INDEX.INDEX_INT32: "I",
    VALUE_INDEX.INDEX_INT64: "Q",
    VALUE_INDEX.INDEX_FLOAT32: "f",
    VALUE_INDEX.INDEX_FLOAT64: "d"
}

# Format: {tag:tag_description}
tag_to_string = collections.OrderedDict([
    ("MemoryRW", "Memory Read/Write"),
    ("ValueType", "Value Type"),
    ("Injection", "Injection"),
    ("Debug", "Debugging"),
    ("BreakWatchpoints", "Breakpoints&Watchpoints"),
    ("Threads", "Threads"),
    ("Registers", "Registers"),
    ("Stack", "Stack&StackTrace"),
    ("Assembly", "Disassemble&Assemble"),
    ("GDBExpressions", "GDB Expressions"),
    ("GDBCommunication", "GDB Communication"),
    ("Tools", "Tools"),
    ("Utilities", "Utilities"),
    ("Processes", "Processes"),
    ("GUI", "GUI"),
    ("ConditionsLocks", "Conditions&Locks"),
    ("GDBInformation", "GDB Information"),
    ("InferiorInformation", "Inferior Information"),
])

# size-->int, any other field-->str
tuple_breakpoint_info = collections.namedtuple("tuple_breakpoint_info", "number breakpoint_type \
                                                disp enabled address size on_hit hit_count enable_count condition")

# start, end-->int, region-->psutil.Process.memory_maps()[item]
tuple_region_info = collections.namedtuple(
    "tuple_region_info", "start end region")

# all fields-->str/None
tuple_examine_expression = collections.namedtuple(
    "tuple_examine_expression", "all address symbol")

# all fields-->bool
gdb_output_mode = collections.namedtuple(
    "gdb_output_mode", "async_output command_output command_info")


class InferiorRunningException(Exception):
    def __init__(self, message="Inferior is running"):
        super(InferiorRunningException, self).__init__(message)


class GDBInitializeException(Exception):
    def __init__(self, message="GDB not initialized"):
        super(GDBInitializeException, self).__init__(message)


class Frozen:
    def __init__(self, value, freeze_type):
        self.value = value
        self.freeze_type = freeze_type


class ValueType:
    def __init__(self, value_index, length, zero_terminate, value_repr=VALUE_REPR.UNSIGNED):
        """
        Args:
            value_index (int): Determines the type of data. Can be a member of VALUE_INDEX
            length (int): Length of the data. Only used when the value_index is INDEX_STRING or INDEX_AOB
            zero_terminate (bool): If False, ",NZT" will be appended to the text representation
            Only used when value_index is INDEX_STRING. Ignored otherwise. "NZT" stands for "Not Zero Terminate"
            value_repr (int): Determines how the data is represented. Can be a member of VALUE_REPR
        """
        self.value_index = value_index
        self.length = length
        self.zero_terminate = zero_terminate
        self.value_repr = value_repr

    def serialize(self):
        return self.value_index, self.length, self.zero_terminate, self.value_repr

    def text(self):
        """Returns the text representation according to its members

        Returns:
            str: A str generated by given parameters

        Examples:
            value_index=VALUE_INDEX.INDEX_STRING_UTF16, length=15, zero_terminate=False--▼
            returned str="String_UTF16[15],NZT"
            value_index=VALUE_INDEX.INDEX_AOB, length=42-->returned str="AoB[42]"
        """
        returned_string = index_to_text_dict[self.value_index]
        if VALUE_INDEX.is_string(self.value_index):
            returned_string = returned_string + "[" + str(self.length) + "]"
            if not self.zero_terminate:
                returned_string += ",NZT"
        elif self.value_index == VALUE_INDEX.INDEX_AOB:
            returned_string += "[" + str(self.length) + "]"
        if VALUE_INDEX.is_integer(self.value_index):
            if self.value_repr == VALUE_REPR.SIGNED:
                returned_string += "(s)"
            elif self.value_repr == VALUE_REPR.HEX:
                returned_string += "(h)"
        return returned_string


class PointerType:
    def __init__(self, base_address, offsets_list=None):
        """
        Args:
            base_address (str, int): The base address of where this pointer starts from. Can be str expression or int.
            offsets_list (list): List of offsets to reach the final pointed data. Can be None for no offsets.
            Last offset in list won't be dereferenced to emulate CE behaviour.
        """
        self.base_address = base_address
        if offsets_list == None:
            self.offsets_list = []
        else:
            self.offsets_list = offsets_list

    def serialize(self):
        return self.base_address, self.offsets_list

    def get_base_address(self):
        """
        Returns the text representation of this pointer's base address
        """
        return hex(self.base_address) if type(self.base_address) != str else self.base_address


class RegisterQueue:
    def __init__(self):
        self.queue_list = []

    def register_queue(self):
        new_queue = queue.Queue()
        self.queue_list.append(new_queue)
        return new_queue

    def broadcast_message(self, message):
        for item in self.queue_list:
            item.put(message)

    def delete_queue(self, queue_instance):
        try:
            self.queue_list.remove(queue_instance)
        except ValueError:
            pass


class KeyboardModifiersTupleDict(collections.abc.Mapping):
    def _convert_to_int(self, tuple_key):
        return tuple(int(x) for x in tuple_key)

    def __init__(self, OrderedDict_like_list):
        new_dict = {}
        for tuple_key, value in OrderedDict_like_list:
            new_dict[self._convert_to_int(tuple_key)] = value
        self._storage = new_dict

    def __getitem__(self, tuple_key):
        return self._storage[self._convert_to_int(tuple_key)]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)
