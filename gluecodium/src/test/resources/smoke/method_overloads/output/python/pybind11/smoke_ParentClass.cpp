

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ParentClass.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentClass = ::smoke::ParentClass;

void register_ParentClass(py::module_& module) {
    py::class_<ParentClass, std::shared_ptr<ParentClass>>(module, "ParentClass")
        .def("foo", py::overload_cast<>(&ParentClass::foo))
        .def("foo", py::overload_cast<const int32_t>(&ParentClass::foo), py::arg("input"))
        .def("bar", &ParentClass::bar)
        .def("baz", &ParentClass::baz)
        ;
}

