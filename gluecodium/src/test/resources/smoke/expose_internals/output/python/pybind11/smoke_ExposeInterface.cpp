

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ExposeInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExposeInterface = ::gluecodium::smoke::ExposeInterface;

class ExposeInterfaceTrampoline : public ExposeInterface {
public:
    using ExposeInterface::ExposeInterface;

};

void register_ExposeInterface(py::module_& module) {
    py::class_<ExposeInterface, std::shared_ptr<ExposeInterface>, ExposeInterfaceTrampoline>(module, "ExposeInterface")
        .def(py::init<>())
        ;
}

