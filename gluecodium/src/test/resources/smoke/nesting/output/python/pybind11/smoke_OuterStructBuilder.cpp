

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterStruct.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Builder = ::smoke::OuterStruct::Builder;


void register_OuterStructBuilder(py::module_& module) {
    py::class_<Builder, std::shared_ptr<Builder>>(module, "OuterStructBuilder")
        .def_static("create", &Builder::create)

        .def("field", &Builder::field, py::arg("value"))

        .def("build", &Builder::build)

        ;
}

