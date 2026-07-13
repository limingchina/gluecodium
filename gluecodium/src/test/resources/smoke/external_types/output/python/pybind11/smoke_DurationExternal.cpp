

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "core/duration.h"
#include "cstdint"

void register_DurationExternal(py::module_& module) {
    py::class_<std::chrono::duration<uint64_t, std::ratio<1,1000>>>(module, "DurationExternal")
        .def_readwrite("value", &std::chrono::duration<uint64_t, std::ratio<1,1000>>::value)
        ;
}

