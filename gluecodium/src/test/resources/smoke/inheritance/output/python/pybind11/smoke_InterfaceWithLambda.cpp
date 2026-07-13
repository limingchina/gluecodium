

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InterfaceWithLambda.h"
#include "functional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InterfaceWithLambda = ::gluecodium::smoke::InterfaceWithLambda;

class InterfaceWithLambdaTrampoline : public InterfaceWithLambda {
public:
    using InterfaceWithLambda::InterfaceWithLambda;

};

void register_InterfaceWithLambda(py::module_& module) {
    py::class_<InterfaceWithLambda, std::shared_ptr<InterfaceWithLambda>, InterfaceWithLambdaTrampoline>(module, "InterfaceWithLambda")
        ;
}

