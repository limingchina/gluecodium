

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CompressionState.h"
#include "smoke/DartColor.h"
#include "smoke/DartSeason.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalTypes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseDartExternalTypes = ::smoke::UseDartExternalTypes;


void register_smoke_UseDartExternalTypes(py::module_& module) {
    py::class_<UseDartExternalTypes, std::shared_ptr<UseDartExternalTypes>>(module, "UseDartExternalTypes")
        ;
}

