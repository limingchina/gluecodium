

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "gluecodium/DurationHash.h"
#include "smoke/DurationInterface.h"
#include "chrono"
#include "string"

void register_DurationInterface(py::module_& module) {
    py::class_<DurationInterface, std::shared_ptr<DurationInterface>>(module, "DurationInterface")
        .def("duration_function", &DurationInterface::duration_function, py::arg("input"))
        ;
}

