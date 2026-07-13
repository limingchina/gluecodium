

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/LambdasDeclarationOrder.h"
#include "smoke/LambdasInterface.h"
#include "smoke/LambdasWithStructuredTypes.h"
#include "functional"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using LambdasWithStructuredTypes = ::smoke::LambdasWithStructuredTypes;

void register_LambdasWithStructuredTypes(py::module_& module) {
    py::class_<LambdasWithStructuredTypes, std::shared_ptr<LambdasWithStructuredTypes>>(module, "LambdasWithStructuredTypes")
        .def("do_class_stuff", &LambdasWithStructuredTypes::do_class_stuff, py::arg("callback"))
        .def("do_struct_stuff", &LambdasWithStructuredTypes::do_struct_stuff, py::arg("callback"))
        ;
}

