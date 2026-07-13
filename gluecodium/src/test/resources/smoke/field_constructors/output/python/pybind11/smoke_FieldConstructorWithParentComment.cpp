

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FieldConstructorWithParentComment.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FieldConstructorWithParentComment = ::smoke::FieldConstructorWithParentComment;

void register_FieldConstructorWithParentComment(py::module_& module) {
    py::class_<FieldConstructorWithParentComment>(module, "FieldConstructorWithParentComment")
        .def_readwrite("string_field", &FieldConstructorWithParentComment::string_field)
        ;
}

