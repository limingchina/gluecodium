

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/DurationHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DurationSeconds.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DurationSeconds = ::smoke::DurationSeconds;


void register_smoke_DurationSeconds(py::module_& module) {
    py::class_<DurationSeconds, std::shared_ptr<DurationSeconds>>(module, "DurationSeconds")
        .def_property("duration_property", py::overload_cast<>(&DurationSeconds::get_duration_property, py::const_), py::overload_cast<const ::std::chrono::seconds>(&DurationSeconds::set_duration_property))
        ;
}

