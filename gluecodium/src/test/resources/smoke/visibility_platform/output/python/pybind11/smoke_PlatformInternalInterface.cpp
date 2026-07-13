

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PlatformInternalInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PlatformInternalInterface = ::smoke::PlatformInternalInterface;

class PlatformInternalInterfaceTrampoline : public PlatformInternalInterface {
public:
    using PlatformInternalInterface::PlatformInternalInterface;

};

void register_PlatformInternalInterface(py::module_& module) {
    py::class_<PlatformInternalInterface, std::shared_ptr<PlatformInternalInterface>, PlatformInternalInterfaceTrampoline>(module, "PlatformInternalInterface")
        .def(py::init<>())
        ;
}

