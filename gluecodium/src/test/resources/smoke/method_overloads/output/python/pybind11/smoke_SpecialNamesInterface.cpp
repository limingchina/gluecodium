

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/SpecialNamesInterface.h"
#include "functional"

void register_SpecialNamesInterface(py::module_& module) {
    py::class_<SpecialNamesInterface, std::shared_ptr<SpecialNamesInterface>>(module, "SpecialNamesInterface")
        .def("dispatch", &SpecialNamesInterface::dispatch, py::arg("callback"))
        ;
}

