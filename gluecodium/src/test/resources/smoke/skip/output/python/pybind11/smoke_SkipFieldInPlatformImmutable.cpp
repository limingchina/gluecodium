

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/DummyStruct.h"
#include "smoke/SkipFieldInPlatformImmutable.h"
#include "cstdint"

void register_SkipFieldInPlatformImmutable(py::module_& module) {
    py::class_<SkipFieldInPlatformImmutable>(module, "SkipFieldInPlatformImmutable")
        .def_readwrite("int_field", &SkipFieldInPlatformImmutable::int_field)
        .def_readwrite("string_field", &SkipFieldInPlatformImmutable::string_field)
        .def_readwrite("bool_field", &SkipFieldInPlatformImmutable::bool_field)
        ;
}

