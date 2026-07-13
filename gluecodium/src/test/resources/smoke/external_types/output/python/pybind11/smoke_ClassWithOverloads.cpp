

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "include/ExternalTypes.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ClassWithOverloads = ::gluecodium::smoke::ClassWithOverloads;

void register_ClassWithOverloads(py::module_& module) {
    py::class_<ClassWithOverloads>(module, "ClassWithOverloads")
        .def("one_overload_not_exposed", &ClassWithOverloads::oneOverloadNotExposed)
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input"))
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input_list"))
        .def("all_overloads_exposed", &ClassWithOverloads::allOverloadsExposed, py::arg("input_string"), py::arg("input_bool"))
        ;
}

