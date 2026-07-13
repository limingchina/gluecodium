

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/NoCacheInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using NoCacheInterface = ::gluecodium::smoke::NoCacheInterface;

class NoCacheInterfaceTrampoline : public NoCacheInterface {
public:
    using NoCacheInterface::NoCacheInterface;

    void foo(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, NoCacheInterface, foo);
    }
};

void register_NoCacheInterface(py::module_& module) {
    py::class_<NoCacheInterface, std::shared_ptr<NoCacheInterface>, NoCacheInterfaceTrampoline>(module, "NoCacheInterface")
        .def(py::init<>())
        .def("foo", &NoCacheInterface::foo)
        ;
}

