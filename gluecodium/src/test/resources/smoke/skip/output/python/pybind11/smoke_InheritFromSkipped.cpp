

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/InheritFromSkipped.h"

void register_InheritFromSkipped(py::module_& module) {
    py::class_<InheritFromSkipped, std::shared_ptr<InheritFromSkipped>>(module, "InheritFromSkipped")
        ;
}

