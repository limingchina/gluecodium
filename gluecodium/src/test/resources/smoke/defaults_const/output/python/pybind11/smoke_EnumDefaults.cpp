

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "fire/Enum1.h"
#include "fire/Enum2.h"
#include "smoke/EnumDefaults.h"
#include "smoke/EnumWrapper.h"
#include "optional"

void register_EnumDefaults(py::module_& module) {
    py::class_<EnumDefaults>(module, "EnumDefaults")
        ;
}

