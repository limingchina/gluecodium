

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DatesSteady.h"
#include "chrono"
#include "optional"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using DatesSteady = ::smoke::DatesSteady;


void register_smoke_DatesSteady(py::module_& module) {
    py::class_<DatesSteady, std::shared_ptr<DatesSteady>>(module, "DatesSteady")
        ;
}

