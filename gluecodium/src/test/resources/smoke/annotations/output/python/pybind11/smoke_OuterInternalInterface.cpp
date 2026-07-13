

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterInternalInterface.h"
#include "cstdint"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterInternalInterface = ::smoke::OuterInternalInterface;

class OuterInternalInterfaceTrampoline : public OuterInternalInterface {
public:
    using OuterInternalInterface::OuterInternalInterface;

    int32_t some_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(int32_t, OuterInternalInterface, some_function);
    }
};

void register_OuterInternalInterface(py::module_& module) {
    py::class_<OuterInternalInterface, std::shared_ptr<OuterInternalInterface>, OuterInternalInterfaceTrampoline>(module, "OuterInternalInterface")
        .def("some_function", &OuterInternalInterface::some_function)
        ;
}

