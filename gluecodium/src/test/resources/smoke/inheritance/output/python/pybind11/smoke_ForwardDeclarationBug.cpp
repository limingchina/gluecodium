

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ForwardDeclarationBug.h"
#include "smoke/ParentClass.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ForwardDeclarationBug = ::smoke::ForwardDeclarationBug;

void register_ForwardDeclarationBug(py::module_& module) {
    py::class_<ForwardDeclarationBug, std::shared_ptr<ForwardDeclarationBug>>(module, "ForwardDeclarationBug")
        .def("foo", &ForwardDeclarationBug::foo, py::arg("bar"))
        ;
}

