

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildConstructors.h"
#include "smoke/Constructors.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildConstructors = ::smoke::ChildConstructors;

void register_ChildConstructors(py::module_& module) {
    py::class_<ChildConstructors, std::shared_ptr<ChildConstructors>>(module, "ChildConstructors")
        .def("create", &ChildConstructors::create)
        .def("create", &ChildConstructors::create, py::arg("other"))
        ;
}

