

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ExposeInternalInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ExposeInternalInterface = ::smoke::ExposeInternalInterface;

class ExposeInternalInterfaceTrampoline : public ExposeInternalInterface {
public:
    using ExposeInternalInterface::ExposeInternalInterface;

};

void register_ExposeInternalInterface(py::module_& module) {
    py::class_<ExposeInternalInterface, std::shared_ptr<ExposeInternalInterface>, ExposeInternalInterfaceTrampoline>(module, "ExposeInternalInterface")
        .def(py::init<>())
        ;
}

