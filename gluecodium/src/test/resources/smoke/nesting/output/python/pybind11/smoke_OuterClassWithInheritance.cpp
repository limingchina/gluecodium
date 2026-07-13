

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterClassWithInheritance.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterClassWithInheritance = ::gluecodium::smoke::OuterClassWithInheritance;

void register_OuterClassWithInheritance(py::module_& module) {
    py::class_<OuterClassWithInheritance, std::shared_ptr<OuterClassWithInheritance>>(module, "OuterClassWithInheritance")
        .def("foo", &OuterClassWithInheritance::foo, py::arg("input"))
        ;
}

