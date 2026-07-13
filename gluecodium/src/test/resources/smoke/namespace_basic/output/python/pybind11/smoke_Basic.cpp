

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "root/space/smoke/Basic.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Basic = ::gluecodium::smoke::Basic;

void register_Basic(py::module_& module) {
    py::class_<Basic, std::shared_ptr<Basic>>(module, "Basic")
        .def("basic_method", &Basic::basic_method, py::arg("input_string"))
        ;
}

