

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "foo/Bar.h"
#include "foo/Bazz.h"
#include "non/Sense.h"
#include "smoke/Structs.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Structs = ::smoke::Structs;


void register_Structs(py::module_& module) {
    py::class_<Structs, std::shared_ptr<Structs>>(module, "Structs")
        .def_static("get_external_struct", &Structs::get_external_struct)

        .def_static("get_another_external_struct", &Structs::get_another_external_struct)

        ;
}

