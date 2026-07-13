

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InheritFromSkipped.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InheritFromSkipped = ::gluecodium::smoke::InheritFromSkipped;

class InheritFromSkippedTrampoline : public InheritFromSkipped {
public:
    using InheritFromSkipped::InheritFromSkipped;

};

void register_InheritFromSkipped(py::module_& module) {
    py::class_<InheritFromSkipped, std::shared_ptr<InheritFromSkipped>, InheritFromSkippedTrampoline>(module, "InheritFromSkipped")
        .def(py::init<>())
        ;
}

