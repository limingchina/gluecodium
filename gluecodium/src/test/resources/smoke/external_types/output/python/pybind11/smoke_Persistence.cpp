

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Persistence.h"

using Persistence = ::smoke::Persistence;



void register_smoke_Persistence(py::module_& module) {
auto cls_Persistence = py::enum_<Persistence>(module, "smoke_Persistence")
        .value("NONE", Persistence::NONE)
        .value("FOR_SESSION", Persistence::FOR_SESSION)
        .value("PERMANENT", Persistence::PERMANENT)
        ;


}
