

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/SwiftMethodOverloads.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SwiftMethodOverloads = ::smoke::SwiftMethodOverloads;


void register_smoke_SwiftMethodOverloads(py::module_& module) {
    py::class_<SwiftMethodOverloads, std::shared_ptr<SwiftMethodOverloads>>(module, "smoke_SwiftMethodOverloads")
        .def("one", &SwiftMethodOverloads::one, py::arg("input"))
                .def("two", [](SwiftMethodOverloads& self, const ::std::vector< ::std::string >& input) {
                        self.two(input);
                }, py::arg("input"))
        ;
}

