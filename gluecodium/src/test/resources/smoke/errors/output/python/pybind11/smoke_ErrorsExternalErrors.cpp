

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"


void register_smoke_ErrorsExternalErrors(py::module_& module) {
    py::enum_<::fire::SomeEnum>(module, "ErrorsExternalErrors")
        .value("NONE", ::fire::SomeEnum::NONE)
        .value("BOOM", ::fire::SomeEnum::BOOM)
        .value("BUST", ::fire::SomeEnum::BUST)
        ;
}

