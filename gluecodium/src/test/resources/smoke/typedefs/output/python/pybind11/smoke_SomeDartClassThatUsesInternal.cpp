

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SomeDartClassThatUsesInternal.h"

void register_SomeDartClassThatUsesInternal(py::module_& module) {
    py::class_<SomeDartClassThatUsesInternal>(module, "SomeDartClassThatUsesInternal")
        .def("add_entity", &SomeDartClassThatUsesInternal::add_entity, py::arg("entity"))
        ;
}

