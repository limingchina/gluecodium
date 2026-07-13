

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "another/SomeCoolClassType.h"

void register_SomeCoolClassType(py::module_& module) {
    py::class_<SomeCoolClassType>(module, "SomeCoolClassType")
        .def("do_important_stuff", &SomeCoolClassType::do_important_stuff)
        ;
}

