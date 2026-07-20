

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "example/FooBar.h"
#include "smoke/Errors.h"
#include "smoke/SomeTypeCollection.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FooBar = ::example::FooBar;


void register_FooBar(py::module_& module) {
    py::class_<FooBar, std::shared_ptr<FooBar>>(module, "FooBar")
        .def_static("method_with_internal_error", &FooBar::method_with_internal_error)

        .def_static("method_with_type_collection_error", &FooBar::method_with_type_collection_error)

        ;
}

