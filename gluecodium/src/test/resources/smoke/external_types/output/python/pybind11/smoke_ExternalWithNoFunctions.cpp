

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "some/path/Bar.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExternalWithNoFunctions = ::gluecodium::smoke::ExternalWithNoFunctions;

class ExternalWithNoFunctionsTrampoline : public ::some::path::Bar {
public:
    using ::some::path::Bar::::some::path::Bar;

};

void register_ExternalWithNoFunctions(py::module_& module) {
    py::class_<::some::path::Bar, std::shared_ptr<::some::path::Bar>, ExternalWithNoFunctionsTrampoline>(module, "ExternalWithNoFunctions")
        ;
}

