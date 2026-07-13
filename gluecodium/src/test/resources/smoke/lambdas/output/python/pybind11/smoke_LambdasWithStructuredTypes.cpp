

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "smoke/LambdasDeclarationOrder.h"
#include "smoke/LambdasInterface.h"
#include "smoke/LambdasWithStructuredTypes.h"
#include "functional"
#include "memory"

void register_LambdasWithStructuredTypes(py::module_& module) {
    py::class_<LambdasWithStructuredTypes>(module, "LambdasWithStructuredTypes")
        .def("do_class_stuff", &LambdasWithStructuredTypes::do_class_stuff, py::arg("callback"))
        .def("do_struct_stuff", &LambdasWithStructuredTypes::do_struct_stuff, py::arg("callback"))
        ;
}

