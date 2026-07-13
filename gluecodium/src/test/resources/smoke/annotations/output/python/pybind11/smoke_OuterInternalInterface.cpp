

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/OuterInternalInterface.h"
#include "cstdint"

void register_OuterInternalInterface(py::module_& module) {
    py::class_<OuterInternalInterface, std::shared_ptr<OuterInternalInterface>>(module, "OuterInternalInterface")
        .def("some_function", &OuterInternalInterface::some_function)
        ;
}

