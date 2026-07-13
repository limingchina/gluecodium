

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassFromClass.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildClassFromClass = ::gluecodium::smoke::ChildClassFromClass;

void register_ChildClassFromClass(py::module_& module) {
    py::class_<ChildClassFromClass, std::shared_ptr<ChildClassFromClass>>(module, "ChildClassFromClass")
        .def("child_class_method", &ChildClassFromClass::child_class_method)
        ;
}

