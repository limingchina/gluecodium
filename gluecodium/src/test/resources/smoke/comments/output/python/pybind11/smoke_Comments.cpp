

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Comments.h"
#include "cstdint"
#include "functional"
#include "optional"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Comments = ::smoke::Comments;


void register_smoke_Comments(py::module_& module) {
    py::class_<Comments, std::shared_ptr<Comments>>(module, "Comments")
        .def_property("is_some_property", py::overload_cast<>(&Comments::is_some_property, py::const_), py::overload_cast<const bool>(&Comments::set_some_property))
        .def_property_readonly("only_getter_property", py::overload_cast<>(&Comments::get_only_getter_property, py::const_))
        .def_property("is_is_visible", py::overload_cast<>(&Comments::is_is_visible, py::const_), py::overload_cast<const bool>(&Comments::set_is_visible))
        ;
}

