

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CtorLinks.h"
#include "cstdint"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SingleCtorWithTwoArgument = ::smoke::CtorLinks::SingleCtorWithTwoArgument;


void register_smoke_CtorLinksSingleCtorWithTwoArgument(py::module_& module) {
    py::class_<SingleCtorWithTwoArgument, std::shared_ptr<SingleCtorWithTwoArgument>>(module, "CtorLinksSingleCtorWithTwoArgument")
        .def(py::init<int32_t, ::std::string>(py::arg("arg"), py::arg("arg2")))

        .def_static("create", &SingleCtorWithTwoArgument::create, py::arg("arg"), py::arg("arg2"))
        ;
}

