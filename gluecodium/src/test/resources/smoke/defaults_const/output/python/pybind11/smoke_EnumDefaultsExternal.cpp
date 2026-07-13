

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "foo/AlienEnum1.h"
#include "foo/AlienEnum2.h"
#include "smoke/EnumDefaultsExternal.h"
#include "smoke/EnumWrapper.h"
#include "optional"

void register_EnumDefaultsExternal(py::module_& module) {
    py::class_<EnumDefaultsExternal>(module, "EnumDefaultsExternal")
        ;
}

