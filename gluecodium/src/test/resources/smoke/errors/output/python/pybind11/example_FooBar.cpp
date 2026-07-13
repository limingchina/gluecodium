

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "example/FooBar.h"
#include "smoke/Errors.h"
#include "smoke/SomeTypeCollection.h"

void register_FooBar(py::module_& module) {
    py::class_<FooBar>(module, "FooBar")
        .def("method_with_internal_error", &FooBar::method_with_internal_error)
        .def("method_with_type_collection_error", &FooBar::method_with_type_collection_error)
        ;
}

